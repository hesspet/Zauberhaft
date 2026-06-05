/**
 * puppen.js — Overlay für Steckbriefe
 *
 * Klick auf eine Puppen-Karte öffnet den zugehörigen Steckbrief
 * in einem Overlay (Desktop: zentriertes Modal, Mobile: Slide-up).
 * Der Steckbrief-Inhalt wird per fetch aus der Zielseite extrahiert.
 */
(function () {
    "use strict";

    const OVERLAY_KLASSE = "puppen-overlay";
    const OVERLAY_OFFEN_KLASSE = "puppen-overlay--offen";
    const BODY_SPERR_KLASSE = "puppen-overlay-aktiv";
    const KARTE_KLASSE = "puppen-karte";
    const STEKBRIEF_KLASSE = "puppen-steckbrief";

    let aktuellesOverlay = null;
    let geladeneSteckbriefe = new Map();

    /* ── DOM-Erstellung ── */

    function erstelleOverlay() {
        if (aktuellesOverlay) {
            return aktuellesOverlay;
        }

        const overlay = document.createElement("div");
        overlay.className = OVERLAY_KLASSE;
        overlay.setAttribute("role", "dialog");
        overlay.setAttribute("aria-modal", "true");
        overlay.setAttribute("aria-label", "Steckbrief");

        const schliessenKnopf = document.createElement("button");
        schliessenKnopf.className = "puppen-overlay-schliessen";
        schliessenKnopf.setAttribute("aria-label", "Schließen");
        schliessenKnopf.innerHTML = "&#10005;";
        overlay.appendChild(schliessenKnopf);

        const modal = document.createElement("div");
        modal.className = "puppen-modal";
        overlay.appendChild(modal);

        document.body.appendChild(overlay);
        aktuellesOverlay = { element: overlay, modal: modal, schliessenKnopf: schliessenKnopf };
        return aktuellesOverlay;
    }

    /* ── Overlay öffnen ── */

    async function oeffneSteckbrief(zielUrl, kartenElement) {
        const overlay = erstelleOverlay();

        // Lade-Indikator
        overlay.modal.innerHTML =
            '<p class="puppen-kurztext" style="text-align:center;padding:3rem 0;"> Steckbrief wird geladen …</p>';
        overlay.element.classList.add(OVERLAY_OFFEN_KLASSE);
        document.body.classList.add(BODY_SPERR_KLASSE);

        try {
            const inhalt = await ladeSteckbriefInhalt(zielUrl);
            overlay.modal.innerHTML = "";
            overlay.modal.appendChild(inhalt);
        } catch (fehler) {
            overlay.modal.innerHTML =
                '<p class="puppen-kurztext" style="text-align:center;padding:3rem 0;color:#c44;">' +
                "Der Steckbrief konnte leider nicht geladen werden.</p>";
        }

        // Fokus auf Schließen-Knopf
        overlay.schliessenKnopf.focus();
    }

    /* ── Inhalt laden und extrahieren ── */

    async function ladeSteckbriefInhalt(zielUrl) {
        if (geladeneSteckbriefe.has(zielUrl)) {
            return geladeneSteckbriefe.get(zielUrl).cloneNode(true);
        }

        const antwort = await fetch(zielUrl, {
            cache: "no-cache",
            credentials: "same-origin",
        });

        if (!antwort.ok) {
            throw new Error("Steckbrief nicht erreichbar (Status " + antwort.status + ")");
        }

        const quelltext = await antwort.text();
        const parser = new DOMParser();
        const zielDokument = parser.parseFromString(quelltext, "text/html");

        // Extrahiere den <main>-Inhalt
        const hauptInhalt = zielDokument.querySelector("main.puppen-main");
        if (!hauptInhalt) {
            throw new Error("Kein Hauptinhalt gefunden");
        }

        const steckbriefContainer = document.createElement("div");
        steckbriefContainer.className = STEKBRIEF_KLASSE;

        // Kopiere alle Kindelemente (nicht den main-Wrapper selbst)
        while (hauptInhalt.firstChild) {
            steckbriefContainer.appendChild(hauptInhalt.firstChild);
        }

        geladeneSteckbriefe.set(zielUrl, steckbriefContainer.cloneNode(true));
        return steckbriefContainer;
    }

    /* ── Overlay schließen ── */

    function schliesseOverlay() {
        if (!aktuellesOverlay) {
            return;
        }

        aktuellesOverlay.element.classList.remove(OVERLAY_OFFEN_KLASSE);
        document.body.classList.remove(BODY_SPERR_KLASSE);

        // Fokus zurückgeben
        const aktiveKarte = document.querySelector("." + KARTE_KLASSE + ":focus-within");
        if (aktiveKarte) {
            aktiveKarte.focus();
        }
    }

    /* ── Event-Listener ── */

    document.addEventListener("click", function (ereignis) {
        // Klick auf Puppen-Karte
        const karte = ereignis.target.closest("." + KARTE_KLASSE);
        if (karte && !ereignis.target.closest("a[href]")) {
            ereignis.preventDefault();
            const zielUrl = karte.getAttribute("data-steckbrief-url");
            if (zielUrl) {
                oeffneSteckbrief(zielUrl, karte);
            }
            return;
        }

        // Klick auf Schließen-Knopf
        if (ereignis.target.closest(".puppen-overlay-schliessen")) {
            schliesseOverlay();
            return;
        }

        // Klick außerhalb des Modals (auf den Overlay-Hintergrund)
        if (aktuellesOverlay && ereignis.target === aktuellesOverlay.element) {
            schliesseOverlay();
        }
    });

    // Tastatur: Enter/Space auf Karte
    document.addEventListener("keydown", function (ereignis) {
        const karte = ereignis.target.closest("." + KARTE_KLASSE);
        if (karte && (ereignis.key === "Enter" || ereignis.key === " ")) {
            ereignis.preventDefault();
            const zielUrl = karte.getAttribute("data-steckbrief-url");
            if (zielUrl) {
                oeffneSteckbrief(zielUrl, karte);
            }
            return;
        }

        // ESC schließt Overlay
        if (ereignis.key === "Escape" && aktuellesOverlay) {
            schliesseOverlay();
        }
    });
})();
