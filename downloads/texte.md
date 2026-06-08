---
layout: downloads
title: Texte &amp; Dokumentation
permalink: /downloads/texte/
chapter: Texte
---

<div class="downloads-detail">
    <h1 class="downloads-titel">{{ page.title }}</h1>

    <div class="downloads-beschreibung">
        <p>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor
            incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud
            exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
        </p>
        <p>
            Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
            fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa
            qui officia deserunt mollit anim id est laborum.
        </p>
    </div>

    <div class="dl-grid">
        {% for chapter in site.data.downloads %}
            {% if chapter.chapter == page.chapter %}
                {% for dl in chapter.items %}
                <div class="dl-item">
                    <a class="dl-main-link" href="{{ dl.url }}" target="_blank" rel="noopener">
                        <span class="dl-icon">{{ dl.emoji }}</span>
                        <span class="dl-info">
                            <span class="dl-name">{{ dl.name }}</span>
                            <span class="dl-desc">{{ dl.description }}</span>
                        </span>
                    </a>
                    {% if dl.doclink %}
                    <a class="dl-doclink" href="{{ dl.doclink | relative_url }}" title="Erweitere Dokumentation">
                        &#x1F4C4;
                    </a>
                    {% endif %}
                </div>
                {% endfor %}
            {% endif %}
        {% endfor %}
    </div>

    <p class="downloads-zurueck">
        <a href="{{ '/downloads/' | relative_url }}">&larr; Zur&uuml;ck zur &Uuml;bersicht</a>
    </p>
</div>
