(function () {
  function initializeSearch() {
  const config = document.getElementById("search-config");
  const searchInput = document.getElementById("search-input");
  const typeFilter = document.getElementById("type-filter");
  const topicFilter = document.getElementById("topic-filter");
  const yearFilter = document.getElementById("year-filter");
  const resultsElement = document.getElementById("search-results");

  if (!config || !searchInput || !typeFilter || !topicFilter || !yearFilter || !resultsElement) {
    return;
  }

  if (config.dataset.searchInitialized === "true") {
    return;
  }

  config.dataset.searchInitialized = "true";

  const searchUrl = config.dataset.searchUrl;
  let configuredTopics = [];
  try {
    configuredTopics = JSON.parse(config.dataset.topics || "[]");
  } catch (e) {
    configuredTopics = [];
  }
  let articles = [];

  function normalizeText(value) {
    return String(value || "")
      .toLocaleLowerCase("de-DE")
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/ä/g, "ae")
      .replace(/ö/g, "oe")
      .replace(/ü/g, "ue")
      .replace(/ß/g, "ss");
  }

  function escapeHtml(value) {
    return String(value || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function scoreArticle(article, query) {
    if (!query) {
      return 1;
    }

    let score = 0;
    const fields = [
      [article.title, 8],
      [(article.topics || []).join(" "), 6],
      [article.summary, 4],
      [article.type, 3],
      [article.content, 1]
    ];

    for (const [field, weight] of fields) {
      const normalizedField = normalizeText(field);
      if (normalizedField.includes(query)) {
        score += weight;
      }
    }

    return score;
  }

  function createOption(value, label) {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = label;
    return option;
  }

  function populateFilters() {
    const types = Array.from(new Set(articles.map((article) => article.type).filter(Boolean))).sort((a, b) => a.localeCompare(b, "de-DE"));
    const years = Array.from(new Set(articles.map((article) => article.year).filter(Boolean))).sort((a, b) => b.localeCompare(a));

    for (const type of types) {
      typeFilter.appendChild(createOption(type, type));
    }

    for (const year of years) {
      yearFilter.appendChild(createOption(year, year));
    }

    const usedTopics = new Set();
    for (const article of articles) {
      for (const topic of (article.topics || [])) {
        usedTopics.add(topic);
      }
    }

    for (const topic of configuredTopics) {
      if (usedTopics.has(topic)) {
        topicFilter.appendChild(createOption(topic, topic));
      }
    }
  }

  function renderResults(results, query) {
    if (results.length === 0) {
      resultsElement.innerHTML = '<p class="empty-state">Keine passenden Artikel gefunden.</p>';
      return;
    }

    const heading = query ? `${results.length} Treffer` : "Neueste Artikel";
    const items = results.slice(0, 50).map((article) => {
      const topics = (article.topics || []).map((topic) => `<li><a href="?topic=${encodeURIComponent(topic)}">${escapeHtml(topic)}</a></li>`).join("");
      return `
        <article class="article-card">
          <div class="article-card__body">
            <div class="article-card__meta">
              <span>${escapeHtml(article.type || "Artikel")}</span>
              <time datetime="${escapeHtml((article.date || "").replace(" ", "T") + ":00")}">${escapeHtml(article.displayDate || article.date)}</time>
            </div>
            <h2 class="article-card__title"><a href="${escapeHtml(article.url)}">${escapeHtml(article.title)}</a></h2>
            <p>${escapeHtml(article.summary || "")}</p>
            ${topics ? `<ul class="tag-list" aria-label="Themen">${topics}</ul>` : ""}
          </div>
        </article>
      `;
    }).join("");

    resultsElement.innerHTML = `<h2 class="search-results__heading">${heading}</h2><div class="article-grid">${items}</div>`;
  }

  function updateResults() {
    const query = normalizeText(searchInput.value.trim());
    const selectedType = typeFilter.value;
    const selectedTopic = topicFilter.value;
    const selectedYear = yearFilter.value;

    const results = articles
      .map((article) => ({ article, score: scoreArticle(article, query) }))
      .filter((entry) => entry.score > 0)
      .filter((entry) => !selectedType || entry.article.type === selectedType)
      .filter((entry) => !selectedTopic || (entry.article.topics || []).includes(selectedTopic))
      .filter((entry) => !selectedYear || entry.article.year === selectedYear)
      .sort((first, second) => {
        if (second.score !== first.score) {
          return second.score - first.score;
        }
        return String(second.article.date).localeCompare(String(first.article.date));
      })
      .map((entry) => entry.article);

    renderResults(query ? results : results.slice(0, 20), query);
  }

  fetch(searchUrl, { credentials: "same-origin" })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Suchindex konnte nicht geladen werden.");
      }
      return response.json();
    })
    .then((data) => {
      articles = Array.isArray(data) ? data : [];
      populateFilters();

      const urlParams = new URLSearchParams(window.location.search);
      const topicFromUrl = urlParams.get("topic");
      if (topicFromUrl) {
        for (const option of topicFilter.options) {
          if (option.value === topicFromUrl) {
            topicFilter.value = topicFromUrl;
            break;
          }
        }
      }

      updateResults();
    })
    .catch(() => {
      resultsElement.innerHTML = '<p class="empty-state">Der Suchindex konnte nicht geladen werden.</p>';
    });

  searchInput.addEventListener("input", updateResults);
  typeFilter.addEventListener("change", updateResults);
  yearFilter.addEventListener("change", updateResults);
  topicFilter.addEventListener("change", updateResults);
  }

  window.zauberhaftInitialisiereSuche = initializeSearch;
  initializeSearch();
})();