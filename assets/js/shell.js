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
      var h = Math.max(
        doc.body.scrollHeight,
        doc.documentElement ? doc.documentElement.scrollHeight : 0
      );
      if (h > 0) f.style.height = (h + 2) + 'px';
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

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { bindNav(); bindFrames(); });
  } else { bindNav(); bindFrames(); }
})();
