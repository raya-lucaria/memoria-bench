(() => {
  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

  // 1. Hero Loop Diagram interactive cycle
  const loopSteps = $$(".loop-step");
  let loopIdx = 0;
  setInterval(() => {
    loopSteps.forEach((el, i) => el.classList.toggle("active", i === loopIdx));
    loopIdx = (loopIdx + 1) % loopSteps.length;
  }, 2600);

  // 2. Harness Tabs
  const tabBtns = $$(".tab-btn");
  const panels = $$(".harness-panel");

  function activateTab(tabName) {
    tabBtns.forEach((btn) => {
      const isActive = btn.dataset.tab === tabName;
      btn.classList.toggle("active", isActive);
      btn.setAttribute("aria-selected", String(isActive));
    });
    panels.forEach((panel) => {
      const isMatch = panel.id === `tab-${tabName}`;
      panel.classList.toggle("active", isMatch);
      panel.hidden = !isMatch;
    });
  }

  tabBtns.forEach((btn) => {
    btn.addEventListener("click", () => activateTab(btn.dataset.tab));
  });

  // 3. Comparison Matrix Filter
  const filterInput = $("#matrix-filter");
  const tableRows = $$("#comparison-table tbody tr");

  filterInput?.addEventListener("input", () => {
    const q = filterInput.value.trim().toLowerCase();
    tableRows.forEach((row) => {
      const text = row.textContent.toLowerCase();
      row.style.display = text.includes(q) ? "" : "none";
    });
  });

  // 4. Memory Benchmark Category Filters
  const benchFilterBtns = $$(".bench-filter-btn");
  const benchCards = $$(".benchmark-card");

  benchFilterBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const filter = btn.dataset.filter;
      benchFilterBtns.forEach((b) => b.classList.toggle("active", b === btn));

      benchCards.forEach((card) => {
        if (filter === "all") {
          card.style.display = "";
        } else {
          const categories = card.dataset.category ? card.dataset.category.split(" ") : [];
          card.style.display = categories.includes(filter) ? "" : "none";
        }
      });
    });
  });
})();
