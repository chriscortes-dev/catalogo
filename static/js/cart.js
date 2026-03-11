/* -------------------------
Cart UI Behaviour
------------------------- */

window.toggleCart = function () {

    const cart = document.getElementById("cartSidebar");
    const overlay = document.getElementById("cartOverlay");

    if (!cart || !overlay) return;

    const isOpen = !cart.classList.contains("translate-x-full");

    if (isOpen) {

        cart.classList.add("translate-x-full");
        overlay.classList.add("opacity-0");
        overlay.classList.add("pointer-events-none");

    } else {

        cart.classList.remove("translate-x-full");
        overlay.classList.remove("opacity-0");
        overlay.classList.remove("pointer-events-none");

    }
};

/* cerrar tocando overlay */

document.addEventListener("DOMContentLoaded", () => {

    const overlay = document.getElementById("cartOverlay");

    overlay?.addEventListener("click", toggleCart);

});

const CART_KEY = "catalogo_cart";

/* -------------------------
Storage
------------------------- */

function getCart() {
    return JSON.parse(localStorage.getItem(CART_KEY)) || [];
}

function saveCart(cart) {
    localStorage.setItem(CART_KEY, JSON.stringify(cart));
}

/* -------------------------
Render
------------------------- */

function renderCartSidebar() {

    const container = document.getElementById("cartItems");

    if (!container) return;

    const cart = getCart();

    container.innerHTML = "";

    if (cart.length === 0) {
        container.innerHTML = `
            <p class="text-gray-400 text-sm">
                El carrito está vacío
            </p>
        `;
        return;
    }

    cart.forEach(item => {

        const template = document.getElementById("cartItemTemplate");

        if (!template) return;

        const clone = template.content.cloneNode(true);

        clone.querySelector("[data-cart-product]")
            .innerText = item.productName;

        clone.querySelector("[data-cart-variant]")
            .innerText = item.variantName;

        clone.querySelector("[data-cart-qty]")
            .innerText = item.quantity;

        clone.querySelector("[data-cart-increase]")
            .addEventListener("click", () =>
                updateCartQty(item.variantId, 1)
            );

        clone.querySelector("[data-cart-decrease]")
            .addEventListener("click", () =>
                updateCartQty(item.variantId, -1, item.min)
            );

        clone.querySelector("[data-cart-remove]")
            .addEventListener("click", () =>
                removeFromCart(item.variantId)
            );

        container.appendChild(clone);

    });
}

/* -------------------------
Quantity
------------------------- */

function updateCartQty(variantId, delta, min = 1) {

    let cart = getCart();

    let item = cart.find(x => x.variantId === variantId);

    if (!item) return;

    let newQty = item.quantity + delta;

    if (newQty < min) {
        item.quantity = min;
    } else {
        item.quantity = newQty;
    }

    saveCart(cart);
    renderCartSidebar();
}

/* -------------------------
Remove
------------------------- */

function removeFromCart(variantId) {

    let cart = getCart();

    cart = cart.filter(x => x.variantId !== variantId);

    saveCart(cart);
    renderCartSidebar();
}

/* -------------------------
WhatsApp Quote
------------------------- */

function sendWhatsAppQuote() {

    const cart = getCart();

    if (!cart.length) {
        alert("El carrito está vacío");
        return;
    }

    let message = `Hola, quiero cotizar productos de ${window.STORE_CONTEXT.name}:%0A%0A`;

    cart.forEach(item => {
        message += `• ${item.productName} (${item.variantName}) - Cantidad: ${item.quantity}%0A`;
    });

    const phone = window.STORE_CONTEXT?.whatsapp;

    const url = `https://wa.me/${phone}?text=${message}`;

    window.open(url, "_blank");
}

/* -------------------------
Add product
------------------------- */

document.addEventListener("DOMContentLoaded", () => {

    const addBtn = document.getElementById("addToCartBtn");
    const radios = document.querySelectorAll(".variant-radio");

    let selectedVariant = null;

    radios.forEach(radio => {

        radio.addEventListener("change", () => {

            selectedVariant = {
                id: radio.dataset.id,
                name: radio.dataset.name || "",
                min: Number(radio.dataset.min || 1)
            };

        });

    });

    addBtn?.addEventListener("click", () => {

        if (!selectedVariant) {
            alert("Selecciona una variante");
            return;
        }

        let cart = getCart();

        let existing = cart.find(
            x => x.variantId === selectedVariant.id
        );

        if (existing) {
            existing.quantity += selectedVariant.min;
        } else {

            cart.push({
                productId: window.PRODUCT_CONTEXT.productId,
                productName: window.PRODUCT_CONTEXT.productName,
                variantId: selectedVariant.id,
                variantName: selectedVariant.name,
                quantity: selectedVariant.min,
                min: selectedVariant.min
            });

        }

        saveCart(cart);
        renderCartSidebar();
        toggleCart();

    });

    renderCartSidebar();
});