---
layout: downloads
title: Firmware &amp; Apps
permalink: /downloads/firmware/
chapter: Firmware zur direkten Installation
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

    {% for chapter in site.data.downloads %}
        {% if chapter.chapter == page.chapter %}
            {% for sub in chapter.subchapters %}
            <h2 class="downloads-subtitel">{{ sub.name }}</h2>
            <div class="dl-grid">
                {% for dl in sub.items %}
                <a class="dl-item" href="{{ dl.url }}" target="_blank" rel="noopener">
                    <span class="dl-icon">{{ dl.emoji }}</span>
                    <span class="dl-info">
                        <span class="dl-name">{{ dl.name }}</span>
                        <span class="dl-desc">{{ dl.description }}</span>
                    </span>
                </a>
                {% endfor %}
            </div>
            {% endfor %}
        {% endif %}
    {% endfor %}

    <p class="downloads-zurueck">
        <a href="{{ '/downloads/' | relative_url }}">&larr; Zur&uuml;ck zur &Uuml;bersicht</a>
    </p>
</div>
