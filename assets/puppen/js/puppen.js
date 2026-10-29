/**
 * puppen.js — Steckbrief-Overlay und Deep Links
 *
 * Jeder Steckbrief ist eine eigene Seite (/puppen/<figur>/). Sie wird komplett
 * ausgeliefert und zeigt die ganze Puppen-Ansicht mit bereits geöffnetem
 * Steckbrief — als Deep Link für Publikationen und Werbung geeignet.
 *
 * Dieses Skript ergänzt nur die Bedienung:
 *   - Klick auf ein Passbild öffnet den Steckbrief ohne Seitenwechsel
 *   - die Adresszeile führt dabei die teilbare Steckbrief-Adresse
 *   - Zurück-Taste, ESC, Klick daneben und der Schließen-Verweis schließen ihn
 *   - ohne JavaScript bleiben alle Verweise normale Links
 */
(function () {
    "use strict";

    const overlay = document.querySelector(".puppen-overlay");

    if (!overlay) {
        return;
    }

    const steckbriefFenster = overlay.querySelector(".puppen-steckbrief");
    const modalFenster = overlay.querySelector(".puppen-modal");
    const schliessenVerweis = overlay.querySelector(".puppen-overlay-schliessen");
    const uebersichtAdresse = new URL(overlay.dataset.uebersichtUrl || "/", window.location.href);

    // Alles außer dem Overlay wird bei offenem Steckbrief unerreichbar.
    const hintergrundBereiche = [];

    for (const bereich of document.body.children) {
        if (bereich !== overlay) {
            hintergrundBereiche.push(bereich);
        }
    }

    const texte = {
        laden: overlay.dataset.textLaden || "Steckbrief wird geladen …",
        fehler: overlay.dataset.textFehler || "Der Steckbrief konnte leider nicht geladen werden.",
    };

    const geladeneSteckbriefe = new Map();
    let ladeZaehler = 0;
    let zuletztFokussierteKarte = null;

    /* ── Zustand ── */

    function istOffen() {
        return overlay.classList.contains("puppen-overlay--offen");
    }

    function istUebersichtsAdresse() {
        return window.location.pathname === uebersichtAdresse.pathname;
    }

    function setzeOffen(offen) {
        overlay.classList.toggle("puppen-overlay--offen", offen);
        overlay.setAttribute("aria-hidden", offen ? "false" : "true");
        document.body.classList.toggle("puppen-overlay-aktiv", offen);

        // Ältere Browser ignorieren "inert" und verhalten sich wie bisher.
        for (const bereich of hintergrundBereiche) {
            bereich.inert = offen;
        }
    }

    function zeigeHinweis(text, istFehler) {
        const hinweis = document.createElement("p");
        hinweis.className = "puppen-hinweis" + (istFehler ? " puppen-hinweis--fehler" : "");
        hinweis.textContent = text;

        steckbriefFenster.innerHTML = "";
        steckbriefFenster.appendChild(hinweis);
    }

    /* ── Inhalt der Steckbrief-Seite laden ── */

    async function ladeSteckbrief(zielAdresse) {
        const zwischengespeichert = geladeneSteckbriefe.get(zielAdresse);

        if (zwischengespeichert !== undefined) {
            return zwischengespeichert;
        }

        const antwort = await fetch(zielAdresse, {
            cache: "no-cache",
            credentials: "same-origin",
        });

        if (!antwort.ok) {
            throw new Error("Steckbrief nicht erreichbar (Status " + antwort.status + ")");
        }

        const quelltext = await antwort.text();
        const dokument = new DOMParser().parseFromString(quelltext, "text/html");
        const quelle = dokument.querySelector(".puppen-steckbrief");

        if (!quelle) {
            throw new Error("Kein Steckbrief im Dokument gefunden");
        }

        geladeneSteckbriefe.set(zielAdresse, quelle.innerHTML);
        return quelle.innerHTML;
    }

    /* ── Öffnen und Schließen ── */

    async function oeffneSteckbrief(zielAdresse, karte) {
        const ladeNummer = ++ladeZaehler;

        zuletztFokussierteKarte = karte || null;
        setzeOffen(true);
        zeigeHinweis(texte.laden, false);

        try {
            const inhalt = await ladeSteckbrief(zielAdresse);

            if (ladeNummer !== ladeZaehler) {
                return;
            }

            steckbriefFenster.innerHTML = inhalt;
        } catch (fehler) {
            if (ladeNummer !== ladeZaehler) {
                return;
            }

            zeigeHinweis(texte.fehler, true);
        }

        if (modalFenster) {
            modalFenster.scrollTop = 0;
        }

        if (schliessenVerweis) {
            schliessenVerweis.focus({ preventScroll: true });
        }
    }

    function schliesseOverlay(adresseAktualisieren) {
        if (!istOffen()) {
            return;
        }

        // Bei einem Deep Link gibt es keinen vorherigen Klick – dann bekommt
        // die Karte der aktuellen Adresse den Fokus zurück.
        const zurueckZuKarte = zuletztFokussierteKarte || findeKarteZurAdresse();

        setzeOffen(false);
        steckbriefFenster.innerHTML = "";

        if (adresseAktualisieren !== false && !istUebersichtsAdresse()) {
            window.history.pushState({ puppenUebersicht: true }, "", uebersichtAdresse.href);
        }

        zuletztFokussierteKarte = null;

        if (zurueckZuKarte) {
            zurueckZuKarte.focus({ preventScroll: true });
        }
    }

    /* ── Ereignisse ── */

    function istEinfacherKlick(ereignis) {
        return (
            ereignis.button === 0 &&
            !ereignis.metaKey &&
            !ereignis.ctrlKey &&
            !ereignis.shiftKey &&
            !ereignis.altKey
        );
    }

    function findeKarteZurAdresse() {
        const karten = document.querySelectorAll(".puppen-karte[data-steckbrief-url]");

        for (let index = 0; index < karten.length; index += 1) {
            if (karten[index].pathname === window.location.pathname) {
                return karten[index];
            }
        }

        return null;
    }

    document.addEventListener("click", function (ereignis) {
        const karte = ereignis.target.closest(".puppen-karte[data-steckbrief-url]");

        if (karte && istEinfacherKlick(ereignis) && (!karte.target || karte.target === "_self")) {
            const zielAdresse = karte.getAttribute("data-steckbrief-url");

            if (zielAdresse) {
                ereignis.preventDefault();
                window.history.pushState({ steckbrief: zielAdresse }, "", zielAdresse);
                oeffneSteckbrief(zielAdresse, karte);
                return;
            }
        }

        if (ereignis.target.closest(".puppen-overlay-schliessen")) {
            if (istEinfacherKlick(ereignis)) {
                ereignis.preventDefault();
                schliesseOverlay();
            }
            return;
        }

        if (ereignis.target === overlay) {
            schliesseOverlay();
        }
    });

    document.addEventListener("keydown", function (ereignis) {
        if (ereignis.key === "Escape" && istOffen()) {
            ereignis.preventDefault();
            schliesseOverlay();
        }
    });

    window.addEventListener("popstate", function () {
        if (istUebersichtsAdresse()) {
            setzeOffen(false);
            steckbriefFenster.innerHTML = "";
            return;
        }

        const karte = findeKarteZurAdresse();

        if (karte) {
            oeffneSteckbrief(karte.getAttribute("data-steckbrief-url"), karte);
        }
    });

    /* ── Start ── */

    if (istOffen()) {
        // Deep Link: Der Steckbrief kam bereits mit der Seite an.
        setzeOffen(true);

        if (schliessenVerweis) {
            schliessenVerweis.focus({ preventScroll: true });
        }
    }
})();
