---
layout: puppen
title: "Puppen, Bauchreden und andere Charaktere"
permalink: /puppen/
---

<div class="puppen-uebersicht">
    <h1 class="puppen-titel">{{ page.title }}</h1>

    {% assign puppen_sortiert = site.puppen | sort: "reihenfolge" %}
    <div class="puppen-grid">
        {% for puppe in puppen_sortiert %}
        <div class="puppen-karte"
             data-steckbrief-url="{{ puppe.url | relative_url }}"
             role="button"
             tabindex="0"
             aria-label="Steckbrief von {{ puppe.name }} öffnen">
            <div class="puppen-passbild-rahmen">
                {% if puppe.passbild %}
                <img
                    class="puppen-passbild"
                    src="{{ puppe.passbild | relative_url }}"
                    alt="Passbild von {{ puppe.name }}"
                    loading="lazy"
                >
                {% else %}
                <div class="puppen-passbild-platzhalter" aria-label="Kein Passbild für {{ puppe.name }}"></div>
                {% endif %}
            </div>
            <h2 class="puppen-name">{{ puppe.name }}</h2>
            <p class="puppen-kurztext">{{ puppe.kurztext }}</p>
        </div>
        {% endfor %}
    </div>

    {% if site.puppen.size == 0 %}
    <p class="puppen-leer">Noch keine Charaktere vorhanden. Bald kommen Nasreddin, Alrich, Emse und Wollebert dazu.</p>
    {% endif %}
</div>
