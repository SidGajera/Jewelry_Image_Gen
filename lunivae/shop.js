/* =====================================================================
   LUNIVAE JEWELS — Product listing (shop.html)
   ===================================================================== */
(function () {
  'use strict';
  var products = window.LUNIVAE_PRODUCTS || [];
  var grid = document.getElementById('grid');
  var count = document.getElementById('count');
  var filtersEl = document.getElementById('filters');
  var sortEl = document.getElementById('sort');
  if (!grid) return;

  var state = { filter: 'all', sort: 'featured' };

  // Deep-link: shop.html?cat=pave
  var params = new URLSearchParams(location.search);
  var cat = params.get('cat');
  if (cat) {
    state.filter = cat;
    Array.prototype.forEach.call(filtersEl.querySelectorAll('.chip'), function (c) {
      c.classList.toggle('is-active', c.dataset.filter === cat);
    });
  }

  function card(p) {
    var a = document.createElement('a');
    a.className = 'product-card';
    a.href = 'product.html?id=' + encodeURIComponent(p.id);
    a.setAttribute('data-reveal', '');
    a.innerHTML =
      '<div class="product-card__media">' +
        '<img src="assets/' + p.lead + '" alt="' + p.name + '" loading="lazy" />' +
        '<span class="product-card__tag">' + p.categoryLabel + '</span>' +
      '</div>' +
      '<div class="product-card__body">' +
        '<h3 class="product-card__name">' + p.name + '</h3>' +
        '<p class="product-card__meta">' + p.metal + ' · ' + p.carat + '</p>' +
        '<div class="product-card__foot">' +
          '<span class="product-card__price">' + window.LUNIVAE.formatPrice(p.price) + '</span>' +
          '<span class="product-card__view">View piece <em>→</em></span>' +
        '</div>' +
      '</div>';
    return a;
  }

  function apply() {
    var list = products.slice();
    if (state.filter !== 'all') {
      list = list.filter(function (p) { return p.category === state.filter; });
    }
    if (state.sort === 'price-asc') list.sort(function (a, b) { return a.price - b.price; });
    else if (state.sort === 'price-desc') list.sort(function (a, b) { return b.price - a.price; });
    else if (state.sort === 'name') list.sort(function (a, b) { return a.name.localeCompare(b.name); });

    grid.innerHTML = '';
    list.forEach(function (p) { grid.appendChild(card(p)); });
    count.textContent = list.length + (list.length === 1 ? ' piece' : ' pieces');

    // trigger reveal for freshly added cards
    if (window.LUNIVAE_REVEAL) window.LUNIVAE_REVEAL();
  }

  filtersEl.addEventListener('click', function (e) {
    var btn = e.target.closest('.chip');
    if (!btn) return;
    state.filter = btn.dataset.filter;
    Array.prototype.forEach.call(filtersEl.querySelectorAll('.chip'), function (c) {
      c.classList.toggle('is-active', c === btn);
    });
    apply();
  });

  sortEl.addEventListener('change', function () { state.sort = sortEl.value; apply(); });

  apply();
})();
