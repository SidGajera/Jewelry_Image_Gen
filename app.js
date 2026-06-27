/* ==========================================================================
   AURA FINE JEWELRY - FRONTEND STATE & LOGIC CONTROLLER
   ========================================================================== */

// 1. Database of Mock IGI Certificates (Trust Building Factor)
const IGI_DATABASE = {
    "IGI-582940294": {
        date: "April 12, 2026",
        number: "LG582940294",
        description: "LABORATORY GROWN DIAMOND",
        shape: "ROUND BRILLIANT",
        measurements: "7.34 x 7.38 x 4.52 mm",
        carat: "1.50 Carat",
        color: "D (Colorless)",
        clarity: "VVS2 (Very Very Slightly Included)",
        cut: "EXCELLENT",
        polish: "EXCELLENT",
        symmetry: "EXCELLENT",
        fluorescence: "NONE",
        inscription: "LABGROWN IGI LG582940294"
    },
    "IGI-601938592": {
        date: "May 29, 2026",
        number: "LG601938592",
        description: "LABORATORY GROWN DIAMOND",
        shape: "OVAL CUT",
        measurements: "9.84 x 7.02 x 4.38 mm",
        carat: "2.00 Carat",
        color: "E (Colorless)",
        clarity: "VS1 (Very Slightly Included)",
        cut: "EXCELLENT (Ideal)",
        polish: "EXCELLENT",
        symmetry: "EXCELLENT",
        fluorescence: "NONE",
        inscription: "LABGROWN IGI LG601938592"
    },
    "IGI-482049102": {
        date: "February 04, 2026",
        number: "GT482049102",
        description: "NATURAL MINED DIAMOND",
        shape: "EMERALD CUT",
        measurements: "8.92 x 6.22 x 4.10 mm",
        carat: "2.50 Carat",
        color: "F (Colorless)",
        clarity: "VVS1 (Very Very Slightly Included)",
        cut: "EXCELLENT",
        polish: "EXCELLENT",
        symmetry: "VERY GOOD",
        fluorescence: "FAINT",
        inscription: "AURA INSCRIBED GT482049102"
    }
};

// 2. SVG Path definitions for diamond shapes
const DIAMOND_SHAPES_POINTS = {
    round: {
        points: "0,-35 25,-12 18,15 -18,15 -25,-12",
        facets: [
            { x1: 0, y1: -35, x2: 0, y2: 15 },
            { x1: -25, y1: -12, x2: 25, y2: -12 },
            { x1: 0, y1: -35, x2: -18, y2: 15 },
            { x1: 0, y1: -35, x2: 18, y2: 15 },
            { x1: -25, y1: -12, x2: 0, y2: 0 },
            { x1: 25, y1: -12, x2: 0, y2: 0 },
            { x1: -18, y1: 15, x2: 0, y2: 0 },
            { x1: 18, y1: 15, x2: 0, y2: 0 }
        ]
    },
    oval: {
        points: "0,-42 22,-20 16,18 -16,18 -22,-20",
        facets: [
            { x1: 0, y1: -42, x2: 0, y2: 18 },
            { x1: -22, y1: -20, x2: 22, y2: -20 },
            { x1: 0, y1: -42, x2: -16, y2: 18 },
            { x1: 0, y1: -42, x2: 16, y2: 18 },
            { x1: -22, y1: -20, x2: 0, y2: -2 },
            { x1: 22, y1: -20, x2: 0, y2: -2 },
            { x1: -16, y1: 18, x2: 0, y2: -2 },
            { x1: 16, y1: 18, x2: 0, y2: -2 }
        ]
    },
    emerald: {
        points: "-18,-32 18,-32 25,-18 25,18 18,32 -18,32 -25,18 -25,-18",
        facets: [
            // Outer step facets
            { x1: -18, y1: -32, x2: -13, y2: -25 },
            { x1: 18, y1: -32, x2: 13, y2: -25 },
            { x1: 25, y1: -18, x2: 18, y2: -13 },
            { x1: 25, y1: 18, x2: 18, y2: 13 },
            { x1: 18, y1: 32, x2: 13, y2: 25 },
            { x1: -18, y1: 32, x2: -13, y2: 25 },
            { x1: -25, y1: 18, x2: -18, y2: 13 },
            { x1: -25, y1: -18, x2: -18, y2: -13 },
            // Inner step rectangles
            { x1: -13, y1: -25, x2: 13, y2: -25 },
            { x1: 13, y1: -25, x2: 18, y2: -13 },
            { x1: 18, y1: -13, x2: 18, y2: 13 },
            { x1: 18, y1: 13, x2: 13, y2: 25 },
            { x1: 13, y1: 25, x2: -13, y2: 25 },
            { x1: -13, y1: 25, x2: -18, y2: 13 },
            { x1: -18, y1: 13, x2: -18, y2: -13 },
            { x1: -18, y1: -13, x2: -13, y2: -25 }
        ]
    },
    princess: {
        points: "-25,-25 25,-25 25,25 -25,25",
        facets: [
            { x1: -25, y1: -25, x2: 25, y2: 25 },
            { x1: 25, y1: -25, x2: -25, y2: 25 },
            { x1: 0, y1: -25, x2: 0, y2: 25 },
            { x1: -25, y1: 0, x2: 25, y2: 0 },
            { x1: 0, y1: 0, x2: -25, y2: -25 },
            { x1: 0, y1: 0, x2: 25, y2: -25 },
            { x1: 0, y1: 0, x2: 25, y2: 25 },
            { x1: 0, y1: 0, x2: -25, y2: 25 }
        ]
    },
    pear: {
        points: "0,-42 22,-12 16,22 -16,22 -22,-12",
        facets: [
            { x1: 0, y1: -42, x2: 0, y2: 22 },
            { x1: -22, y1: -12, x2: 22, y2: -12 },
            { x1: 0, y1: -42, x2: -16, y2: 22 },
            { x1: 0, y1: -42, x2: 16, y2: 22 },
            { x1: -22, y1: -12, x2: 0, y2: 3 },
            { x1: 22, y1: -12, x2: 0, y2: 3 },
            { x1: -16, y1: 22, x2: 0, y2: 3 },
            { x1: 16, y1: 22, x2: 0, y2: 3 }
        ]
    }
};

// 3. Application State
const state = {
    currentRoute: "home",
    cart: [],
    customizer: {
        template: "solitaire",
        metalPurity: "14k",
        metalColor: "yellow",
        stoneOrigin: "lab",
        stoneShape: "round",
        caratWeight: 1.5,
        ringSize: "7",
        engraving: ""
    }
};

// 4. Initializer
document.addEventListener("DOMContentLoaded", () => {
    // Check local storage for existing cart data
    const savedCart = localStorage.getItem("aura_cart");
    if (savedCart) {
        try {
            state.cart = JSON.parse(savedCart);
            updateCartBadge();
        } catch(e) {
            console.error("Could not parse saved cart data", e);
        }
    }

    // Initialize SPA routing
    window.addEventListener("hashchange", handleRoute);
    handleRoute(); // Execute once to parse landing route

    // Initialize Event Listeners
    setupNavListeners();
    setupCustomizerControls();
    setupCartListeners();
    setupLookupListeners();
    setupModalListeners();
    
    // Initial Customizer rendering calculation
    updateCustomizerUI();
});

// 5. Hash Router
function handleRoute() {
    const rawHash = window.location.hash || "#/";
    let route = "home";
    let params = new URLSearchParams();

    // Check query params in hash (e.g. #/customizer?template=halo)
    if (rawHash.includes("?")) {
        const parts = rawHash.split("?");
        route = parts[0].replace("#/", "") || "home";
        params = new URLSearchParams(parts[1]);
    } else {
        route = rawHash.replace("#/", "") || "home";
    }
    
    // Clean route formatting
    if (route.endsWith("/")) route = route.slice(0, -1);
    if (!route) route = "home";

    state.currentRoute = route;

    // Display proper SPA section
    document.querySelectorAll(".spa-view").forEach(section => {
        section.classList.add("hidden");
    });
    
    const activeSection = document.getElementById(`view-${route}`);
    if (activeSection) {
        activeSection.classList.remove("hidden");
    } else {
        // Fallback to home if route not found
        document.getElementById("view-home").classList.remove("hidden");
        state.currentRoute = "home";
    }

    // Update active nav highlights
    document.querySelectorAll(".nav-item, .mobile-nav-item").forEach(item => {
        if (item.getAttribute("data-route") === state.currentRoute) {
            item.classList.add("active");
        } else {
            item.classList.remove("active");
        }
    });

    // Close mobile menu on navigate
    document.querySelector(".mobile-menu").classList.add("hidden");

    // Route-specific hook: URL Parameter loading for customizer templates
    if (state.currentRoute === "customizer") {
        const templateParam = params.get("template");
        if (templateParam && ["solitaire", "halo", "pave"].includes(templateParam)) {
            state.customizer.template = templateParam;
            // Sync the HTML radio checks
            const radio = document.querySelector(`input[name="setting-template"][value="${templateParam}"]`);
            if (radio) radio.checked = true;
        }
        updateCustomizerUI();
    }
    
    // Trigger Lucide SVG replacements
    if (window.lucide) {
        lucide.createIcons();
    }
    
    // Scroll window to top
    window.scrollTo(0, 0);
}

// 6. Navigation Event Listeners
function setupNavListeners() {
    // Mobile menu toggle
    const toggleBtn = document.querySelector(".mobile-menu-toggle");
    const mobileMenu = document.querySelector(".mobile-menu");
    
    toggleBtn.addEventListener("click", () => {
        mobileMenu.classList.toggle("hidden");
        // Swap icon between hamburger and cross
        const icon = toggleBtn.querySelector("i");
        if (mobileMenu.classList.contains("hidden")) {
            icon.setAttribute("data-lucide", "menu");
        } else {
            icon.setAttribute("data-lucide", "x");
        }
        lucide.createIcons();
    });
}

// 7. Customizer Engine & Price Calculator
function setupCustomizerControls() {
    // Detect metal template changes
    document.querySelectorAll('input[name="setting-template"]').forEach(elem => {
        elem.addEventListener("change", (e) => {
            state.customizer.template = e.target.value;
            updateCustomizerUI(true); // animate sparkle
        });
    });

    // Detect gold purity selection
    document.querySelectorAll('input[name="metal-purity"]').forEach(elem => {
        elem.addEventListener("change", (e) => {
            state.customizer.metalPurity = e.target.value;
            updateCustomizerUI(true);
        });
    });

    // Detect gold color selection
    document.querySelectorAll('input[name="metal-color"]').forEach(elem => {
        elem.addEventListener("change", (e) => {
            state.customizer.metalColor = e.target.value;
            updateCustomizerUI();
        });
    });

    // Detect diamond origin selection
    document.querySelectorAll('input[name="stone-origin"]').forEach(elem => {
        elem.addEventListener("change", (e) => {
            state.customizer.stoneOrigin = e.target.value;
            updateCustomizerUI(true);
        });
    });

    // Detect diamond shape selection
    document.querySelectorAll('input[name="stone-shape"]').forEach(elem => {
        elem.addEventListener("change", (e) => {
            state.customizer.stoneShape = e.target.value;
            updateCustomizerUI(true);
        });
    });

    // Detect carat range slider
    const caratSlider = document.getElementById("carat-slider");
    const caratValText = document.getElementById("carat-value-text");
    caratSlider.addEventListener("input", (e) => {
        const val = parseFloat(e.target.value).toFixed(1) + " Ct";
        caratValText.innerText = val;
        state.customizer.caratWeight = parseFloat(e.target.value);
        updateCustomizerUI();
    });

    // Detect ring size dropdown
    document.getElementById("ring-size-select").addEventListener("change", (e) => {
        state.customizer.ringSize = e.target.value;
    });

    // Detect engraving text input
    const engInput = document.getElementById("engraving-input");
    const engCount = document.getElementById("engraving-count-text");
    engInput.addEventListener("input", (e) => {
        const val = e.target.value;
        state.customizer.engraving = val;
        engCount.innerText = `${val.length} / 20`;
        
        // Update live preview engraving overlay text
        const textOverlay = document.getElementById("preview-engraving");
        if (textOverlay) {
            textOverlay.textContent = val ? `"${val.toUpperCase()}"` : "";
        }
    });

    // "Add Custom Creation to Bag" Action
    document.getElementById("btn-add-to-cart").addEventListener("click", () => {
        // Package copy of customizer parameters
        const customizedItem = {
            id: Date.now() + Math.random().toString(36).substr(2, 5),
            template: state.customizer.template,
            metalPurity: state.customizer.metalPurity,
            metalColor: state.customizer.metalColor,
            stoneOrigin: state.customizer.stoneOrigin,
            stoneShape: state.customizer.stoneShape,
            caratWeight: state.customizer.caratWeight,
            ringSize: state.customizer.ringSize,
            engraving: state.customizer.engraving,
            price: calculatePricing(state.customizer)
        };

        state.cart.push(customizedItem);
        saveCartToLocalStorage();
        updateCartBadge();
        renderCartDrawerItems();
        openCartDrawer();
    });
}

// 8. Live State Synchronizer & Vector Morphing
function updateCustomizerUI(animateSparkle = false) {
    const config = state.customizer;

    // 1. Calculate pricing
    const itemPrice = calculatePricing(config);
    const formattedPrice = `$${itemPrice.toLocaleString()}`;
    const monthlyAffirm = `$${Math.round(itemPrice / 36)}`;
    
    document.getElementById("calculated-price").innerText = formattedPrice;
    document.getElementById("financing-price").innerText = monthlyAffirm;

    // 2. Render Text Specs summary panel below canvas
    const displayMetal = `${config.metalPurity.toUpperCase()} ${capitalize(config.metalColor)} Gold (Solid)`;
    const displayStone = `${config.caratWeight.toFixed(2)} Ct ${capitalize(config.stoneShape)} (${config.stoneOrigin === "lab" ? "Lab Grown" : "Natural Mined"})`;
    
    document.getElementById("spec-metal-text").innerText = displayMetal;
    document.getElementById("spec-stone-text").innerText = displayStone;

    // 3. Update Dynamic SVG elements
    const svg = document.getElementById("customizer-svg");
    if (!svg) return;

    // Get color gradients based on metal choice
    const metalGradUrl = `url(#${config.metalColor}-gold-grad)`;
    
    // Update shank stroke gradient and prong colors
    document.getElementById("ring-shank").setAttribute("stroke", metalGradUrl);
    document.getElementById("prong-base").setAttribute("fill", metalGradUrl);
    document.getElementById("prong-left").setAttribute("fill", metalGradUrl);
    document.getElementById("prong-right").setAttribute("fill", metalGradUrl);
    
    const haloBacking = document.getElementById("halo-ring-backing");
    if (haloBacking) haloBacking.setAttribute("stroke", metalGradUrl);

    // Template template options (halo, pave, solitaire)
    const paveStones = document.getElementById("pave-stones");
    const haloCircle = document.getElementById("halo-circle");

    if (config.template === "pave") {
        paveStones.classList.remove("hidden");
    } else {
        paveStones.classList.add("hidden");
    }

    if (config.template === "halo") {
        haloCircle.classList.remove("hidden");
        haloBacking.classList.remove("hidden");
    } else {
        haloCircle.classList.add("hidden");
        haloBacking.classList.add("hidden");
    }

    // Diamond Gem Shape polygon coordinates swapping
    const gemPoints = DIAMOND_SHAPES_POINTS[config.stoneShape];
    const gemShapeElement = document.getElementById("diamond-shape");
    const gemFacetsElement = document.getElementById("diamond-facets");

    if (gemPoints && gemShapeElement) {
        gemShapeElement.setAttribute("points", gemPoints.points);
        
        // Clear old facets & draw new ones to match the shape
        gemFacetsElement.innerHTML = "";
        gemPoints.facets.forEach(f => {
            const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
            line.setAttribute("x1", f.x1);
            line.setAttribute("y1", f.y1);
            line.setAttribute("x2", f.x2);
            line.setAttribute("y2", f.y2);
            gemFacetsElement.appendChild(line);
        });
    }

    // Carat Scale calculation (ranges 0.5 to 5.0)
    // Map carat range to linear scale multiplier (0.6x for 0.5ct up to 1.7x for 5.0ct)
    const scale = 0.6 + (config.caratWeight - 0.5) * (1.1 / 4.5);
    const gemGroup = document.getElementById("diamond-gem-group");
    if (gemGroup) {
        gemGroup.setAttribute("transform", `translate(200, 115) scale(${scale})`);
    }

    // Prong layout adjusts outward as scale expands so prongs grip diamond
    // Prong center: Y is fixed, X spreads wider
    const prongBaseWidth = 22 * scale; // prong anchor spread calculation
    document.getElementById("prong-left").setAttribute("cx", (200 - prongBaseWidth).toString());
    document.getElementById("prong-right").setAttribute("cx", (200 + prongBaseWidth).toString());

    // Sparkle animation effect trigger if specified
    if (animateSparkle && gemShapeElement) {
        gemShapeElement.classList.remove("sparkle-active");
        void gemShapeElement.offsetWidth; // trigger reflow to restart animation
        gemShapeElement.classList.add("sparkle-active");
        
        const glowBg = document.getElementById("sparkle-glow-bg");
        if (glowBg) {
            glowBg.style.opacity = "0.7";
            setTimeout(() => { glowBg.style.opacity = "0.3"; }, 800);
        }
    }
}

// Pricing formula engine based on jewelry specs (US buying psychology)
function calculatePricing(config) {
    let price = 0;

    // 1. Base setting style cost
    if (config.template === "solitaire") price += 950;
    else if (config.template === "halo") price += 1380;
    else if (config.template === "pave") price += 1550;

    // 2. Metal Gold purity premium
    if (config.metalPurity === "14k") price += 250;
    else if (config.metalPurity === "18k") price += 600;

    // 3. Diamond carat calculation (Exponential factor: larger carats cost more per carat)
    const baseCaratRate = config.stoneOrigin === "lab" ? 1200 : 2800;
    const caratMultiplier = Math.pow(config.caratWeight, 1.25); // exponential scaling for larger stones
    price += Math.round(caratMultiplier * baseCaratRate);

    return price;
}

// 9. Shopping Cart Operations
function setupCartListeners() {
    // Toggle Cart open
    document.querySelector(".cart-toggle-btn").addEventListener("click", openCartDrawer);

    // Toggle Cart close buttons
    document.querySelectorAll(".close-cart-btn, .cart-overlay-backdrop, .close-cart-btn-link").forEach(btn => {
        btn.addEventListener("click", closeCartDrawer);
    });

    // "Proceed to secure checkout" button click
    document.getElementById("btn-begin-checkout").addEventListener("click", () => {
        if (state.cart.length === 0) return;
        closeCartDrawer();
        openCheckoutModal();
    });

    // Handle payment selection change (credit vs financing)
    document.querySelectorAll('input[name="payment-method"]').forEach(radio => {
        radio.addEventListener("change", (e) => {
            const val = e.target.value;
            const cardFields = document.getElementById("credit-card-fields");
            const affirmFields = document.getElementById("affirm-fields");
            
            if (val === "credit") {
                cardFields.classList.remove("hidden");
                affirmFields.classList.add("hidden");
                // Remove required flags for inputs inside hidden areas
                cardFields.querySelectorAll("input").forEach(i => i.required = true);
            } else {
                cardFields.classList.add("hidden");
                affirmFields.classList.remove("hidden");
                cardFields.querySelectorAll("input").forEach(i => i.required = false);
            }
        });
    });

    // Mock checkout form submission
    document.getElementById("mock-checkout-form").addEventListener("submit", (e) => {
        e.preventDefault();
        
        // Random order reference number
        const orderRef = "AU-" + Math.floor(100000 + Math.random() * 900000);
        document.getElementById("success-ref-num").innerText = orderRef;
        
        // Clean cart state
        state.cart = [];
        saveCartToLocalStorage();
        updateCartBadge();
        renderCartDrawerItems();
        
        // Hide checkout modal and display success screen
        closeCheckoutModal();
        document.getElementById("success-modal").classList.remove("hidden");
    });

    // Close success order modal
    document.getElementById("btn-success-close").addEventListener("click", () => {
        document.getElementById("success-modal").classList.add("hidden");
        window.location.hash = "#/customizer";
    });
}

function openCartDrawer() {
    document.querySelector(".cart-drawer-container").classList.remove("hidden");
    document.querySelector(".cart-overlay-backdrop").classList.remove("hidden");
    document.body.style.overflow = "hidden"; // block background scroll
}

function closeCartDrawer() {
    document.querySelector(".cart-drawer-container").classList.add("hidden");
    document.querySelector(".cart-overlay-backdrop").classList.add("hidden");
    document.body.style.overflow = "";
}

function updateCartBadge() {
    const counts = state.cart.length;
    const badge = document.querySelector(".cart-badge");
    badge.innerText = counts;
    document.getElementById("cart-drawer-count").innerText = `${counts} ${counts === 1 ? 'item' : 'items'}`;
}

function saveCartToLocalStorage() {
    localStorage.setItem("aura_cart", JSON.stringify(state.cart));
}

function renderCartDrawerItems() {
    const listContainer = document.getElementById("cart-items-list");
    const subtotalText = document.getElementById("cart-subtotal");
    const totalText = document.getElementById("cart-total");
    
    if (state.cart.length === 0) {
        listContainer.innerHTML = `
            <div class="empty-cart-state">
                <i data-lucide="shopping-bag" class="empty-cart-icon"></i>
                <p>Your bag is currently empty.</p>
                <a href="#/customizer" class="btn btn-secondary close-cart-btn-link">Explore Custom Workshop</a>
            </div>
        `;
        subtotalText.innerText = "$0";
        totalText.innerText = "$0";
        
        // Add link hooks to newly injected items
        listContainer.querySelector(".close-cart-btn-link").addEventListener("click", closeCartDrawer);
        
        if (window.lucide) lucide.createIcons();
        return;
    }

    let subtotal = 0;
    listContainer.innerHTML = "";

    state.cart.forEach(item => {
        subtotal += item.price;
        
        const itemCard = document.createElement("div");
        itemCard.className = "cart-item";
        
        const specSummaryHtml = `
            <li>Setting: ${capitalize(item.template)} Setting</li>
            <li>Metal: Solid ${item.metalPurity.toUpperCase()} ${capitalize(item.metalColor)} Gold</li>
            <li>Stone: ${item.caratWeight.toFixed(2)} Ct ${capitalize(item.stoneShape)} (${item.stoneOrigin === 'lab' ? 'Lab Grown' : 'Natural'})</li>
            <li>Ring Size: US ${item.ringSize}</li>
        `;
        
        const engravingHtml = item.engraving 
            ? `<div class="cart-item-engraving-badge"><i data-lucide="pen-tool"></i> Engraving: "${item.engraving.toUpperCase()}"</div>` 
            : "";

        // Dynamic Ring icon color overlay on mini thumbnail
        const thumbColor = item.metalColor === "yellow" ? "#E6C575" : (item.metalColor === "rose" ? "#F3A38E" : "#E5E7EB");

        itemCard.innerHTML = `
            <div class="cart-item-preview-frame">
                <svg viewBox="0 0 100 100" width="55" height="55">
                    <circle cx="50" cy="58" r="28" stroke="${thumbColor}" stroke-width="4" fill="none" />
                    <!-- tiny diamond top -->
                    <polygon points="50,15 62,25 50,32 38,25" fill="#E0F2FE" stroke="#38BDF8" stroke-width="1"/>
                </svg>
            </div>
            
            <div class="cart-item-info">
                <div class="cart-item-header">
                    <div>
                        <h4 class="cart-item-title">Custom Ring</h4>
                        <ul class="cart-item-specs-summary">${specSummaryHtml}</ul>
                        ${engravingHtml}
                    </div>
                    <span class="cart-item-price">$${item.price.toLocaleString()}</span>
                </div>
                
                <div class="cart-item-actions">
                    <button class="btn-remove-item" data-id="${item.id}">
                        <i data-lucide="trash-2"></i> Remove Design
                    </button>
                </div>
            </div>
        `;
        
        // Remove hook
        itemCard.querySelector(".btn-remove-item").addEventListener("click", (e) => {
            const idToRemove = e.currentTarget.getAttribute("data-id");
            state.cart = state.cart.filter(c => c.id !== idToRemove);
            saveCartToLocalStorage();
            updateCartBadge();
            renderCartDrawerItems();
        });

        listContainer.appendChild(itemCard);
    });

    subtotalText.innerText = `$${subtotal.toLocaleString()}`;
    totalText.innerText = `$${subtotal.toLocaleString()}`;
    
    if (window.lucide) lucide.createIcons();
}

// 10. Checkout Modal Display
function openCheckoutModal() {
    const modal = document.getElementById("checkout-modal");
    modal.classList.remove("hidden");
    
    // Render list items in checkout pane
    const checkoutSummaryList = document.getElementById("checkout-summary-items");
    let total = 0;
    
    checkoutSummaryList.innerHTML = "";
    
    state.cart.forEach(item => {
        total += item.price;
        const itemRow = document.createElement("div");
        itemRow.className = "checkout-summary-item";
        itemRow.innerHTML = `
            <div>
                <span class="chk-item-name">Bespoke Diamond Ring</span>
                <span class="chk-item-specs">${capitalize(item.template)} | Solid ${item.metalPurity.toUpperCase()} Gold | ${item.caratWeight.toFixed(2)}ct ${capitalize(item.stoneShape)}</span>
            </div>
            <span class="chk-item-price">$${item.price.toLocaleString()}</span>
        `;
        checkoutSummaryList.appendChild(itemRow);
    });

    document.getElementById("checkout-subtotal").innerText = `$${total.toLocaleString()}`;
    document.getElementById("checkout-total").innerText = `$${total.toLocaleString()}`;
    
    document.body.style.overflow = "hidden";
}

function closeCheckoutModal() {
    document.getElementById("checkout-modal").classList.add("hidden");
    document.body.style.overflow = "";
}

// 11. IGI Certificate Authentication Module
function setupLookupListeners() {
    const input = document.getElementById("cert-number-input");
    const lookupBtn = document.getElementById("btn-lookup-cert");
    const certCard = document.getElementById("cert-display-card");
    const errorBox = document.getElementById("cert-error-box");
    
    lookupBtn.addEventListener("click", () => {
        const query = input.value.trim();
        const record = IGI_DATABASE[query];
        
        if (record) {
            // Fill matching specifications in HTML certificate elements
            document.getElementById("cert-date-val").innerText = record.date;
            document.getElementById("cert-num-val").innerText = record.number;
            document.getElementById("cert-desc-val").innerText = record.description;
            document.getElementById("cert-shape-val").innerText = record.shape;
            document.getElementById("cert-measure-val").innerText = record.measurements;
            document.getElementById("cert-carat-val").innerText = record.carat;
            document.getElementById("cert-color-val").innerText = record.color;
            document.getElementById("cert-clarity-val").innerText = record.clarity;
            document.getElementById("cert-cut-val").innerText = record.cut;
            document.getElementById("cert-polish-val").innerText = record.polish;
            document.getElementById("cert-symm-val").innerText = record.symmetry;
            document.getElementById("cert-fluor-val").innerText = record.fluorescence;
            document.getElementById("cert-inscr-val").innerText = record.inscription;
            
            // Show certificate card, hide error box
            certCard.classList.remove("hidden");
            errorBox.classList.add("hidden");
            
            // Auto scroll certificate replica into view
            certCard.scrollIntoView({ behavior: "smooth", block: "nearest" });
        } else {
            // Show error box, hide certificate card
            errorBox.classList.remove("hidden");
            certCard.classList.add("hidden");
        }
    });
}

// 12. Modal Utility Triggers
function setupModalListeners() {
    // Open info modals in Customizer
    document.querySelectorAll("[data-modal]").forEach(btn => {
        btn.addEventListener("click", () => {
            const modalId = btn.getAttribute("data-modal");
            const targetModal = document.getElementById(modalId);
            if (targetModal) {
                targetModal.classList.remove("hidden");
                document.body.style.overflow = "hidden";
            }
        });
    });

    // Close info modals & checkout modal
    document.querySelectorAll(".close-modal-btn, .modal-overlay, #btn-close-checkout").forEach(btn => {
        btn.addEventListener("click", (e) => {
            // Close only if click is directly on container overlay backdrop or on designated close button
            if (e.target === e.currentTarget || e.currentTarget.classList.contains("close-modal-btn") || e.currentTarget.id === "btn-close-checkout") {
                document.querySelectorAll(".modal-overlay").forEach(m => m.classList.add("hidden"));
                document.body.style.overflow = "";
            }
        });
    });
    
    // Prevent modal content clicks from bubbled closing
    document.querySelectorAll(".modal-content").forEach(content => {
        content.addEventListener("click", (e) => {
            e.stopPropagation();
        });
    });
}

// 13. Helper Utility Functions
function capitalize(str) {
    if (!str) return "";
    return str.charAt(0).toUpperCase() + str.slice(1);
}
