/* =====================================================================
   LUNIVAE JEWELS — Product listing with left filter sidebar
   Facets: Category · Stone · Price · Metal  (+ Sort)
   Route-aware so the same file powers shop.html and the bundled build.
   ===================================================================== */
(function () {
  'use strict';
  var products = window.LUNIVAE_PRODUCTS || [];
  var grid = document.getElementById('grid');
  if (!grid) return;
  var count = document.getElementById('count');
  var none = document.getElementById('shopNone');
  var sidebar = document.getElementById('filterSidebar');
  var U = window.LUNIVAE;

  function assetSrc(f) {
    if (window.LUNIVAE_IMG && window.LUNIVAE_IMG[f]) return window.LUNIVAE_IMG[f];
    return 'assets/' + f;
  }
  function productHref(id) {
    return window.LUNIVAE_BUNDLE ? '#/product/' + id : 'product.html?id=' + encodeURIComponent(id);
  }

  var state = { category: 'all', stone: [], metal: [], price: 'any', sort: 'featured' };

  // Optional deep link (?cat=pave) for the multipage build
  try {
    var qp = new URLSearchParams(location.search).get('cat');
    if (qp) {
      state.category = qp;
      var r = sidebar && sidebar.querySelector('input[name="category"][value="' + qp + '"]');
      if (r) r.checked = true;
    }
  } catch (e) {}

  function card(p) {
    return '<a class="product-card" href="' + productHref(p.id) + '" data-reveal>' +
      '<div class="product-card__media"><img src="' + assetSrc(p.lead) + '" alt="' + p.name + '" loading="lazy" />' +
      '<span class="product-card__tag">' + p.categoryLabel + '</span></div>' +
      '<div class="product-card__body"><h3 class="product-card__name">' + p.name + '</h3>' +
      '<p class="product-card__meta">' + p.metal + ' · ' + p.carat + '</p>' +
      '<div class="product-card__foot"><span class="product-card__price">' + U.formatPrice(p.price) + '</span>' +
      '<span class="product-card__view">View piece <em>&rarr;</em></span></div></div></a>';
  }

  function inPrice(p) {
    if (state.price === 'any') return true;
    var parts = state.price.split('-'); var lo = +parts[0], hi = +parts[1];
    return p.price >= lo && p.price <= hi;
  }

  function apply() {
    var list = products.filter(function (p) {
      if (state.category !== 'all' && p.category !== state.category) return false;
      if (state.stone.length && state.stone.indexOf(p.stone) === -1) return false;
      if (state.metal.length && state.metal.indexOf(p.metal) === -1) return false;
      if (!inPrice(p)) return false;
      return true;
    });
    if (state.sort === 'price-asc') list.sort(function (a, b) { return a.price - b.price; });
    else if (state.sort === 'price-desc') list.sort(function (a, b) { return b.price - a.price; });
    else if (state.sort === 'name') list.sort(function (a, b) { return a.name.localeCompare(b.name); });

    grid.innerHTML = list.map(card).join('');
    if (count) count.textContent = list.length + (list.length === 1 ? ' piece' : ' pieces');
    if (none) none.hidden = list.length !== 0;
    grid.style.display = list.length ? '' : 'none';
    if (window.LUNIVAE_REVEAL) window.LUNIVAE_REVEAL();
  }

  function readFacets() {
    if (!sidebar) return;
    var cat = sidebar.querySelector('input[name="category"]:checked');
    state.category = cat ? cat.value : 'all';
    var price = sidebar.querySelector('input[name="price"]:checked');
    state.price = price ? price.value : 'any';
    state.stone = Array.prototype.map.call(
      sidebar.querySelectorAll('[data-facet="stone"] input:checked'), function (i) { return i.value; });
    state.metal = Array.prototype.map.call(
      sidebar.querySelectorAll('[data-facet="metal"] input:checked'), function (i) { return i.value; });
  }

  if (sidebar) sidebar.addEventListener('change', function () { readFacets(); apply(); });

  var clear = document.getElementById('filterClear');
  var reset = document.getElementById('resetFilters');
  function clearAll() {
    if (!sidebar) return;
    sidebar.querySelectorAll('input[type="checkbox"]').forEach(function (i) { i.checked = false; });
    var allCat = sidebar.querySelector('input[name="category"][value="all"]');
    if (allCat) allCat.checked = true;
    var anyPrice = sidebar.querySelector('input[name="price"][value="any"]');
    if (anyPrice) anyPrice.checked = true;
    readFacets(); apply();
  }
  if (clear) clear.addEventListener('click', clearAll);
  if (reset) reset.addEventListener('click', clearAll);

  var sortSel = document.getElementById('sort');
  if (sortSel) sortSel.addEventListener('change', function () { state.sort = sortSel.value; apply(); });

  // Mobile: toggle the sidebar open/closed
  var toggle = document.getElementById('filterToggle');
  if (toggle && sidebar) toggle.addEventListener('click', function () {
    var open = sidebar.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', String(open));
  });

  readFacets();
  apply();
})();
