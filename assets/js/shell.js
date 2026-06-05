/* Shared shell behaviour: mobile drawer toggle + same-origin iframe auto-resize */
(function () {
  // --- mobile nav drawer ---
  function bindNav() {
    var toggle = document.querySelector('.navtoggle');
    var scrim = document.querySelector('.scrim');
    if (toggle) toggle.addEventListener('click', function () {
      document.body.classList.toggle('nav-open');
    });
    if (scrim) scrim.addEventListener('click', function () {
      document.body.classList.remove('nav-open');
    });
  }

  // --- auto-size embedded dashboard iframes to their content ---
  function sizeFrame(f) {
    try {
      var doc = f.contentDocument || f.contentWindow.document;
      if (!doc || !doc.body) return;
      // The embeds pin html/body to min-height:0/height:auto, so body.scrollHeight
      // is the true content height and does NOT feed back from the iframe height.
      var h = doc.body.scrollHeight;
      if (h > 0 && Math.abs(h + 2 - parseInt(f.style.height || 0)) > 2) {
        f.style.height = (h + 2) + 'px';
      }
    } catch (e) { /* cross-origin: leave fixed height */ }
  }
  function bindFrames() {
    var frames = document.querySelectorAll('iframe.embed-frame');
    frames.forEach(function (f) {
      var resize = function () { sizeFrame(f); };
      f.addEventListener('load', function () {
        resize();
        // re-measure a few times for late layout / fonts / charts
        [120, 400, 900, 1800].forEach(function (t) { setTimeout(resize, t); });
        try {
          var win = f.contentWindow;
          if (win) win.addEventListener('resize', resize);
        } catch (e) {}
      });
      // already-loaded case
      if (f.contentDocument && f.contentDocument.readyState === 'complete') resize();
    });
    window.addEventListener('resize', function () {
      frames.forEach(function (f) { sizeFrame(f); });
    });
  }

  // --- scrollspy: highlight the section the user is in; smooth-scroll on click ---
  function bindSpy() {
    var spy = document.querySelector('.scrollspy');
    if (!spy) return;
    var links = [].slice.call(spy.querySelectorAll('a'));
    var ids = links.map(function (a) { return a.getAttribute('href').slice(1); });
    var sections = ids.map(function (id) { return document.getElementById(id); }).filter(Boolean);
    function setActive(id) {
      links.forEach(function (a) { a.classList.toggle('active', a.getAttribute('href') === '#' + id); });
    }
    links.forEach(function (a) {
      a.addEventListener('click', function (e) {
        e.preventDefault();
        var t = document.getElementById(a.getAttribute('href').slice(1));
        if (t) { t.scrollIntoView({ behavior: 'smooth', block: 'start' }); setActive(t.id); }
      });
    });
    function onScroll() {
      var top = (document.querySelector('.topbar') ? 68 : 0) + 90;
      var current = sections[0];
      sections.forEach(function (s) {
        if (s.getBoundingClientRect().top <= top) current = s;
      });
      if (current) setActive(current.id);
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // --- accessible tabs (Technology / Industry / Tech×Industry pages) ---
  function bindTabs() {
    var bars = document.querySelectorAll('.tabbar');
    bars.forEach(function (bar) {
      var tabs = [].slice.call(bar.querySelectorAll('[role="tab"]'));
      if (!tabs.length) return;
      function reveal(panel) {
        if (!panel) return;
        var frames = panel.querySelectorAll('iframe.embed-frame');
        var run = function () { frames.forEach(function (f) { sizeFrame(f); }); };
        run(); [60, 250, 700].forEach(function (t) { setTimeout(run, t); });
      }
      function select(tab, focus) {
        tabs.forEach(function (t) {
          var sel = t === tab;
          t.setAttribute('aria-selected', sel ? 'true' : 'false');
          t.tabIndex = sel ? 0 : -1;
          var panel = document.getElementById(t.getAttribute('aria-controls'));
          if (panel) panel.hidden = !sel;
          if (sel) reveal(panel);
        });
        if (focus) tab.focus();
      }
      tabs.forEach(function (t) {
        t.addEventListener('click', function () { select(t); });
        t.addEventListener('keydown', function (e) {
          var idx = tabs.indexOf(t), n = null;
          if (e.key === 'ArrowRight' || e.key === 'ArrowDown') n = tabs[(idx + 1) % tabs.length];
          else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') n = tabs[(idx - 1 + tabs.length) % tabs.length];
          else if (e.key === 'Home') n = tabs[0];
          else if (e.key === 'End') n = tabs[tabs.length - 1];
          if (n) { e.preventDefault(); select(n, true); }
        });
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { bindNav(); bindFrames(); bindSpy(); bindTabs(); });
  } else { bindNav(); bindFrames(); bindSpy(); bindTabs(); }
})();
