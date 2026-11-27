/* AI SDLC Metrics & KPIs Map — interaction layer (design system v1.0, "Interaction and motion"). */
(function () {
  'use strict';
  var d = document, root = d.documentElement;
  root.classList.add('js');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Map topic hover: one dark tooltip "Open <topic> →" with the destination in grey.
     Native SVG titles are not used on nodes, so only one tooltip shows; aria-label keeps the name. */
  var tip = d.querySelector('.tip');
  function place(e, el) {
    var x, y;
    if (e && e.clientX !== undefined && e.type !== 'focus') { x = e.clientX; y = e.clientY; }
    else { var r = el.getBoundingClientRect(); x = r.left + r.width / 2; y = r.top; }
    var w = tip.offsetWidth, h = tip.offsetHeight, vw = window.innerWidth;
    var left = x + 14, top = y - h - 12;
    if (left + w > vw - 8) left = x - w - 14;   // flip near the right edge
    if (left < 8) left = 8;
    if (top < 8) top = y + 18;
    tip.style.left = left + 'px'; tip.style.top = top + 'px';
  }
  if (tip) {
    d.querySelectorAll('a.maplink').forEach(function (a) {
      function show(e) {
        tip.innerHTML = 'Open ' + a.getAttribute('aria-label') + ' →<small>' + a.dataset.dest + '</small>';
        tip.classList.add('on'); place(e, a);
      }
      function hide() { tip.classList.remove('on'); }
      a.addEventListener('mouseenter', show);
      a.addEventListener('mousemove', function (e) { place(e, a); });
      a.addEventListener('mouseleave', hide);
      a.addEventListener('focus', show);
      a.addEventListener('blur', hide);
    });
  }

  /* Band focus: pointing at a band label, or pinning a legend chip, fades the other bands. */
  var svg = d.querySelector('svg.overview'), pinned = null;
  function focusBand(id) {
    if (!svg) return;
    svg.querySelectorAll('.band').forEach(function (b) { b.classList.toggle('cur', b.dataset.band === id); });
    svg.classList.toggle('focused', !!id);
  }
  if (svg) {
    svg.querySelectorAll('.band-label').forEach(function (l) {
      l.addEventListener('mouseenter', function () { if (!pinned) focusBand(l.dataset.band); });
      l.addEventListener('mouseleave', function () { if (!pinned) focusBand(null); });
      l.addEventListener('focus', function () { if (!pinned) focusBand(l.dataset.band); });
      l.addEventListener('blur', function () { if (!pinned) focusBand(null); });
      l.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); togglePin(l.dataset.band); }
      });
      l.addEventListener('click', function () { togglePin(l.dataset.band); });
    });
  }
  var chips = d.querySelectorAll('.chip');
  function togglePin(id) {
    pinned = pinned === id ? null : id;
    chips.forEach(function (c) { c.setAttribute('aria-pressed', String(c.dataset.band === pinned)); });
    focusBand(pinned);
  }
  chips.forEach(function (c) { c.addEventListener('click', function () { togglePin(c.dataset.band); }); });
  d.addEventListener('keydown', function (e) { if (e.key === 'Escape' && pinned) togglePin(pinned); });

  /* Scroll motion: fade up once on entering view; none with reduced motion. */
  var fades = d.querySelectorAll('.fade');
  if (reduce || !('IntersectionObserver' in window)) {
    fades.forEach(function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    fades.forEach(function (el) { io.observe(el); });
  }

  /* Reading progress + current section in "On this page". */
  var bar = d.querySelector('.progress span');
  var links = Array.prototype.slice.call(d.querySelectorAll('.onpage a'));
  var heads = links.map(function (a) { return d.getElementById(a.getAttribute('href').slice(1)); });
  function onScroll() {
    if (bar) {
      var h = root.scrollHeight - root.clientHeight;
      bar.style.width = (h > 0 ? (root.scrollTop / h) * 100 : 0) + '%';
    }
    var cur = -1;
    heads.forEach(function (h, i) { if (h && h.getBoundingClientRect().top < 120) cur = i; });
    links.forEach(function (a, i) { a.classList.toggle('on', i === cur); });
  }
  if (bar || links.length) { window.addEventListener('scroll', onScroll, { passive: true }); onScroll(); }
})();
