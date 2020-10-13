window.addEventListener("DOMContentLoaded", () => {
  const tabs = document.querySelectorAll('.sphinx-tabs-tab');
  const tabLists = document.querySelector('[role="tablist"]');

  // Add a click event handler to each tab
  tabs.forEach(tab => {
    tab.addEventListener("click", changeTabs);
  });

  // Enable arrow navigation between tabs in the tab list
  let tabFocus = 0;
  tabLists.addEventListener("keydown", e => {
    if (e.keyCode === 39 || e.keyCode === 37) {
      tabs[tabFocus].setAttribute("tabindex", -1);
      // Move right
      if (e.keyCode === 39) {
        tabFocus++;
        if (tabFocus >= tabs.length) {
          tabFocus = 0;
        }
      // Move left
      } else if (e.keyCode === 37) {
        tabFocus--;
        if (tabFocus < 0) {
          tabFocus = tabs.length - 1;
        }
      }

      tabs[tabFocus].setAttribute("tabindex", 0);
      tabs[tabFocus].focus();
    }
  });
  const lastSelected = sessionStorage.getItem('sphinx-tabs-last-selected');
  if (lastSelected != null) selectGroupedTabs(lastSelected);
});

function changeTabs(e) {
  const target = e.target;
  const selected = target.getAttribute("aria-selected") === "true";

  deselectTabset(target);

  if (!selected) {
    selectTab(target);
    const name = target.getAttribute("name");
    selectGroupedTabs(name, target.id);

    if (target.classList.contains("group-tab")) {
      // Persist during session
      sessionStorage.setItem('sphinx-tabs-last-selected', name);
    }

  }

}

function selectTab(target) {
  target.setAttribute("aria-selected", true);

  // Show the associated panel
  document
    .getElementById(target.getAttribute("aria-controls"))
    .removeAttribute("hidden");
}

function selectGroupedTabs(name, clickedId=null) {
  const groupedTabs = document.querySelectorAll(`.sphinx-tabs-tab[name="${name}"]`);
  const tabLists = Array.from(groupedTabs).map(tab => tab?.parentNode);

  tabLists
    .forEach(tabList => {
      // Don't want to change the tabList containing the clicked tab
      const clickedTab = tabList.querySelector(`[id="${clickedId}"]`);
      if (clickedTab === null ) {
        // Select first tab with matching name
        const tab = tabList.querySelector(`.sphinx-tabs-tab[name="${name}"]`);
        deselectTabset(tab);
        selectTab(tab);
      }
    })
}

function deselectTabset(target) {
  const parent = target.parentNode;
  const grandparent = parent.parentNode;

  // Hide all tabs in tablist
  parent
  .querySelectorAll('[aria-selected="true"]')
  .forEach(t => t.setAttribute("aria-selected", false));


  // Hide all associated panels
  grandparent
    .querySelectorAll('[role="tabpanel"]')
    .forEach(p => p.setAttribute("hidden", true));
}
