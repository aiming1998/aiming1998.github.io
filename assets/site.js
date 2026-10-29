/* Links remain usable without JavaScript; JavaScript adds accessible tab behavior. */
const tablist = document.querySelector('.tabs');
const tabs = Array.from(document.querySelectorAll('.tab'));
const panels = Array.from(document.querySelectorAll('.panel'));
if (tablist && tabs.length) {
  tablist.setAttribute('role', 'tablist');
  tabs.forEach(tab => {
    tab.setAttribute('role', 'tab');
    tab.setAttribute('aria-controls', tab.hash.slice(1));
  });
  panels.forEach(panel => {
    panel.setAttribute('role', 'tabpanel');
    panel.setAttribute('aria-labelledby', 'tab-' + panel.id);
    panel.tabIndex = 0;
  });
  function activate(id, updateURL = false, focus = false) {
    if (!panels.some(panel => panel.id === id)) id = panels[0].id;
    tabs.forEach(tab => {
      const selected = tab.hash === '#' + id;
      tab.setAttribute('aria-selected', String(selected));
      tab.tabIndex = selected ? 0 : -1;
      if (selected && focus) tab.focus();
    });
    panels.forEach(panel => { panel.hidden = panel.id !== id; });
    if (updateURL) history.replaceState(null, '', '#' + id);
    document.querySelectorAll('[data-language]').forEach(link => {
      link.href = link.getAttribute('data-language') + '#' + id;
    });
  }
  tabs.forEach((tab, index) => {
    tab.addEventListener('click', event => {
      event.preventDefault();
      activate(tab.hash.slice(1), true);
    });
    tab.addEventListener('keydown', event => {
      let target;
      if (event.key === 'ArrowRight') target = (index + 1) % tabs.length;
      if (event.key === 'ArrowLeft') target = (index - 1 + tabs.length) % tabs.length;
      if (event.key === 'Home') target = 0;
      if (event.key === 'End') target = tabs.length - 1;
      if (target !== undefined) {
        event.preventDefault();
        activate(tabs[target].hash.slice(1), true, true);
      }
    });
  });
  window.addEventListener('hashchange', () => activate(location.hash.slice(1)));
  activate(location.hash.slice(1));
}
