document.addEventListener('DOMContentLoaded', () => {
    
    // SVG Generator function
    const createPlaceholder = (color, emoji) => {
        const svg = `
        <svg width="400" height="400" xmlns="http://www.w3.org/2000/svg">
            <rect width="100%" height="100%" fill="${color}"/>
            <text x="50%" y="50%" font-family="Arial, sans-serif" font-size="150" text-anchor="middle" dy=".35em">${emoji}</text>
        </svg>`;
        return 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(svg);
    };

    // State
    const state = {
        cart: [],
        currentCategory: 'all',
        products: [
            { id: 1, name: 'Футболка Premium', price: 1990, category: 'clothes', image: createPlaceholder('#3B82F6', '👕'), desc: '100% хлопок, размеры S-XXL' },
            { id: 2, name: 'Джинсы Slim Fit', price: 4490, category: 'clothes', image: createPlaceholder('#6366F1', '👖'), desc: 'Деним, размеры 28-36' },
            { id: 3, name: 'Кроссовки Sport', price: 5990, category: 'shoes', image: createPlaceholder('#EC4899', '👟'), desc: 'Дышащие, размеры 36-45' },
            { id: 4, name: 'Сумка Tote', price: 3290, category: 'accessories', image: createPlaceholder('#F59E0B', '👜'), desc: 'Эко-кожа, вместительная' },
            { id: 5, name: 'Наушники Wireless', price: 2990, category: 'electronics', image: createPlaceholder('#10B981', '🎧'), desc: 'Bluetooth 5.0, 20ч работы' },
            { id: 6, name: 'Куртка Демисезон', price: 7990, category: 'clothes', image: createPlaceholder('#EF4444', '🧥'), desc: 'Водоотталкивающая, S-XL' },
            { id: 7, name: 'Ботинки Chelsea', price: 8490, category: 'shoes', image: createPlaceholder('#8B5CF6', '👢'), desc: 'Натуральная кожа, 36-44' },
            { id: 8, name: 'Смарт-часы Pro', price: 6990, category: 'electronics', image: createPlaceholder('#06B6D4', '⌚'), desc: 'Пульс, шаги, уведомления' }
        ],
        modalProduct: null,
        modalQty: 1
    };

    // Elements
    const productsGrid = document.getElementById('products-grid');
    const categoryBtns = document.querySelectorAll('.tg-category');
    const searchInput = document.querySelector('.tg-search-input');
    const toast = document.getElementById('toast');
    
    // Modals
    const productModal = document.getElementById('product-modal');
    const modalAddBtn = document.getElementById('modal-add-btn');
    const qtyValue = document.getElementById('qty-value');
    const cartModal = document.getElementById('cart-modal');
    const cartItemsList = document.getElementById('cart-items-list');
    
    // Cart Bar
    const cartBar = document.getElementById('cart-bar');
    const cartCount = document.getElementById('cart-count');
    const cartTotal = document.getElementById('cart-total');

    // --- Rendering ---
    function renderProducts() {
        productsGrid.innerHTML = '';
        state.products.forEach(product => {
            const card = document.createElement('article');
            card.className = 'tg-product-card';
            card.dataset.category = product.category;
            card.dataset.id = product.id;
            
            // Badges
            let badgeHTML = '';
            if (product.id === 1 || product.id === 5) badgeHTML = '<div class="product-badge sale">-20%</div>';
            if (product.id === 2 || product.id === 7) badgeHTML = '<div class="product-badge hit">Хит</div>';
            if (product.id === 3 || product.id === 8) badgeHTML = '<div class="product-badge new">New</div>';

            // Image tag with style
            const imgTag = `<img src="${product.image}" alt="${product.name}" style="display:block; width:100%; height:100%; object-fit:cover;">`;

            card.innerHTML = `
                <div class="product-image">
                    ${badgeHTML}
                    ${imgTag}
                </div>
                <div class="product-info">
                    <h3 class="product-name">${product.name}</h3>
                    <p class="product-description">${product.desc}</p>
                    <div class="product-prices">
                        <span class="price-current">${formatPrice(product.price)}</span>
                    </div>
                    <button class="add-to-cart-btn" data-id="${product.id}">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/>
                            <line x1="3" y1="6" x2="21" y2="6"/>
                            <path d="M16 10a4 4 0 0 1-8 0"/>
                        </svg>
                        В корзину
                    </button>
                </div>
            `;
            productsGrid.appendChild(card);
        });
        filterProducts();
    }

    renderProducts();

    // --- Filtering ---
    categoryBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            categoryBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            state.currentCategory = btn.dataset.category;
            filterProducts();
        });
    });

    searchInput.addEventListener('input', (e) => {
        filterProducts(e.target.value.toLowerCase());
    });

    function filterProducts(searchTerm = '') {
        if (!searchTerm && searchInput.value) searchTerm = searchInput.value.toLowerCase();
        
        const cards = productsGrid.querySelectorAll('.tg-product-card');
        cards.forEach(card => {
            const category = card.dataset.category;
            const name = card.querySelector('.product-name').textContent.toLowerCase();
            
            const categoryMatch = state.currentCategory === 'all' || category === state.currentCategory;
            const searchMatch = name.includes(searchTerm);
            
            if (categoryMatch && searchMatch) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }

    // --- Interactions (Delegation) ---
    productsGrid.addEventListener('click', (e) => {
        const addToCartBtn = e.target.closest('.add-to-cart-btn');
        if (addToCartBtn) {
            e.stopPropagation();
            const id = parseInt(addToCartBtn.dataset.id);
            addToCart(id, 1);
            
            const originalContent = addToCartBtn.innerHTML;
            addToCartBtn.innerHTML = '✓';
            addToCartBtn.classList.add('added');
            setTimeout(() => {
                addToCartBtn.innerHTML = originalContent;
                addToCartBtn.classList.remove('added');
            }, 1000);
            return;
        }

        const card = e.target.closest('.tg-product-card');
        if (card) {
            const id = parseInt(card.dataset.id);
            openProductModal(id);
        }
    });

    // --- Product Modal ---
    function openProductModal(id) {
        const product = state.products.find(p => p.id === id);
        if (!product) return;

        state.modalProduct = product;
        state.modalQty = 1;
        
        document.getElementById('modal-title').textContent = product.name;
        document.getElementById('modal-description').textContent = product.desc;
        document.getElementById('modal-price').textContent = formatPrice(product.price);
        document.getElementById('modal-image').innerHTML = `<img src="${product.image}" alt="${product.name}" style="width:100%; height:100%; object-fit:cover;">`;
        qtyValue.textContent = state.modalQty;
        modalAddBtn.textContent = `Добавить за ${formatPrice(product.price)}`;

        productModal.classList.add('visible');
        document.body.style.overflow = 'hidden';
    }

    function closeProductModal() {
        productModal.classList.remove('visible');
        document.body.style.overflow = '';
        state.modalProduct = null;
    }

    document.getElementById('modal-close').addEventListener('click', closeProductModal);
    
    document.querySelector('.qty-btn.minus').addEventListener('click', () => {
        if (state.modalQty > 1) {
            state.modalQty--;
            qtyValue.textContent = state.modalQty;
            modalAddBtn.textContent = `Добавить за ${formatPrice(state.modalProduct.price * state.modalQty)}`;
        }
    });

    document.querySelector('.qty-btn.plus').addEventListener('click', () => {
        if (state.modalQty < 10) {
            state.modalQty++;
            qtyValue.textContent = state.modalQty;
            modalAddBtn.textContent = `Добавить за ${formatPrice(state.modalProduct.price * state.modalQty)}`;
        }
    });

    modalAddBtn.addEventListener('click', () => {
        if (state.modalProduct) {
            addToCart(state.modalProduct.id, state.modalQty);
            closeProductModal();
        }
    });

    // --- Cart ---
    function addToCart(id, qty) {
        const product = state.products.find(p => p.id === id);
        if (!product) return;

        const existing = state.cart.find(i => i.id === id);
        if (existing) {
            existing.qty += qty;
        } else {
            state.cart.push({ ...product, qty });
        }
        
        updateCartUI();
        showToast();
    }

    function updateCartUI() {
        const totalQty = state.cart.reduce((sum, i) => sum + i.qty, 0);
        const totalPrice = state.cart.reduce((sum, i) => sum + (i.price * i.qty), 0);

        cartCount.textContent = totalQty;
        cartTotal.textContent = formatPrice(totalPrice);
        
        if (totalQty > 0) {
            cartBar.classList.add('visible');
        } else {
            cartBar.classList.remove('visible');
            closeCartModal();
        }
    }

    // --- Cart Modal ---
    cartBar.addEventListener('click', (e) => {
        if (e.target.closest('#checkout-btn')) return;
        openCartModal();
    });

    document.querySelector('.cart-info').addEventListener('click', openCartModal);

    function openCartModal() {
        if (state.cart.length === 0) return;
        renderCartItems();
        cartModal.classList.add('visible');
        document.body.style.overflow = 'hidden';
    }

    function closeCartModal() {
        cartModal.classList.remove('visible');
        document.body.style.overflow = '';
    }

    document.getElementById('cart-close').addEventListener('click', closeCartModal);

    function renderCartItems() {
        cartItemsList.innerHTML = '';
        let total = 0;
        let count = 0;

        state.cart.forEach(item => {
            total += item.price * item.qty;
            count += item.qty;
            
            const div = document.createElement('div');
            div.className = 'cart-item';
            div.innerHTML = `
                <div class="cart-item-image"><img src="${item.image}" style="width:100%; height:100%; object-fit:cover;"></div>
                <div class="cart-item-info">
                    <div class="cart-item-title">${item.name}</div>
                    <div class="cart-item-price">${formatPrice(item.price)}</div>
                </div>
                <div class="cart-item-controls">
                    <button class="cart-control-btn minus" data-id="${item.id}">−</button>
                    <span class="cart-item-qty">${item.qty}</span>
                    <button class="cart-control-btn plus" data-id="${item.id}">+</button>
                </div>
            `;
            cartItemsList.appendChild(div);
        });

        document.getElementById('summary-count').textContent = `${count} шт.`;
        document.getElementById('summary-total').textContent = formatPrice(total);
        document.getElementById('cart-checkout-btn').textContent = `Оформить на ${formatPrice(total)}`;
    }

    cartItemsList.addEventListener('click', (e) => {
        const btn = e.target.closest('.cart-control-btn');
        if (!btn) return;
        
        const id = parseInt(btn.dataset.id);
        const item = state.cart.find(i => i.id === id);
        
        if (btn.classList.contains('plus')) item.qty++;
        else if (btn.classList.contains('minus')) {
            item.qty--;
            if (item.qty <= 0) state.cart = state.cart.filter(i => i.id !== id);
        }
        
        updateCartUI();
        renderCartItems();
    });

    // --- Helpers ---
    function formatPrice(price) {
        return new Intl.NumberFormat('ru-RU').format(price) + ' ₽';
    }

    function showToast() {
        toast.classList.add('visible');
        setTimeout(() => toast.classList.remove('visible'), 2000);
    }

    document.querySelectorAll('.modal-overlay').forEach(el => {
        el.addEventListener('click', () => {
            closeProductModal();
            closeCartModal();
        });
    });

    // --- Checkout ---
    const handleCheckout = () => {
        alert('Заказ оформлен! Спасибо за покупку.');
        state.cart = [];
        updateCartUI();
        closeCartModal();
    };
    document.getElementById('checkout-btn').addEventListener('click', handleCheckout);
    document.getElementById('cart-checkout-btn').addEventListener('click', handleCheckout);

    // --- Support Chat Logic ---
    const supportModal = document.getElementById('support-modal');
    const openSupportBtn = document.getElementById('open-support-btn');
    const supportCloseBtn = document.getElementById('support-close');
    const chatArea = document.getElementById('chat-area');
    const chatInput = document.getElementById('chat-input');
    const chatSendBtn = document.getElementById('chat-send');
    const chatChips = document.querySelectorAll('.chat-chip');

    openSupportBtn.addEventListener('click', () => {
        supportModal.classList.add('visible');
        document.body.style.overflow = 'hidden';
        setTimeout(() => {
            chatInput.focus();
        }, 300);
    });

    supportCloseBtn.addEventListener('click', () => {
        supportModal.classList.remove('visible');
        document.body.style.overflow = '';
    });

    function addMessage(text, type) {
        const div = document.createElement('div');
        div.className = `chat-msg ${type}`;
        div.textContent = text;
        chatArea.insertBefore(div, chatArea.querySelector('.chat-chips'));
        chatArea.scrollTop = chatArea.scrollHeight;
    }

    function botReply(text) {
        // Typing indicator simulation could go here
        setTimeout(() => {
            addMessage(text, 'bot');
        }, 1000 + Math.random() * 1000);
    }

    function handleSend() {
        const text = chatInput.value.trim();
        if (!text) return;
        
        addMessage(text, 'user');
        chatInput.value = '';
        
        // Simple auto-reply logic
        const lower = text.toLowerCase();
        if (lower.includes('где') || lower.includes('заказ')) {
            botReply('Ваш заказ обрабатывается и будет отправлен в течение 24 часов. Трек-номер придет в уведомлении.');
        } else if (lower.includes('размер')) {
            botReply('Размерная сетка доступна в карточке каждого товара. Если сомневаетесь, рекомендуем брать на размер больше.');
        } else if (lower.includes('возврат')) {
            botReply('Возврат возможен в течение 14 дней. Просто принесите товар в любой пункт выдачи Wildberries.');
        } else {
            botReply('Спасибо за вопрос! Оператор подключится к диалогу в течение минуты.');
        }
    }

    chatSendBtn.addEventListener('click', handleSend);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSend();
    });

    chatChips.forEach(chip => {
        chip.addEventListener('click', () => {
            const text = chip.textContent.replace(/^[^\wа-яА-ЯёЁ]+/, '').trim(); // Remove emoji prefix
            addMessage(text, 'user');
            
            // Logic match
            if (text.includes('Где заказ')) botReply('Ваш заказ в пути! Ожидаемая дата доставки: завтра.');
            else if (text.includes('размеров')) botReply('Отправил вам таблицу размеров 📄. (тут должна быть картинка)');
            else if (text.includes('Возврат')) botReply('Для возврата заполните заявку в личном кабинете WB.');
        });
    });

    // --- Auto Scaling ---
    function adjustScale() {
        const phoneHeight = 844;
        const availableHeight = window.innerHeight - 40; 
        const scale = Math.min(1, availableHeight / phoneHeight);
        
        const frame = document.querySelector('.phone-frame');
        if (frame) {
            frame.style.transform = `scale(${scale})`;
            frame.style.marginTop = '0';
            frame.style.marginBottom = '0';
        }
    }

    window.addEventListener('resize', adjustScale);
    adjustScale();
    setTimeout(adjustScale, 100);

    // Telegram WebApp Init
    if (window.Telegram && window.Telegram.WebApp) {
        const tg = window.Telegram.WebApp;
        tg.expand();
        tg.ready();
    }

    if (window.location.search.includes('openChat=true')) {
        supportModal.classList.add('visible');
        document.body.style.overflow = 'hidden';
    }
});
