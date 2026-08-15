/* =====================================================================
   LUNIVAE JEWELS — Product details (product.html)
   ===================================================================== */
(function () {
  'use strict';
  var root = document.getElementById('pdp');
  if (!root) return;
  var params = new URLSearchParams(location.search);
  var id = params.get('id');
  var p = window.LUNIVAE.byId(id) || window.LUNIVAE_PRODUCTS[0];

  if (!p) {
    root.innerHTML = '<section class="section container"><h1 class="section-title">Piece not found</h1>' +
      '<p class="section-lede">This piece is no longer available. <a class="link-arrow" href="shop.html">Back to the collection <span>→</span></a></p></section>';
    return;
  }

  document.title = p.name + ' — Lunivae Jewels';

  var thumbs = p.images.map(function (img, i) {
    return '<button class="pdp__thumb' + (i === 0 ? ' is-active' : '') + '" data-img="assets/' + img + '" aria-label="View image ' + (i + 1) + '">' +
      '<img src="assets/' + img + '" alt="' + p.name + ' view ' + (i + 1) + '" loading="lazy" /></button>';
  }).join('');

  var specs = [
    ['Metal', p.metal],
    ['Stone', p.stone],
    ['Carat', p.carat],
    ['Cut', p.cut],
    ['Colour', p.color],
    ['Clarity', p.clarity],
    ['Certification', p.cert]
  ].map(function (row) {
    return '<div class="spec"><span class="spec__k">' + row[0] + '</span><span class="spec__v">' + row[1] + '</span></div>';
  }).join('');

  var related = window.LUNIVAE_PRODUCTS.filter(function (x) { return x.id !== p.id; }).slice(0, 3).map(function (x) {
    return '<a class="product-card" href="product.html?id=' + x.id + '" data-reveal>' +
      '<div class="product-card__media"><img src="assets/' + x.lead + '" alt="' + x.name + '" loading="lazy" />' +
      '<span class="product-card__tag">' + x.categoryLabel + '</span></div>' +
      '<div class="product-card__body"><h3 class="product-card__name">' + x.name + '</h3>' +
      '<p class="product-card__meta">' + x.metal + ' · ' + x.carat + '</p>' +
      '<div class="product-card__foot"><span class="product-card__price">' + window.LUNIVAE.formatPrice(x.price) + '</span>' +
      '<span class="product-card__view">View piece <em>→</em></span></div></div></a>';
  }).join('');

  root.innerHTML =
    '<section class="pdp container">' +
      '<nav class="breadcrumb" aria-label="Breadcrumb">' +
        '<a href="index.html">Home</a><span>/</span><a href="shop.html">Collection</a><span>/</span><span>' + p.name + '</span>' +
      '</nav>' +
      '<div class="pdp__grid">' +
        '<div class="pdp__gallery">' +
          '<div class="pdp__stage"><img id="pdpMain" src="assets/' + p.images[0] + '" alt="' + p.name + '" /></div>' +
          '<div class="pdp__thumbs">' + thumbs + '</div>' +
        '</div>' +
        '<div class="pdp__info">' +
          '<p class="eyebrow">' + p.categoryLabel + '</p>' +
          '<h1 class="pdp__title">' + p.name + '</h1>' +
          '<p class="pdp__price">' + window.LUNIVAE.formatPrice(p.price) + '<span class="pdp__price-note"> · indicative</span></p>' +
          '<p class="pdp__blurb">' + p.blurb + '</p>' +
          '<div class="pdp__options">' +
            '<div class="pdp__field"><label for="sizeSel">Ring size (US)</label>' +
              '<select id="sizeSel">' +
                ['4','4.5','5','5.5','6','6.5','7','7.5','8','8.5','9','9.5','10'].map(function (s) {
                  return '<option value="' + s + '"' + (s === '6.5' ? ' selected' : '') + '>' + s + '</option>';
                }).join('') +
              '</select></div>' +
            '<div class="pdp__field"><label>Quantity</label>' +
              '<div class="qty qty--lg" id="qtyCtl"><button class="qty__btn" data-act="dec" aria-label="Decrease">–</button>' +
              '<span class="qty__n" id="qtyN">1</span><button class="qty__btn" data-act="inc" aria-label="Increase">+</button></div></div>' +
          '</div>' +
          '<div class="pdp__actions">' +
            '<button class="btn btn--gold btn--block" id="addBtn">Add to Bag · ' + window.LUNIVAE.formatPrice(p.price) + '</button>' +
            '<div class="pdp__actions-row">' +
              '<a class="btn btn--ghost" id="enquireBtn" href="index.html#contact">Enquire</a>' +
              '<button class="btn btn--ghost" id="wishBtn">Save</button>' +
            '</div>' +
          '</div>' +
          '<p class="pdp__reassure">Made to order in 3–4 weeks · Certified &amp; insured worldwide shipping · Lifetime care</p>' +
          '<div class="pdp__specs">' + specs + '</div>' +
          '<div class="pdp__desc"><h2>About this piece</h2><p>' + p.description + '</p></div>' +
        '</div>' +
      '</div>' +
    '</section>' +
    '<section class="section related">' +
      '<div class="container">' +
        '<div class="section-head"><p class="eyebrow">You may also like</p><h2 class="section-title">More from the house.</h2></div>' +
        '<div class="product-grid product-grid--3">' + related + '</div>' +
      '</div>' +
    '</section>';

  // Gallery thumbnail switching
  var main = document.getElementById('pdpMain');
  root.querySelectorAll('.pdp__thumb').forEach(function (t) {
    t.addEventListener('click', function () {
      main.src = t.dataset.img;
      root.querySelectorAll('.pdp__thumb').forEach(function (o) { o.classList.remove('is-active'); });
      t.classList.add('is-active');
    });
  });

  // Quantity stepper
  var qty = 1;
  var qtyN = document.getElementById('qtyN');
  var qtyCtl = document.getElementById('qtyCtl');
  if (qtyCtl) qtyCtl.addEventListener('click', function (e) {
    var b = e.target.closest('.qty__btn'); if (!b) return;
    qty = Math.max(1, qty + (b.getAttribute('data-act') === 'inc' ? 1 : -1));
    qtyN.textContent = qty;
  });

  // Add to Bag
  var addBtn = document.getElementById('addBtn');
  if (addBtn) addBtn.addEventListener('click', function () {
    var size = (document.getElementById('sizeSel') || {}).value || '';
    if (window.LunivaeCart) {
      window.LunivaeCart.add(p.id, qty, size);
      window.LunivaeCart.openDrawer();
    }
    addBtn.textContent = 'Added to Bag ✓';
    setTimeout(function () { addBtn.textContent = 'Add to Bag · ' + window.LUNIVAE.formatPrice(p.price); }, 1600);
  });

  // Enquire → remember which piece, deep link to contact
  var enquire = document.getElementById('enquireBtn');
  enquire.addEventListener('click', function () {
    try { sessionStorage.setItem('lunivae_enquiry', p.name); } catch (e) {}
  });

  // Wishlist (localStorage)
  var wish = document.getElementById('wishBtn');
  function wished() {
    try { return JSON.parse(localStorage.getItem('lunivae_wishlist') || '[]'); } catch (e) { return []; }
  }
  function paintWish() {
    var w = wished();
    var on = w.indexOf(p.id) !== -1;
    wish.textContent = on ? 'Saved to Wishlist ✓' : 'Save to Wishlist';
    wish.classList.toggle('is-saved', on);
  }
  wish.addEventListener('click', function () {
    var w = wished();
    var i = w.indexOf(p.id);
    if (i === -1) w.push(p.id); else w.splice(i, 1);
    try { localStorage.setItem('lunivae_wishlist', JSON.stringify(w)); } catch (e) {}
    paintWish();
  });
  paintWish();

  if (window.LUNIVAE_REVEAL) window.LUNIVAE_REVEAL();
})();
