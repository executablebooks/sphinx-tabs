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
    // Move right
    if (e.keyCode === 39 || e.keyCode === 37) {
      tabs[tabFocus].setAttribute("tabindex", -1);
      if (e.keyCode === 39) {
        tabFocus++;
        // If we're at the end, go to the start
        if (tabFocus >= tabs.length) {
          tabFocus = 0;
        }
        // Move left
      } else if (e.keyCode === 37) {
        tabFocus--;
        // If we're at the start, move to the end
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
  const selected = target.getAttribute("aria-selected") === true;

  deselectTabset(target);

  if (!selected) {
    const name = target.getAttribute("name");
    // selectGroupedTabs(name, target.id);

    if (target.classList.contains("group-tab")) {
      // Persist during session
      sessionStorage.setItem('sphinx-tabs-last-selected', name);
    }
  }
  selectTab(target);
}

function selectTab(target) {
  // Select tab
  target.setAttribute("aria-selected", true);

  // Show the associated panel
  console.log(target.id)
  console.log(target.tagName);
  document
    .getElementById(target.getAttribute("aria-controls"))
    .removeAttribute("hidden");
}

function selectGroupedTabs(name, notId=null) {
  const groupedTabs = document.querySelectorAll(`.sphinx-tabs-tab[name="${name}"]`);
  console.log(groupedTabs);
  const tabLists = groupedTabs.forEach(tab => tab.parentNode);
  console.log(tabLists);

  tabLists
    .forEach(tabList => 
      tabList.querySelector(`.sphinx-tabs-tab[name="${name}"]`)
      .forEach(function(tab) {
        if (tab.id !== notId) {
          deselectTabset(tab);
          selectTab(tab);
        }})
    )
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
