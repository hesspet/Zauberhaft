---
layout: esp32_firmware
title: ESP32 Firmware
permalink: /downloads/firmware/
---

<div class="downloads-detail">
    <h1 class="downloads-titel">{{ page.title }}</h1>

    <div class="downloads-beschreibung">
        <p>
            Hier findest du Firmware f&uuml;r ESP32-Mikrocontroller zum direkten
            Flashen &uuml;ber den Browser &mdash; kein zus&auml;tzliches Tool n&ouml;tig.
        </p>
        <p>
            W&auml;hle ein Projekt und eine Variante aus. Ein Klick auf
            &bdquo;Installieren&ldquo; &ouml;ffnet den ESP Web Tools-Dialog, der
            die Firmware direkt auf deinen Controller schreibt.
        </p>
        <p>
            <strong>Hinweis 1:</strong> Diese Funktion nutzt die Web Serial API und
            steht nur auf Desktop-Rechnern mit Windows, macOS oder Linux zur
            Verf&uuml;gung. Mobile Ger&auml;te (Android, iOS) werden nicht
            unterst&uuml;tzt.
        </p>
		<p>
            <strong>Hinweis 2:</strong> Ein typisches Problem, dass beim Flashen auftritt, 
			ist, dass die Anwendung das Board nicht findet. Wenn bereits auf dem Board eine 
			Anwendung installiert ist, so kann es sein, dass diese das Board in einen
			Schlafzustand versetzt (BlePrompter macht dies) und somit ist es auch vom Desktop-Rechnern
			nicht erreichbar. Vor dem Flashen muss also das Board in den Empfangszustand versetzt werden.
			In der Regel erfolgt dies bei ESP32 Boards durch das Drücken der Resettaste und der Taste IO9, oft aber auch als BOOT Taste beschriftet
        </p>
		<p>
			<ol>
			  <li>Drücke die Taste "RESET" und halte sie gedrückt.</li>
			  <li>Drücke dann die Taste "BOOT" und halte sie gedrückt.</li>
			  <li>Lasse nun die Taste "RESET" los, halte dabei aber weiterhin die Taste "BOOT" gedrückt.</li>
			  <li>Lasse nun die Taste "BOOT" los.</li>
			  <li>Jetzt ist das Board in einem Haltezustand und kann vom Desktop-Rechner erkannt werden.</li>
			  <li>Flashe nun die gewünschte Firmware.</li>
			</ol>
		</p>
    </div>

    {% if site.data.firmware and site.data.firmware.projects %}
        {% for project in site.data.firmware.projects %}
        <div class="firmware-project">
            <h2 class="firmware-project-name">{{ project.name }}</h2>
            <p class="firmware-project-desc">{{ project.description }}</p>

            {% for variant in project.variants %}
            <div class="firmware-variant">
                <div class="firmware-variant-info">
                    <div class="firmware-variant-name">{{ variant.name }}</div>
                    <div class="firmware-variant-desc">{{ variant.description }}</div>
                </div>
                <div class="firmware-variant-actions">
                    {% if variant.info_file %}
                    <a class="firmware-readme-link"
                       href="{{ '/assets/firmware/' | append: project.slug | append: '/' | append: variant.slug | append: '/' | append: variant.info_file | relative_url }}"
                       target="_blank"
                       title="Versionsinformationen zu {{ variant.name }}">
                        &#x2139;&#xfe0f; Info
                    </a>
                    {% endif %}
                    <esp-web-install-button
                        manifest="{{ '/assets/firmware/' | append: project.slug | append: '/' | append: variant.slug | append: '/manifest.json' | relative_url }}">
                        <button slot="activate" class="firmware-install-button">
                            &#x1F4E5; Installieren
                        </button>
                        <span slot="unsupported">
                            Dein Browser unterst&uuml;tzt Web Serial nicht.
                            Bitte Chrome oder Edge verwenden.
                        </span>
                        <span slot="not-allowed">
                            Bitte diese Seite &uuml;ber HTTPS &ouml;ffnen.
                        </span>
                    </esp-web-install-button>
                </div>
            </div>
            {% endfor %}
        </div>
        {% endfor %}
    {% else %}
        <p class="dl-empty">Noch keine Firmware hinterlegt. Schau sp&auml;ter wieder vorbei.</p>
    {% endif %}

    <p class="downloads-zurueck">
        <a href="{{ '/downloads/' | relative_url }}">&larr; Zur&uuml;ck zur &Uuml;bersicht</a>
    </p>
</div>
