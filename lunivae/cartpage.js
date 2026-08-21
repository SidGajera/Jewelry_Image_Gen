/* =====================================================================
   LUNIVAE JEWELS — Full cart page (cart.html / #/cart)
   ===================================================================== */
(function () {
  'use strict';
  var root = document.getElementById('cartLayout');
  if (!root) return;
  var C = window.LunivaeCart;
  var fmt = C.format;

  function assetSrc(file) {
    if (window.LUNIVAE_IMG && window.LUNIVAE_IMG[file]) return window.LUNIVAE_IMG[file];
    return 'assets/' + file;
  }
  function link(name) { return window.LUNIVAE_BUNDLE ? '#/' + name : name + '.html'; }

  function render() {
    var lines = C.lines();
    if (!lines.length) {
      root.innerHTML = '<div class="cart-empty">' +
        '<p class="cart-empty__title">Your bag is empty.</p>' +
        '<p class="cart-empty__text">Discover the house silhouettes and begin your piece.</p>' +
        '<a href="' + link('shop') + '" class="btn btn--gold">Explore the Collection</a></div>';
      return;
    }
    var rows = lines.map(function (l) {
      return '<div class="cart-row" data-id="' + l.id + '" data-size="' + (l.size || '') + '">' +
        '<a class="cart-row__media" href="' + link('product') + (window.LUNIVAE_BUNDLE ? '/' + l.id : '?id=' + l.id) + '"><img src="' + assetSrc(l.product.lead) + '" alt="' + l.product.name + '"/></a>' +
        '<div class="cart-row__info">' +
          '<a class="cart-row__name" href="' + link('product') + (window.LUNIVAE_BUNDLE ? '/' + l.id : '?id=' + l.id) + '">' + l.product.name + '</a>' +
          '<p class="cart-row__meta">' + l.product.metal + ' · ' + l.product.carat + (l.size ? ' · Size ' + l.size : '') + '</p>' +
          '<button class="cart-row__rm" data-rm aria-label="Remove">Remove</button>' +
        '</div>' +
        '<div class="cart-row__qty"><div class="qty"><button class="qty__btn" data-act="dec">–</button><span class="qty__n">' + l.qty + '</span><button class="qty__btn" data-act="inc">+</button></div></div>' +
        '<div class="cart-row__price">' + fmt(l.lineTotal) + '</div>' +
      '</div>';
    }).join('');

    var sub = C.subtotal();
    root.innerHTML =
      '<div class="cart-items">' +
        '<div class="cart-items__head"><span>Item</span><span>Quantity</span><span>Total</span></div>' +
        rows +
        '<a href="' + link('shop') + '" class="link-arrow cart-continue">Continue shopping<span>→</span></a>' +
      '</div>' +
      '<aside class="cart-summary">' +
        '<h2 class="cart-summary__title">Order Summary</h2>' +
        '<div class="cart-summary__row"><span>Subtotal</span><span>' + fmt(sub) + '</span></div>' +
        '<div class="cart-summary__row"><span>Shipping</span><span>Complimentary</span></div>' +
        '<div class="cart-summary__row"><span>Duties &amp; taxes</span><span>Calculated at checkout</span></div>' +
        '<div class="cart-summary__total"><span>Total</span><span>' + fmt(sub) + '</span></div>' +
        '<a href="' + link('checkout') + '" class="btn btn--gold btn--block">Proceed to Checkout</a>' +
        '<p class="cart-summary__note">Certified &amp; insured worldwide shipping · Lifetime care</p>' +
      '</aside>';
  }

  root.addEventListener('click', function (e) {
    var row = e.target.closest('.cart-row');
    if (!row) return;
    var id = row.getAttribute('data-id'), size = row.getAttribute('data-size');
    if (e.target.closest('[data-rm]')) { C.remove(id, size); render(); return; }
    var q = e.target.closest('.qty__btn');
    if (q) {
      var cur = C.lines().filter(function (l) { return l.id === id && (l.size || '') === size; })[0];
      if (!cur) return;
      C.setQty(id, size, cur.qty + (q.getAttribute('data-act') === 'inc' ? 1 : -1));
      render();
    }
  });

  C.onChange(render);
  render();
})();
