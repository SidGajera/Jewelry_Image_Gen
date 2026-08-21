/* =====================================================================
   LUNIVAE JEWELS — Cart engine + slide-out drawer
   Client-side only (localStorage). Shared across every page.
   ===================================================================== */
(function () {
  'use strict';
  var KEY = 'lunivae_cart';
  var P = function () { return window.LUNIVAE_PRODUCTS || []; };
  var fmt = function (n) { return '$' + n.toLocaleString('en-US'); };
  var listeners = [];

  function read() {
    try { return JSON.parse(localStorage.getItem(KEY) || '[]'); } catch (e) { return []; }
  }
  function write(items) {
    try { localStorage.setItem(KEY, JSON.stringify(items)); } catch (e) {}
    listeners.forEach(function (fn) { try { fn(); } catch (e) {} });
  }
  function keyOf(id, size) { return id + '::' + (size || '-'); }

  var Cart = {
    items: read,
    onChange: function (fn) { listeners.push(fn); },
    count: function () { return read().reduce(function (n, i) { return n + i.qty; }, 0); },
    add: function (id, qty, size) {
      qty = qty || 1;
      var items = read();
      var k = keyOf(id, size);
      var row = items.filter(function (i) { return keyOf(i.id, i.size) === k; })[0];
      if (row) row.qty += qty; else items.push({ id: id, qty: qty, size: size || '' });
      write(items);
    },
    setQty: function (id, size, qty) {
      var items = read().map(function (i) {
        if (keyOf(i.id, i.size) === keyOf(id, size)) i.qty = qty;
        return i;
      }).filter(function (i) { return i.qty > 0; });
      write(items);
    },
    remove: function (id, size) {
      write(read().filter(function (i) { return keyOf(i.id, i.size) !== keyOf(id, size); }));
    },
    clear: function () { write([]); },
    lines: function () {
      var prods = P();
      return read().map(function (i) {
        var p = prods.filter(function (x) { return x.id === i.id; })[0];
        if (!p) return null;
        return { id: i.id, size: i.size, qty: i.qty, product: p, lineTotal: p.price * i.qty };
      }).filter(Boolean);
    },
    subtotal: function () {
      return Cart.lines().reduce(function (s, l) { return s + l.lineTotal; }, 0);
    },
    format: fmt
  };
  window.LunivaeCart = Cart;

  /* ---------------- Drawer UI ---------------- */
  function assetSrc(file) {
    // In the bundled single-file build, images are swapped to data URIs via window.LUNIVAE_IMG
    if (window.LUNIVAE_IMG && window.LUNIVAE_IMG[file]) return window.LUNIVAE_IMG[file];
    return 'assets/' + file;
  }

  function renderDrawer() {
    var body = document.getElementById('drawerBody');
    var foot = document.getElementById('drawerFoot');
    var badge = document.getElementById('cartCount');
    if (badge) {
      var c = Cart.count();
      badge.textContent = c;
      badge.classList.toggle('is-empty', c === 0);
    }
    if (!body || !foot) return;
    var lines = Cart.lines();
    if (!lines.length) {
      body.innerHTML = '<div class="drawer-empty"><p>Your bag is empty.</p>' +
        '<a href="' + link('shop') + '" class="btn btn--gold btn--sm" data-drawer-close>Explore the Collection</a></div>';
      foot.innerHTML = '';
      return;
    }
    body.innerHTML = lines.map(function (l) {
      return '<div class="drawer-item">' +
        '<div class="drawer-item__media"><img src="' + assetSrc(l.product.lead) + '" alt="' + l.product.name + '"/></div>' +
        '<div class="drawer-item__info">' +
          '<p class="drawer-item__name">' + l.product.name + '</p>' +
          (l.size ? '<p class="drawer-item__opt">Size ' + l.size + '</p>' : '') +
          '<p class="drawer-item__price">' + fmt(l.product.price) + '</p>' +
          '<div class="qty" data-id="' + l.id + '" data-size="' + (l.size || '') + '">' +
            '<button class="qty__btn" data-act="dec" aria-label="Decrease">–</button>' +
            '<span class="qty__n">' + l.qty + '</span>' +
            '<button class="qty__btn" data-act="inc" aria-label="Increase">+</button>' +
          '</div>' +
        '</div>' +
        '<button class="drawer-item__rm" data-rm="' + l.id + '" data-size="' + (l.size || '') + '" aria-label="Remove">✕</button>' +
      '</div>';
    }).join('');
    foot.innerHTML =
      '<div class="drawer-sub"><span>Subtotal</span><span>' + fmt(Cart.subtotal()) + '</span></div>' +
      '<p class="drawer-note">Shipping &amp; duties calculated at checkout.</p>' +
      '<a href="' + link('checkout') + '" class="btn btn--gold btn--block">Checkout</a>' +
      '<a href="' + link('cart') + '" class="btn btn--ghost btn--block" data-drawer-close>View Bag</a>';
  }

  // Route-aware link (bundle uses hash routes, multipage uses .html)
  function link(name) {
    if (window.LUNIVAE_BUNDLE) return '#/' + name;
    return name + '.html';
  }

  function openDrawer() {
    var d = document.getElementById('cartDrawer'), o = document.getElementById('drawerOverlay');
    if (!d) return;
    renderDrawer();
    d.classList.add('is-open'); d.setAttribute('aria-hidden', 'false');
    if (o) o.classList.add('is-open');
    document.body.classList.add('no-scroll');
  }
  function closeDrawer() {
    var d = document.getElementById('cartDrawer'), o = document.getElementById('drawerOverlay');
    if (d) { d.classList.remove('is-open'); d.setAttribute('aria-hidden', 'true'); }
    if (o) o.classList.remove('is-open');
    document.body.classList.remove('no-scroll');
  }
  window.LunivaeCart.openDrawer = openDrawer;
  window.LunivaeCart.closeDrawer = closeDrawer;
  window.LunivaeCart.renderDrawer = renderDrawer;

  function wire() {
    var btn = document.getElementById('cartBtn');
    if (btn) btn.addEventListener('click', openDrawer);
    var close = document.getElementById('drawerClose');
    if (close) close.addEventListener('click', closeDrawer);
    var ov = document.getElementById('drawerOverlay');
    if (ov) ov.addEventListener('click', closeDrawer);

    var drawer = document.getElementById('cartDrawer');
    if (drawer) drawer.addEventListener('click', function (e) {
      var rm = e.target.closest('[data-rm]');
      if (rm) { Cart.remove(rm.getAttribute('data-rm'), rm.getAttribute('data-size')); renderDrawer(); return; }
      var q = e.target.closest('.qty__btn');
      if (q) {
        var wrap = q.closest('.qty');
        var id = wrap.getAttribute('data-id'), size = wrap.getAttribute('data-size');
        var cur = read().filter(function (i) { return keyOf(i.id, i.size) === keyOf(id, size); })[0];
        if (!cur) return;
        Cart.setQty(id, size, cur.qty + (q.getAttribute('data-act') === 'inc' ? 1 : -1));
        renderDrawer();
        return;
      }
      if (e.target.closest('[data-drawer-close]')) closeDrawer();
    });

    Cart.onChange(renderDrawer);
    renderDrawer();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', wire);
  else wire();
})();
