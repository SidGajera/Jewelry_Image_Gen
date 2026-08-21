/* =====================================================================
   LUNIVAE JEWELS — main.js
   Preloader · nav state · reveals · counters · cursor · parallax · forms
   ===================================================================== */
(function () {
  'use strict';

  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $  = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));

  /* ---------- Optional raster logo swap ---------- */
  // If body[data-logo="image"] and assets/logo.png exists, replace lockups.
  function maybeSwapLogo() {
    if (document.body.getAttribute('data-logo') !== 'image') return;
    $$('.logo-badge, .brand').forEach((el) => {
      const img = document.createElement('img');
      img.src = 'assets/logo.png';
      img.alt = 'Lunivae Jewels';
      img.className = 'logo-badge__img';
      img.style.width = el.classList.contains('brand') ? '150px' : '100%';
      el.appendChild(img);
    });
  }

  /* ---------- Preloader ---------- */
  function initPreloader() {
    const pre = $('#preloader');
    if (!pre) return;
    let hidden = false;
    const done = () => {
      if (hidden) return;
      hidden = true;
      pre.classList.add('is-done');
      document.body.classList.add('is-loaded');
      setTimeout(() => (pre.style.display = 'none'), 700);
    };
    const min = prefersReduced ? 0 : 900;
    // Fire whether or not the load event has already happened.
    if (document.readyState === 'complete') {
      setTimeout(done, min);
    } else {
      window.addEventListener('load', () => setTimeout(done, min), { once: true });
    }
    // Safety net — always clears the veil quickly.
    setTimeout(done, 2400);
  }

  /* ---------- Header scroll state ---------- */
  function initHeader() {
    const header = $('#header');
    if (!header) return;
    // Inner pages (shop/product) use a permanently solid header.
    if (document.body.hasAttribute('data-solid-nav')) {
      header.classList.add('is-scrolled', 'is-solid');
      return;
    }
    const onScroll = () => header.classList.toggle('is-scrolled', window.scrollY > 40);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---------- Mobile menu ---------- */
  function initMenu() {
    const toggle = $('#menuToggle');
    const menu = $('#mobileMenu');
    if (!toggle || !menu) return;
    const close = () => {
      document.body.classList.remove('is-menu-open');
      toggle.setAttribute('aria-expanded', 'false');
      menu.setAttribute('aria-hidden', 'true');
    };
    toggle.addEventListener('click', () => {
      const open = document.body.classList.toggle('is-menu-open');
      toggle.setAttribute('aria-expanded', String(open));
      menu.setAttribute('aria-hidden', String(!open));
    });
    $$('.mobile-menu__link', menu).forEach((a) => a.addEventListener('click', close));
  }

  /* ---------- Reveal on scroll ---------- */
  let revealIO = null;
  function observeReveals() {
    const items = $$('[data-reveal]:not(.is-in), [data-reveal-lines]:not(.is-in)');
    if (location.search.indexOf('reveal=off') !== -1) {
      items.forEach((el) => { el.classList.add('is-in'); el.style.transitionDelay = '0ms'; });
      const pre = $('#preloader'); if (pre) pre.style.display = 'none';
      return;
    }
    if (prefersReduced || !('IntersectionObserver' in window)) {
      items.forEach((el) => el.classList.add('is-in'));
      return;
    }
    if (!revealIO) {
      revealIO = new IntersectionObserver(
        (entries) => {
          entries.forEach((e) => {
            if (e.isIntersecting) { e.target.classList.add('is-in'); revealIO.unobserve(e.target); }
          });
        },
        { threshold: 0.12, rootMargin: '0px 0px -8% 0px' }
      );
    }
    items.forEach((el) => {
      const sibs = el.parentElement ? $$('[data-reveal]', el.parentElement) : [];
      const idx = sibs.indexOf(el);
      if (idx > 0) el.style.transitionDelay = Math.min(idx * 80, 400) + 'ms';
      revealIO.observe(el);
    });
  }
  // Exposed so dynamically rendered pages (shop/product) can register new nodes.
  window.LUNIVAE_REVEAL = observeReveals;

  /* ---------- Number counters ---------- */
  function initCounters() {
    const nums = $$('[data-count]');
    if (!nums.length) return;
    if (prefersReduced || !('IntersectionObserver' in window)) {
      nums.forEach((n) => (n.textContent = n.dataset.count + (n.dataset.suffix || '')));
      return;
    }
    const run = (el) => {
      const target = parseFloat(el.dataset.count);
      const suffix = el.dataset.suffix || '';
      const dur = 1600;
      const t0 = performance.now();
      const tick = (now) => {
        const p = Math.min(1, (now - t0) / dur);
        const eased = 1 - Math.pow(1 - p, 3);
        el.textContent = Math.round(target * eased) + (p === 1 ? suffix : '');
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    };
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) { run(e.target); io.unobserve(e.target); }
        });
      },
      { threshold: 0.6 }
    );
    nums.forEach((n) => io.observe(n));
  }

  /* ---------- Custom cursor ---------- */
  function initCursor() {
    if (prefersReduced || window.matchMedia('(pointer: coarse)').matches) return;
    const cur = $('#cursor');
    if (!cur) return;
    let x = 0, y = 0, cx = 0, cy = 0;
    document.addEventListener('mousemove', (e) => {
      x = e.clientX; y = e.clientY;
      cur.classList.add('is-active');
    });
    document.addEventListener('mouseleave', () => cur.classList.remove('is-active'));
    const loop = () => {
      cx += (x - cx) * 0.18;
      cy += (y - cy) * 0.18;
      cur.style.transform = `translate(${cx}px, ${cy}px)`;
      requestAnimationFrame(loop);
    };
    loop();
    const hoverSel = 'a, button, .col-card, .field input, .field select, .field textarea';
    document.addEventListener('mouseover', (e) => {
      if (e.target.closest(hoverSel)) cur.classList.add('is-hover');
    });
    document.addEventListener('mouseout', (e) => {
      if (e.target.closest(hoverSel)) cur.classList.remove('is-hover');
    });
  }

  /* ---------- Parallax ---------- */
  function initParallax() {
    if (prefersReduced) return;
    const layers = $$('[data-parallax] img');
    if (!layers.length) return;
    let ticking = false;
    const update = () => {
      const vh = window.innerHeight;
      layers.forEach((img) => {
        const rect = img.parentElement.getBoundingClientRect();
        if (rect.bottom < 0 || rect.top > vh) return;
        const progress = (rect.top + rect.height / 2 - vh / 2) / vh; // -1..1
        img.style.transform = `translate3d(0, ${(-progress * 6).toFixed(2)}%, 0)`;
      });
      ticking = false;
    };
    window.addEventListener('scroll', () => {
      if (!ticking) { requestAnimationFrame(update); ticking = true; }
    }, { passive: true });
    update();
  }

  /* ---------- Hero mouse tilt (subtle) ---------- */
  function initHeroTilt() {
    if (prefersReduced || window.matchMedia('(pointer: coarse)').matches) return;
    const media = $('.hero__media img');
    if (!media) return;
    const hero = $('#hero');
    hero.addEventListener('mousemove', (e) => {
      const r = hero.getBoundingClientRect();
      const dx = (e.clientX - r.left) / r.width - 0.5;
      const dy = (e.clientY - r.top) / r.height - 0.5;
      media.style.transform = `scale(1.06) translate(${(-dx * 14).toFixed(1)}px, ${(-dy * 14).toFixed(1)}px)`;
    });
    hero.addEventListener('mouseleave', () => {
      media.style.transform = 'scale(1.06)';
    });
  }

  /* ---------- Contact form ---------- */
  function initForm() {
    const form = $('#contactForm');
    const note = $('#formNote');
    if (!form) return;
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const name = $('#name').value.trim();
      const email = $('#email').value.trim();
      const interest = $('#interest').value;
      const valid = name && /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email) && interest;
      if (!valid) {
        note.textContent = 'Please add your name, a valid email and an interest.';
        note.classList.add('is-error');
        return;
      }
      note.classList.remove('is-error');
      note.textContent = 'Thank you, ' + name.split(' ')[0] + '. Our atelier will be in touch within one business day.';
      form.reset();
    });

    const news = $('#newsForm');
    if (news) {
      news.addEventListener('submit', (e) => {
        e.preventDefault();
        const input = news.querySelector('input');
        if (input && /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(input.value.trim())) {
          input.value = '';
          input.placeholder = 'Subscribed ✦';
        } else if (input) {
          input.placeholder = 'Enter a valid email';
        }
      });
    }
  }

  /* ---------- Enquiry prefill (arriving from a product page) ---------- */
  function initEnquiryPrefill() {
    let piece = null;
    try { piece = sessionStorage.getItem('lunivae_enquiry'); } catch (e) {}
    if (!piece) return;
    const msg = $('#message');
    const interest = $('#interest');
    if (interest) interest.value = 'collection';
    if (msg && !msg.value) msg.value = "I'm interested in the " + piece + '. Please share availability and options.';
    try { sessionStorage.removeItem('lunivae_enquiry'); } catch (e) {}
    // If deep-linked to #contact, gently focus the name field
    if (location.hash === '#contact') {
      const name = $('#name');
      if (name) setTimeout(() => name.focus(), 400);
    }
  }

  /* ---------- Footer year ---------- */
  function initYear() {
    const y = $('#year');
    if (y) y.textContent = new Date().getFullYear();
  }

  /* ---------- Init ---------- */
  document.addEventListener('DOMContentLoaded', () => {
    maybeSwapLogo();
    initPreloader();
    initHeader();
    initMenu();
    observeReveals();
    initEnquiryPrefill();
    initCounters();
    initCursor();
    initParallax();
    initHeroTilt();
    initForm();
    initYear();
  });
})();
