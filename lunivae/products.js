/* =====================================================================
   LUNIVAE JEWELS — Shared product catalog
   Used by shop.html (listing) and product.html (details)
   ===================================================================== */
window.LUNIVAE_PRODUCTS = [
  {
    id: 'aurelia',
    name: 'The Aurelia Solitaire',
    category: 'solitaire',
    categoryLabel: 'Solitaire',
    price: 4200,
    metal: '18K Yellow Gold',
    stone: 'Lab-Grown Diamond',
    carat: '1.50 ct',
    cut: 'Round Brilliant',
    color: 'E',
    clarity: 'VVS2',
    cert: 'IGI Certified',
    lead: 'hero-solitaire.jpg',
    images: ['hero-solitaire.jpg', 'ring-top.jpg', 'ring-angle.jpg', 'ring-side.jpg', 'model-hand.jpg'],
    blurb: 'Our signature round brilliant, cradled in a hand-finished four-prong setting.',
    description: 'The Aurelia is the piece the house is known for — a single round brilliant of exceptional fire, raised on a slender band so the light is never interrupted. Each stone is hand-selected and set by our master jewelers in Surat, then finished to a mirror polish. A quietly perfect solitaire, made to be worn for a lifetime.'
  },
  {
    id: 'celeste',
    name: 'Celeste Round Brilliant',
    category: 'solitaire',
    categoryLabel: 'Solitaire',
    price: 3600,
    metal: '18K Yellow Gold',
    stone: 'Lab-Grown Diamond',
    carat: '1.20 ct',
    cut: 'Round Brilliant',
    color: 'F',
    clarity: 'VS1',
    cert: 'IGI Certified',
    lead: 'ring-top.jpg',
    images: ['ring-top.jpg', 'ring-angle.jpg', 'ring-side.jpg'],
    blurb: 'A classic hidden-halo solitaire with a delicate pavé shoulder.',
    description: 'Celeste pairs a bright round brilliant with a whisper of pavé along the shoulders — enough to catch the light, never enough to distract. A timeless everyday solitaire that moves effortlessly from morning to occasion.'
  },
  {
    id: 'seraphine',
    name: 'Seraphine Pavé',
    category: 'pave',
    categoryLabel: 'Pavé',
    price: 4800,
    metal: '18K Yellow Gold',
    stone: 'Lab-Grown Diamond',
    carat: '1.60 ct',
    cut: 'Round Brilliant',
    color: 'E',
    clarity: 'VVS1',
    cert: 'IGI Certified',
    lead: 'ring-angle.jpg',
    images: ['ring-angle.jpg', 'ring-side.jpg', 'ring-top.jpg'],
    blurb: 'French micro-pavé shoulders framing a luminous centre stone.',
    description: 'Seraphine surrounds its centre stone with rows of hand-set micro-pavé, each tiny diamond individually beaded by hand. The effect is a band that appears to be made entirely of light — an heirloom silhouette for the promise of a lifetime.'
  },
  {
    id: 'isolde',
    name: 'Isolde Pavé Band',
    category: 'pave',
    categoryLabel: 'Pavé',
    price: 3900,
    metal: '18K Yellow Gold',
    stone: 'Lab-Grown Diamond',
    carat: '1.30 ct',
    cut: 'Round Brilliant',
    color: 'F',
    clarity: 'VS2',
    cert: 'IGI Certified',
    lead: 'ring-side.jpg',
    images: ['ring-side.jpg', 'ring-top.jpg', 'ring-angle.jpg'],
    blurb: 'A refined profile with pavé carried all the way around the band.',
    description: 'Isolde is designed to be beautiful from every angle — the pavé continues around the full circumference of the band, so there is no wrong way to wear it. A modern classic with an unmistakably regal profile.'
  },
  {
    id: 'lumiere',
    name: 'Lumière Bridal Ring',
    category: 'bridal',
    categoryLabel: 'Bridal',
    price: 5400,
    metal: '18K Yellow Gold',
    stone: 'Lab-Grown Diamond',
    carat: '1.80 ct',
    cut: 'Round Brilliant',
    color: 'D',
    clarity: 'VVS2',
    cert: 'IGI Certified',
    lead: 'model-hand.jpg',
    images: ['model-hand.jpg', 'hero-solitaire.jpg', 'ring-angle.jpg'],
    blurb: 'The bridal centrepiece — a flawless D-colour brilliant, made to be seen.',
    description: 'Lumière is our bridal statement: a rare D-colour brilliant of nearly two carats, set high to catch every movement of light. Designed to be the piece a story is told around — and to be photographed for the rest of your life.'
  },
  {
    id: 'regina',
    name: 'Regina Heritage Solitaire',
    category: 'heritage',
    categoryLabel: 'Heritage',
    price: 6200,
    metal: '18K Yellow Gold',
    stone: 'Natural Diamond',
    carat: '2.00 ct',
    cut: 'Round Brilliant',
    color: 'E',
    clarity: 'VVS1',
    cert: 'GIA Certified',
    lead: 'hero-solitaire.jpg',
    images: ['hero-solitaire.jpg', 'model-hand.jpg', 'ring-top.jpg'],
    blurb: 'A two-carat natural brilliant — our most regal commission.',
    description: 'Regina is the fullest expression of the house: a two-carat natural diamond, GIA-certified, set in warm yellow gold with royal restraint. Commissioned one at a time and kept for generations — jewelry in the truest heritage sense.'
  }
];

/* Helpers shared by both pages */
window.LUNIVAE = {
  formatPrice: function (n) {
    return '$' + n.toLocaleString('en-US');
  },
  byId: function (id) {
    return window.LUNIVAE_PRODUCTS.filter(function (p) { return p.id === id; })[0] || null;
  }
};
