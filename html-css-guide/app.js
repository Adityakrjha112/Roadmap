(() => {
  'use strict';
  const root = document.documentElement;
  const index = JSON.parse(document.getElementById('lesson-index').textContent);
  const views = [...document.querySelectorAll('main > .view')];
  const navLinks = [...document.querySelectorAll('[data-nav]')];
  const search = document.getElementById('search');
  const searchView = document.getElementById('search-view');
  const menu = document.getElementById('menu-toggle');
  const themeButton = document.getElementById('theme-toggle');
  const toast = document.getElementById('toast');
  const storageKey = 'fieldnotes-html-css-v1';
  let state = { read: [], checks: {}, theme: 'light' };
  let toastTimer;
  try {
    const saved = JSON.parse(localStorage.getItem(storageKey));
    if (saved && typeof saved === 'object') {
      state.read = Array.isArray(saved.read) ? saved.read.filter(id => index.some(r => r.id === id)) : [];
      state.read = [...new Set(state.read)];
      state.checks = saved.checks && typeof saved.checks === 'object' ? saved.checks : {};
      state.theme = saved.theme === 'dark' ? 'dark' : 'light';
    }
  } catch { /* The guide remains usable without storage. */ }
  function notify(message) {
    clearTimeout(toastTimer);
    toast.textContent = message;
    toast.classList.add('visible');
    toastTimer = setTimeout(() => toast.classList.remove('visible'), 3200);
  }
  function persist() {
    try { localStorage.setItem(storageKey, JSON.stringify(state)); }
    catch { notify('Progress is available for this visit; browser storage is unavailable.'); }
  }
  function closeMenu() {
    document.body.classList.remove('menu-open');
    menu.setAttribute('aria-expanded', 'false');
    menu.setAttribute('aria-label', 'Open chapter navigation');
  }
  function theme() {
    root.dataset.theme = state.theme;
    themeButton.setAttribute('aria-label', `Switch to ${state.theme === 'dark' ? 'light' : 'dark'} theme`);
  }
  function progress() {
    const read = new Set(state.read);
    document.getElementById('progress-count').textContent = `${read.size} / 24`;
    document.getElementById('reading-progress').value = read.size;
    navLinks.forEach(a => a.classList.toggle('read', read.has(a.dataset.nav)));
    document.querySelectorAll('.mark-read').forEach(button => {
      const complete = read.has(button.dataset.lesson);
      button.setAttribute('aria-pressed', String(complete));
      button.textContent = complete ? 'Chapter read ✓ · undo' : 'Mark chapter as read ✓';
    });
    const next = index.find(r => !read.has(r.id));
    const link = document.getElementById('continue-link');
    link.href = next ? `#${next.id}` : '#projects';
    link.textContent = read.size ? (next ? 'Continue learning ↗' : 'Build a mini project ↗') : 'Start learning ↗';
    document.querySelectorAll('[data-check]').forEach(input => { input.checked = Boolean(state.checks[input.dataset.check]); });
  }
  function route(moveFocus = false) {
    const id = location.hash.slice(1) || 'overview';
    const target = document.getElementById(id);
    const view = target && target.closest('main > .view') || document.getElementById('overview');
    search.value = '';
    views.forEach(v => { v.hidden = v !== view; });
    navLinks.forEach(a => {
      if (a.dataset.nav === view.id) a.setAttribute('aria-current', 'page');
      else a.removeAttribute('aria-current');
    });
    const activeLink = navLinks.find(a => a.dataset.nav === view.id);
    if (activeLink?.closest('details')) activeLink.closest('details').open = true;
    const lesson = index.find(r => r.id === view.id);
    document.title = lesson ? `${lesson.title} — Fieldnotes` : 'Fieldnotes — Learn HTML & CSS';
    closeMenu();
    if (moveFocus) {
      const heading = view.querySelector('h1');
      if (heading) { heading.tabIndex = -1; heading.focus({ preventScroll: true }); }
      if (target && target !== view) target.scrollIntoView();
      else window.scrollTo(0, 0);
    }
  }
  function runSearch() {
    const query = search.value.trim().toLocaleLowerCase();
    if (!query) { route(); return; }
    views.forEach(v => { v.hidden = v !== searchView; });
    const words = query.split(/\s+/);
    const matches = index.filter(r => words.every(w => `${r.title} ${r.text}`.toLocaleLowerCase().includes(w)));
    const results = document.getElementById('search-results');
    results.replaceChildren();
    document.getElementById('search-count').textContent = matches.length ? `${matches.length} ${matches.length === 1 ? 'chapter' : 'chapters'} for “${search.value.trim()}”` : 'No matching chapters. Try “forms”, “grid”, “margin”, or “focus”.';
    for (const row of matches) {
      const a = document.createElement('a'); a.href = `#${row.id}`; a.className = 'search-result';
      const meta = document.createElement('small'); meta.textContent = `PART ${row.part} · CHAPTER ${row.id.slice(-2)}`;
      const title = document.createElement('h2'); title.textContent = `${row.title} →`;
      const description = document.createElement('p'); description.textContent = row.text.slice(0, 185) + '…';
      a.append(meta, title, description); results.append(a);
    }
  }
  root.classList.add('js');
  theme(); progress(); route();
  window.addEventListener('hashchange', () => route(true));
  search.addEventListener('input', runSearch);
  document.getElementById('clear-search').addEventListener('click', () => route(true));
  document.addEventListener('click', event => {
    const anchor = event.target.closest('a[href^="#"]');
    if (anchor && anchor.getAttribute('href') === location.hash && !anchor.classList.contains('skip-link')) route(true);
    if (document.body.classList.contains('menu-open') && !event.target.closest('#sidebar, #menu-toggle')) closeMenu();
  });
  menu.addEventListener('click', () => {
    const open = document.body.classList.toggle('menu-open');
    menu.setAttribute('aria-expanded', String(open));
    menu.setAttribute('aria-label', open ? 'Close chapter navigation' : 'Open chapter navigation');
  });
  document.addEventListener('keydown', event => {
    if (event.key === '/' && !event.metaKey && !event.ctrlKey && !event.altKey && !event.target.closest('input, textarea, [contenteditable="true"]')) {
      event.preventDefault(); search.focus();
    }
    if (event.key === 'Escape') {
      if (document.body.classList.contains('menu-open')) { closeMenu(); menu.focus(); }
      else if (search.value) { route(true); }
    }
  });
  themeButton.addEventListener('click', () => { state.theme = state.theme === 'light' ? 'dark' : 'light'; theme(); persist(); });
  document.querySelectorAll('.mark-read').forEach(button => button.addEventListener('click', () => {
    const id = button.dataset.lesson;
    const wasRead = state.read.includes(id);
    state.read = wasRead ? state.read.filter(value => value !== id) : [...state.read, id];
    progress(); persist(); notify(wasRead ? 'Chapter marked unread.' : 'One small step forward. Chapter marked as read.');
  }));
  document.querySelectorAll('[data-check]').forEach(input => input.addEventListener('change', () => {
    state.checks[input.dataset.check] = input.checked; persist();
  }));
  document.querySelectorAll('.copy').forEach(button => button.addEventListener('click', async () => {
    const code = button.closest('.code-panel').querySelector('code');
    try {
      await navigator.clipboard.writeText(code.textContent);
      notify('Code copied. Paste it into your HTML file.');
    } catch {
      const range = document.createRange(); range.selectNodeContents(code);
      const selection = window.getSelection(); selection.removeAllRanges(); selection.addRange(range);
      notify('Code selected. Use your browser’s Copy command.');
    }
  }));
  document.getElementById('reset-progress').addEventListener('click', () => {
    if (!window.confirm('Reset all chapter reading progress and revision checkboxes in this browser?')) return;
    state.read = []; state.checks = {}; progress(); persist(); notify('A fresh page. Your reading progress has been reset.');
  });
})();
