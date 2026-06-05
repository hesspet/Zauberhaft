(function () {
  const blogPfadMuster = /\/blog(?:\/|$)/;
  const blogStartVerweis = document.querySelector("a[href*='/blog/']");
  const basisPfad = blogStartVerweis
    ? new URL(blogStartVerweis.href, window.location.href).pathname.replace(/blog\/.*$/, "")
    : "/";
  const geladeneDokumente = new Map();
  let laufendeAnfrage = null;

  function istBlogAdresse(adresse) {
    return adresse.origin === window.location.origin && blogPfadMuster.test(adresse.pathname);
  }

  function istInterneSeitenAdresse(adresse) {
    return (
      adresse.origin === window.location.origin &&
      (adresse.pathname === basisPfad || adresse.pathname.startsWith(`${basisPfad}blog/`))
    );
  }

  function istGleicheDokumentAdresse(adresse) {
    return adresse.pathname === window.location.pathname && adresse.search === window.location.search;
  }

  function ermittleVerweisElement(ereignis) {
    return ereignis.target && ereignis.target.closest
      ? ereignis.target.closest("a[href]")
      : null;
  }

  function istNavigierbarerBlogVerweis(verweisElement, ereignis) {
    if (!verweisElement) {
      return false;
    }

    if (
      ereignis &&
      (ereignis.defaultPrevented ||
        ereignis.metaKey ||
        ereignis.ctrlKey ||
        ereignis.shiftKey ||
        ereignis.altKey)
    ) {
      return false;
    }

    if (ereignis && "button" in ereignis && ereignis.button !== 0) {
      return false;
    }

    if (verweisElement.hasAttribute("download")) {
      return false;
    }

    const zielFenster = verweisElement.getAttribute("target");

    if (zielFenster && zielFenster !== "_self") {
      return false;
    }

    const zielAdresse = new URL(verweisElement.href, window.location.href);

    if (!istInterneSeitenAdresse(zielAdresse)) {
      return false;
    }

    return !istGleicheDokumentAdresse(zielAdresse);
  }

  function setzeLadezustand(istAktiv) {
    document.documentElement.classList.toggle("blog-client-navigation-active", istAktiv);
  }

  async function ladeDokument(zielAdresse) {
    const zwischenspeicherKennung = zielAdresse.href;

    if (geladeneDokumente.has(zwischenspeicherKennung)) {
      return geladeneDokumente.get(zwischenspeicherKennung).cloneNode(true);
    }

    if (laufendeAnfrage) {
      laufendeAnfrage.abort();
    }

    laufendeAnfrage = new AbortController();

    const antwort = await fetch(zielAdresse.href, {
      cache: "no-cache",
      credentials: "same-origin",
      signal: laufendeAnfrage.signal,
    });

    if (!antwort.ok) {
      throw new Error("Die Zielseite konnte nicht geladen werden.");
    }

    const quelltext = await antwort.text();
    const parser = new DOMParser();
    const zielDokument = parser.parseFromString(quelltext, "text/html");
    geladeneDokumente.set(zwischenspeicherKennung, zielDokument);
    return zielDokument.cloneNode(true);
  }

  function ermittleStylesheetAdressen(dokument, dokumentAdresse) {
    return Array.from(dokument.querySelectorAll('link[rel="stylesheet"][href]')).map((stylesheet) =>
      new URL(stylesheet.getAttribute("href"), dokumentAdresse.href).href
    );
  }

  function ladeStylesheet(stylesheetAdresse) {
    const vorhandenesStylesheet = Array.from(document.querySelectorAll('link[rel="stylesheet"][href]')).find(
      (stylesheet) => new URL(stylesheet.getAttribute("href"), window.location.href).href === stylesheetAdresse
    );

    if (vorhandenesStylesheet) {
      return Promise.resolve();
    }

    return new Promise((resolve) => {
      const stylesheet = document.createElement("link");
      stylesheet.rel = "stylesheet";
      stylesheet.href = stylesheetAdresse;
      stylesheet.dataset.blogClientNavigation = "true";
      stylesheet.addEventListener("load", resolve, { once: true });
      stylesheet.addEventListener("error", resolve, { once: true });
      document.head.appendChild(stylesheet);
      window.setTimeout(resolve, 1500);
    });
  }

  async function bereiteStylesheetsVor(zielDokument, zielAdresse) {
    const stylesheetAdressen = ermittleStylesheetAdressen(zielDokument, zielAdresse);
    await Promise.all(stylesheetAdressen.map(ladeStylesheet));
    return stylesheetAdressen;
  }

  function entferneAlteStylesheets(aktiveStylesheetAdressen) {
    const aktiveAdressen = new Set(aktiveStylesheetAdressen);

    for (const stylesheet of document.querySelectorAll('link[rel="stylesheet"][href]')) {
      const stylesheetAdresse = new URL(stylesheet.getAttribute("href"), window.location.href).href;

      if (!aktiveAdressen.has(stylesheetAdresse)) {
        stylesheet.remove();
      }
    }
  }

  function scrolleZumZiel(zielAdresse) {
    if (!zielAdresse.hash) {
      window.scrollTo({ top: 0, left: 0, behavior: "auto" });
      return;
    }

    const zielKennung = decodeURIComponent(zielAdresse.hash.slice(1));
    const zielElement = document.getElementById(zielKennung);

    if (zielElement) {
      zielElement.scrollIntoView({ block: "start", behavior: "auto" });
    } else {
      window.scrollTo({ top: 0, left: 0, behavior: "auto" });
    }
  }

  async function ersetzeDokumentteile(zielDokument, zielAdresse, sollVerlaufSchreiben) {
    if (!zielDokument.body) {
      throw new Error("Die Zielseite hat keine verwendbare Dokumentstruktur.");
    }

    const aktiveStylesheetAdressen = await bereiteStylesheetsVor(zielDokument, zielAdresse);
    const neuerDokumentkoerper = zielDokument.body.cloneNode(true);

    document.title = zielDokument.title;
    document.body.replaceWith(neuerDokumentkoerper);
    entferneAlteStylesheets(aktiveStylesheetAdressen);

    if (sollVerlaufSchreiben) {
      window.history.pushState({ blogNavigation: true }, "", zielAdresse.href);
    }

    scrolleZumZiel(zielAdresse);

    if (window.zauberhaftInitialisiereSuche) {
      window.zauberhaftInitialisiereSuche();
    }

    document.dispatchEvent(
      new CustomEvent("blog:navigation", {
        detail: { url: zielAdresse.href },
      })
    );
  }

  async function navigiereZu(verweisElement) {
    const zielAdresse = new URL(verweisElement.href, window.location.href);

    try {
      setzeLadezustand(true);
      const zielDokument = await ladeDokument(zielAdresse);
      ersetzeDokumentteile(zielDokument, zielAdresse, true);
    } catch (fehler) {
      if (fehler.name === "AbortError") {
        return;
      }

      window.location.href = zielAdresse.href;
    } finally {
      setzeLadezustand(false);
    }
  }

  function ladeImHintergrund(verweisElement) {
    if (!istNavigierbarerBlogVerweis(verweisElement)) {
      return;
    }

    const zielAdresse = new URL(verweisElement.href, window.location.href);

    if (geladeneDokumente.has(zielAdresse.href)) {
      return;
    }

    fetch(zielAdresse.href, { cache: "no-cache", credentials: "same-origin" })
      .then((antwort) => (antwort.ok ? antwort.text() : ""))
      .then((quelltext) => {
        if (!quelltext) {
          return;
        }

        const parser = new DOMParser();
        geladeneDokumente.set(zielAdresse.href, parser.parseFromString(quelltext, "text/html"));
      })
      .catch(() => {});
  }

  document.addEventListener("click", function (ereignis) {
    const verweisElement = ermittleVerweisElement(ereignis);

    if (!istNavigierbarerBlogVerweis(verweisElement, ereignis)) {
      return;
    }

    ereignis.preventDefault();
    navigiereZu(verweisElement);
  });

  document.addEventListener(
    "pointerenter",
    function (ereignis) {
      ladeImHintergrund(ermittleVerweisElement(ereignis));
    },
    true
  );

  document.addEventListener(
    "focusin",
    function (ereignis) {
      ladeImHintergrund(ermittleVerweisElement(ereignis));
    },
    true
  );

  window.addEventListener("popstate", function () {
    if (!istInterneSeitenAdresse(new URL(window.location.href))) {
      window.location.reload();
      return;
    }

    ladeDokument(new URL(window.location.href))
      .then((zielDokument) => {
        const aktuelleAdresse = new URL(window.location.href);
        ersetzeDokumentteile(zielDokument, aktuelleAdresse, false);
      })
      .catch(() => {
        window.location.reload();
      });
  });
})();
