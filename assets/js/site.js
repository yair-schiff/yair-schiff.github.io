(function () {
  var root = document.documentElement;

  // Light/dark toggle (initial theme is set in <head> to avoid a flash)
  var toggle = document.querySelector('.theme-toggle');
  function label() {
    var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    var text = 'Switch to ' + next + ' mode';
    toggle.setAttribute('aria-label', text);
    toggle.setAttribute('title', text);
  }
  if (toggle) {
    label();
    toggle.addEventListener('click', function () {
      var theme = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', theme);
      try { localStorage.setItem('theme', theme); } catch (e) {}
      label();
    });
  }

  // Publication filters: the section's data-show attribute drives CSS visibility
  var pubs = document.querySelector('.publications');
  var buttons = document.querySelectorAll('[data-filter]');
  Array.prototype.forEach.call(buttons, function (btn) {
    btn.addEventListener('click', function () {
      pubs.setAttribute('data-show', btn.getAttribute('data-filter'));
      Array.prototype.forEach.call(buttons, function (b) {
        b.setAttribute('aria-pressed', b === btn ? 'true' : 'false');
      });
    });
  });

  // Back-to-top button: appears once the Publications heading (or 600px) is scrolled past
  var toTop = document.querySelector('.to-top');
  function onScroll() {
    var past = pubs ? pubs.getBoundingClientRect().top < 0 : window.scrollY > 600;
    toTop.classList.toggle('show', past);
  }
  if (toTop) {
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
    toTop.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });
  }
})();
