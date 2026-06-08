---
layout: blog_page
title: "Suche"
summary: "Lokale Suche im Artikelarchiv."
permalink: /blog/suche/
---

{% assign asset_version = site.github.build_revision | default: site.time %}

<div id="search-config"
     data-search-url="{{ '/blog/search.json' | relative_url }}?v={{ asset_version | uri_escape }}"
     data-topics="{{ site.data.blog_topics | jsonify | escape }}"></div>

<form class="search-controls" role="search">
  <label for="search-input">Suchbegriff</label>
  <input id="search-input" type="search" placeholder="Suchbegriff eingeben..." autocomplete="off">

  <label for="type-filter">Artikeltyp</label>
  <select id="type-filter">
    <option value="">Alle Typen</option>
  </select>

  <label for="topic-filter">Thema</label>
  <select id="topic-filter">
    <option value="">Alle Themen</option>
  </select>

  <label for="year-filter">Jahr</label>
  <select id="year-filter">
    <option value="">Alle Jahre</option>
  </select>
</form>

<div id="search-results" class="search-results" aria-live="polite">
  <p class="empty-state">Die Suche wird geladen.</p>
</div>

<noscript>
  <p class="empty-state">Die Suche benötigt JavaScript. Archiv und Themenübersicht funktionieren ohne JavaScript.</p>
</noscript>
