/* =====================================================================
   LUNIVAE JEWELS — Checkout (checkout.html / #/checkout)
   Multi-step: Information → Payment → Review → Confirmation.
   Client-side only. Payment is a demo — no real transaction occurs.
   ===================================================================== */
(function () {
  'use strict';
  var root = document.getElementById('checkoutRoot');
  if (!root) return;
  var C = window.LunivaeCart;
  var fmt = C.format;

  function assetSrc(f) {
    if (window.LUNIVAE_IMG && window.LUNIVAE_IMG[f]) return window.LUNIVAE_IMG[f];
    return 'assets/' + f;
  }
  function link(name) { return window.LUNIVAE_BUNDLE ? '#/' + name : name + '.html'; }

  var STEPS = ['Information', 'Payment', 'Review'];
  var step = 0;
  var data = {}; // collected field values
  var order = null; // set after placing

  function esc(s) { return (s == null ? '' : String(s)).replace(/"/g, '&quot;'); }
  // DOM ids are namespaced with co_ so they never collide with other forms
  // (e.g. the home contact form) when everything shares one document (bundle).
  function field(id, label, type, opts) {
    opts = opts || {};
    var did = 'co_' + id;
    var val = esc(data[id] || '');
    if (type === 'select') {
      var options = opts.options.map(function (o) {
        return '<option value="' + o + '"' + (data[id] === o ? ' selected' : '') + '>' + o + '</option>';
      }).join('');
      return '<div class="field field--fill' + (opts.half ? ' field--half' : '') + '">' +
        '<select id="' + did + '" required>' + '<option value="" disabled' + (data[id] ? '' : ' selected') + '></option>' + options + '</select>' +
        '<label class="label--static" for="' + did + '">' + label + '</label></div>';
    }
    return '<div class="field field--fill' + (opts.half ? ' field--half' : '') + '">' +
      '<input type="' + (type || 'text') + '" id="' + did + '" value="' + val + '" placeholder=" " ' +
      (opts.inputmode ? 'inputmode="' + opts.inputmode + '" ' : '') +
      (opts.maxlength ? 'maxlength="' + opts.maxlength + '" ' : '') + '/>' +
      '<label for="' + did + '">' + label + '</label></div>';
  }

  function summary() {
    var lines = C.lines();
    var items = lines.map(function (l) {
      return '<div class="co-sum__item"><div class="co-sum__media"><img src="' + assetSrc(l.product.lead) + '" alt="' + l.product.name + '"/>' +
        '<span class="co-sum__qty">' + l.qty + '</span></div>' +
        '<div class="co-sum__info"><p class="co-sum__name">' + l.product.name + '</p>' +
        '<p class="co-sum__meta">' + l.product.metal + (l.size ? ' · Size ' + l.size : '') + '</p></div>' +
        '<span class="co-sum__price">' + fmt(l.lineTotal) + '</span></div>';
    }).join('');
    var sub = C.subtotal();
    return '<aside class="co-summary">' +
      '<h2 class="co-summary__title">Order Summary</h2>' +
      '<div class="co-sum__items">' + items + '</div>' +
      '<div class="co-summary__row"><span>Subtotal</span><span>' + fmt(sub) + '</span></div>' +
      '<div class="co-summary__row"><span>Shipping</span><span>Complimentary</span></div>' +
      '<div class="co-summary__total"><span>Total</span><span>' + fmt(sub) + '</span></div>' +
      '</aside>';
  }

  function stepper() {
    return '<ol class="co-steps">' + STEPS.map(function (s, i) {
      var cls = i === step ? 'is-active' : (i < step ? 'is-done' : '');
      return '<li class="co-step ' + cls + '"><span class="co-step__n">' + (i < step ? '✓' : (i + 1)) + '</span>' + s + '</li>';
    }).join('<span class="co-steps__sep"></span>') + '</ol>';
  }

  function formForStep() {
    if (step === 0) {
      return '<div class="co-form-grid">' +
        field('firstName', 'First name', 'text', { half: true }) +
        field('lastName', 'Last name', 'text', { half: true }) +
        field('email', 'Email address', 'email') +
        field('phone', 'Phone', 'tel') +
        field('address', 'Address', 'text') +
        field('apartment', 'Apartment, suite (optional)', 'text') +
        field('city', 'City', 'text', { half: true }) +
        field('postal', 'Postal code', 'text', { half: true }) +
        field('state', 'State / Province', 'text', { half: true }) +
        field('country', 'Country', 'select', { half: true, options: ['India', 'United States', 'United Kingdom', 'United Arab Emirates', 'Canada', 'Australia', 'Singapore', 'Other'] }) +
      '</div>';
    }
    if (step === 1) {
      return '<div class="co-pay-note">Demo checkout — no real payment is processed. Enter any test values.</div>' +
        '<div class="co-form-grid">' +
        field('cardName', 'Cardholder name', 'text') +
        field('cardNumber', 'Card number', 'text', { inputmode: 'numeric', maxlength: '19' }) +
        field('cardExp', 'Expiry (MM/YY)', 'text', { half: true, maxlength: '5' }) +
        field('cardCvc', 'CVC', 'text', { half: true, inputmode: 'numeric', maxlength: '4' }) +
      '</div>';
    }
    // review
    return '<div class="co-review">' +
      '<div class="co-review__block"><h3>Contact</h3><p>' + esc(data.email) + '<br>' + esc(data.phone) + '</p>' +
        '<button class="co-edit" data-goto="0">Edit</button></div>' +
      '<div class="co-review__block"><h3>Ship to</h3><p>' + esc(data.firstName) + ' ' + esc(data.lastName) + '<br>' +
        esc(data.address) + (data.apartment ? ', ' + esc(data.apartment) : '') + '<br>' +
        esc(data.city) + ', ' + esc(data.state) + ' ' + esc(data.postal) + '<br>' + esc(data.country) + '</p>' +
        '<button class="co-edit" data-goto="0">Edit</button></div>' +
      '<div class="co-review__block"><h3>Payment</h3><p>Card ending ' + esc((data.cardNumber || '').replace(/\s/g, '').slice(-4)) + '</p>' +
        '<button class="co-edit" data-goto="1">Edit</button></div>' +
      '<label class="co-terms"><input type="checkbox" id="agree" /> I agree to the terms of sale and privacy policy.</label>' +
    '</div>';
  }

  function buttonsForStep() {
    var back = step > 0 ? '<button class="btn btn--ghost" id="coBack">Back</button>' : '<a class="btn btn--ghost" href="' + link('cart') + '">Back to Bag</a>';
    var next = step < 2 ? '<button class="btn btn--gold" id="coNext">Continue</button>' :
      '<button class="btn btn--gold" id="coPlace">Place Order · ' + fmt(C.subtotal()) + '</button>';
    return '<div class="co-actions">' + back + next + '</div>';
  }

  function renderCheckout() {
    root.innerHTML =
      '<div class="checkout__grid">' +
        '<div class="checkout__main">' +
          stepper() +
          '<div class="co-panel">' + formForStep() + '<p class="co-error" id="coError"></p>' + buttonsForStep() + '</div>' +
        '</div>' +
        summary() +
      '</div>';
    bind();
  }

  function save() {
    ['firstName','lastName','email','phone','address','apartment','city','postal','state','country',
     'cardName','cardNumber','cardExp','cardCvc'].forEach(function (id) {
      var e = document.getElementById('co_' + id); if (e) data[id] = e.value.trim();
    });
  }

  function validateStep() {
    var err = '';
    if (step === 0) {
      if (!data.firstName || !data.lastName) err = 'Please enter your full name.';
      else if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(data.email || '')) err = 'Please enter a valid email address.';
      else if (!data.phone) err = 'Please enter a phone number.';
      else if (!data.address || !data.city || !data.postal || !data.state || !data.country) err = 'Please complete your shipping address.';
    } else if (step === 1) {
      var num = (data.cardNumber || '').replace(/\s/g, '');
      if (!data.cardName) err = 'Please enter the cardholder name.';
      else if (!/^\d{12,19}$/.test(num)) err = 'Please enter a valid card number.';
      else if (!/^\d{2}\/\d{2}$/.test(data.cardExp || '')) err = 'Enter expiry as MM/YY.';
      else if (!/^\d{3,4}$/.test(data.cardCvc || '')) err = 'Enter a valid CVC.';
    }
    return err;
  }

  function placeOrder() {
    var agree = document.getElementById('agree');
    if (!agree || !agree.checked) { showError('Please accept the terms of sale to continue.'); return; }
    var n = 'LJ-' + String(Math.floor(100000 + Math.random() * 900000));
    order = { number: n, total: C.subtotal(), email: data.email, name: data.firstName, lines: C.lines() };
    C.clear();
    renderConfirmation();
    window.scrollTo(0, 0);
  }

  function renderConfirmation() {
    var items = order.lines.map(function (l) {
      return '<div class="co-sum__item"><div class="co-sum__media"><img src="' + assetSrc(l.product.lead) + '" alt=""/>' +
        '<span class="co-sum__qty">' + l.qty + '</span></div>' +
        '<div class="co-sum__info"><p class="co-sum__name">' + l.product.name + '</p>' +
        '<p class="co-sum__meta">' + l.product.metal + (l.size ? ' · Size ' + l.size : '') + '</p></div>' +
        '<span class="co-sum__price">' + fmt(l.lineTotal) + '</span></div>';
    }).join('');
    root.innerHTML =
      '<div class="co-confirm">' +
        '<div class="co-confirm__mark">✓</div>' +
        '<p class="eyebrow">Order Confirmed</p>' +
        '<h2 class="co-confirm__title">Thank you, ' + esc(order.name) + '.</h2>' +
        '<p class="co-confirm__lede">Your order <strong>' + order.number + '</strong> is confirmed. A receipt is on its way to ' + esc(order.email) + '. Our atelier will be in touch with crafting updates.</p>' +
        '<div class="co-confirm__card">' + items +
          '<div class="co-summary__total"><span>Total paid</span><span>' + fmt(order.total) + '</span></div>' +
        '</div>' +
        '<a href="' + link('shop') + '" class="btn btn--gold">Continue Shopping</a>' +
      '</div>';
  }

  function showError(msg) { var e = document.getElementById('coError'); if (e) e.textContent = msg; }

  function bind() {
    // format card number in groups of 4
    var cn = document.getElementById('co_cardNumber');
    if (cn) cn.addEventListener('input', function () {
      var v = cn.value.replace(/\D/g, '').slice(0, 19);
      cn.value = v.replace(/(.{4})/g, '$1 ').trim();
    });
    var ce = document.getElementById('co_cardExp');
    if (ce) ce.addEventListener('input', function () {
      var v = ce.value.replace(/\D/g, '').slice(0, 4);
      ce.value = v.length > 2 ? v.slice(0, 2) + '/' + v.slice(2) : v;
    });

    var next = document.getElementById('coNext');
    if (next) next.addEventListener('click', function () {
      save();
      var err = validateStep();
      if (err) { showError(err); return; }
      step++; renderCheckout(); window.scrollTo(0, 0);
    });
    var back = document.getElementById('coBack');
    if (back) back.addEventListener('click', function () { save(); step--; renderCheckout(); window.scrollTo(0, 0); });
    var place = document.getElementById('coPlace');
    if (place) place.addEventListener('click', placeOrder);
    root.querySelectorAll('.co-edit').forEach(function (b) {
      b.addEventListener('click', function () { save(); step = parseInt(b.getAttribute('data-goto'), 10); renderCheckout(); window.scrollTo(0, 0); });
    });
  }

  function start() {
    if (!C.lines().length && !order) {
      root.innerHTML = '<div class="cart-empty">' +
        '<p class="cart-empty__title">Your bag is empty.</p>' +
        '<p class="cart-empty__text">Add a piece before checking out.</p>' +
        '<a href="' + link('shop') + '" class="btn btn--gold">Explore the Collection</a></div>';
      return;
    }
    renderCheckout();
  }

  window.LUNIVAE_CHECKOUT_START = start; // used by the bundle router
  start();
})();
