// Configurações da aplicação
const CONFIG = {
    API_BASE_URL: window.location.origin,
    WHATSAPP_NUMBER: '5511999999999', // Substitua pelo número real da padaria
    WHATSAPP_MESSAGE: 'Olá! Gostaria de fazer um pedido de entrega.',
    CURRENCY: 'R$',
    DELIVERY_FEE: 5.00,
    MINIMUM_ORDER: 15.00
};

// Estado global da aplicação
let appState = {
    products: [],
    cart: [],
    currentCategory: 'all',
    isLoading: false
};

// Elementos DOM
const elements = {
    productsGrid: document.getElementById('productsGrid'),
    cartSidebar: document.getElementById('cartSidebar'),
    cartItems: document.getElementById('cartItems'),
    cartTotal: document.getElementById('cartTotal'),
    cartCount: document.getElementById('cartCount'),
    cartToggle: document.getElementById('cartToggle'),
    loadingOverlay: document.getElementById('loadingOverlay'),
    successModal: document.getElementById('successModal'),
    filterButtons: document.querySelectorAll('.filter-btn'),
    navToggle: document.querySelector('.nav-toggle'),
    navMenu: document.querySelector('.nav-menu'),
    contactForm: document.getElementById('contactForm')
};

// Inicialização da aplicação
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    loadProducts();
});

// Inicializar aplicação
function initializeApp() {
    // Carregar carrinho do localStorage
    loadCartFromStorage();
    updateCartDisplay();
    
    // Configurar smooth scroll para links de navegação
    setupSmoothScroll();
    
    // Configurar menu mobile
    setupMobileMenu();
}

// Configurar event listeners
function setupEventListeners() {
    // Filtros de categoria
    elements.filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const category = btn.dataset.category;
            filterProducts(category);
            
            // Atualizar botões ativos
            elements.filterButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        });
    });

    // Formulário de contato
    if (elements.contactForm) {
        elements.contactForm.addEventListener('submit', handleContactForm);
    }

    // Fechar carrinho ao clicar fora
    document.addEventListener('click', (e) => {
        if (!elements.cartSidebar.contains(e.target) && 
            !elements.cartToggle.contains(e.target) && 
            elements.cartSidebar.classList.contains('open')) {
            toggleCart();
        }
    });
}

// Carregar produtos da API
async function loadProducts() {
    showLoading(true);
    
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/produtos/`);
        if (!response.ok) throw new Error('Erro ao carregar produtos');
        
        appState.products = await response.json();
        renderProducts(appState.products);
    } catch (error) {
        console.error('Erro ao carregar produtos:', error);
        showError('Erro ao carregar produtos. Tente novamente.');
    } finally {
        showLoading(false);
    }
}

// Renderizar produtos
function renderProducts(products) {
    if (!elements.productsGrid) return;
    
    elements.productsGrid.innerHTML = '';
    
    if (products.length === 0) {
        elements.productsGrid.innerHTML = `
            <div class="no-products">
                <i class="fas fa-search"></i>
                <h3>Nenhum produto encontrado</h3>
                <p>Tente selecionar outra categoria</p>
            </div>
        `;
        return;
    }
    
    products.forEach(product => {
        const productCard = createProductCard(product);
        elements.productsGrid.appendChild(productCard);
    });
}

// Criar card de produto
function createProductCard(product) {
    const card = document.createElement('div');
    card.className = 'product-card';
    
    // Ícone baseado na categoria
    const categoryIcons = {
        'Pães': 'fas fa-bread-slice',
        'Bebidas': 'fas fa-coffee',
        'Doces': 'fas fa-cookie-bite',
        'Salgados': 'fas fa-pizza-slice',
        'Cafés': 'fas fa-mug-hot'
    };
    
    const icon = categoryIcons[product.categoria] || 'fas fa-utensils';
    
    card.innerHTML = `
        <div class="product-image">
            <i class="${icon}"></i>
        </div>
        <div class="product-info">
            <h3 class="product-name">${product.nome}</h3>
            <p class="product-description">${product.descricao || 'Produto artesanal feito com ingredientes selecionados.'}</p>
            <div class="product-price">${CONFIG.CURRENCY} ${product.preco.toFixed(2)}</div>
            <div class="product-actions">
                <div class="quantity-controls">
                    <button class="quantity-btn" onclick="decreaseQuantity(${product.id})">
                        <i class="fas fa-minus"></i>
                    </button>
                    <span class="quantity-display" id="qty-${product.id}">0</span>
                    <button class="quantity-btn" onclick="increaseQuantity(${product.id})">
                        <i class="fas fa-plus"></i>
                    </button>
                </div>
                <button class="btn btn-primary" onclick="addToCart(${product.id})">
                    <i class="fas fa-cart-plus"></i>
                    Adicionar
                </button>
            </div>
        </div>
    `;
    
    // Atualizar quantidade se já estiver no carrinho
    const cartItem = appState.cart.find(item => item.id === product.id);
    if (cartItem) {
        const qtyDisplay = card.querySelector(`#qty-${product.id}`);
        if (qtyDisplay) qtyDisplay.textContent = cartItem.quantity;
    }
    
    return card;
}

// Filtrar produtos por categoria
function filterProducts(category) {
    appState.currentCategory = category;
    
    if (category === 'all') {
        renderProducts(appState.products);
    } else {
        const filteredProducts = appState.products.filter(product => 
            product.categoria === category
        );
        renderProducts(filteredProducts);
    }
}

// Funções do carrinho
function addToCart(productId) {
    const product = appState.products.find(p => p.id === productId);
    if (!product) return;
    
    const existingItem = appState.cart.find(item => item.id === productId);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        appState.cart.push({
            id: product.id,
            name: product.nome,
            price: product.preco,
            quantity: 1
        });
    }
    
    updateCartDisplay();
    saveCartToStorage();
    showNotification(`${product.nome} adicionado ao carrinho!`);
}

function removeFromCart(productId) {
    appState.cart = appState.cart.filter(item => item.id !== productId);
    updateCartDisplay();
    saveCartToStorage();
}

function updateQuantity(productId, newQuantity) {
    if (newQuantity <= 0) {
        removeFromCart(productId);
        return;
    }
    
    const item = appState.cart.find(item => item.id === productId);
    if (item) {
        item.quantity = newQuantity;
        updateCartDisplay();
        saveCartToStorage();
    }
}

function increaseQuantity(productId) {
    const item = appState.cart.find(item => item.id === productId);
    if (item) {
        updateQuantity(productId, item.quantity + 1);
    } else {
        addToCart(productId);
    }
}

function decreaseQuantity(productId) {
    const item = appState.cart.find(item => item.id === productId);
    if (item) {
        updateQuantity(productId, item.quantity - 1);
    }
}

// Atualizar exibição do carrinho
function updateCartDisplay() {
    // Atualizar contador
    const totalItems = appState.cart.reduce((sum, item) => sum + item.quantity, 0);
    elements.cartCount.textContent = totalItems;
    
    // Atualizar itens do carrinho
    elements.cartItems.innerHTML = '';
    
    if (appState.cart.length === 0) {
        elements.cartItems.innerHTML = `
            <div class="empty-cart">
                <i class="fas fa-shopping-cart"></i>
                <p>Seu carrinho está vazio</p>
            </div>
        `;
        elements.cartTotal.textContent = `${CONFIG.CURRENCY} 0,00`;
        return;
    }
    
    appState.cart.forEach(item => {
        const cartItem = document.createElement('div');
        cartItem.className = 'cart-item';
        cartItem.innerHTML = `
            <div class="cart-item-info">
                <div class="cart-item-name">${item.name}</div>
                <div class="cart-item-price">${CONFIG.CURRENCY} ${item.price.toFixed(2)}</div>
            </div>
            <div class="cart-item-quantity">
                <button class="quantity-btn" onclick="decreaseQuantity(${item.id})">
                    <i class="fas fa-minus"></i>
                </button>
                <span>${item.quantity}</span>
                <button class="quantity-btn" onclick="increaseQuantity(${item.id})">
                    <i class="fas fa-plus"></i>
                </button>
            </div>
        `;
        elements.cartItems.appendChild(cartItem);
    });
    
    // Atualizar total
    const total = appState.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    elements.cartTotal.textContent = `${CONFIG.CURRENCY} ${total.toFixed(2)}`;
    
    // Atualizar quantidades nos cards de produtos
    updateProductQuantities();
}

// Atualizar quantidades nos cards de produtos
function updateProductQuantities() {
    appState.cart.forEach(cartItem => {
        const qtyDisplay = document.getElementById(`qty-${cartItem.id}`);
        if (qtyDisplay) {
            qtyDisplay.textContent = cartItem.quantity;
        }
    });
}

// Toggle do carrinho
function toggleCart() {
    elements.cartSidebar.classList.toggle('open');
}

// Finalizar pedido via WhatsApp
function finalizeOrder() {
    if (appState.cart.length === 0) {
        showError('Adicione produtos ao carrinho antes de finalizar o pedido.');
        return;
    }
    
    const total = appState.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    
    // Verificar pedido mínimo
    if (total < CONFIG.MINIMUM_ORDER) {
        showError(`Pedido mínimo para entrega é de ${CONFIG.CURRENCY} ${CONFIG.MINIMUM_ORDER.toFixed(2)}. Adicione mais itens ao carrinho.`);
        return;
    }
    
    const orderMessage = generateOrderMessage();
    const whatsappUrl = `https://wa.me/${CONFIG.WHATSAPP_NUMBER}?text=${encodeURIComponent(orderMessage)}`;
    
    // Abrir WhatsApp
    window.open(whatsappUrl, '_blank');
    
    // Mostrar modal de sucesso
    showSuccessModal();
    
    // Limpar carrinho
    appState.cart = [];
    updateCartDisplay();
    saveCartToStorage();
}

// Gerar mensagem do pedido
function generateOrderMessage() {
    const subtotal = appState.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    const deliveryFee = subtotal >= CONFIG.MINIMUM_ORDER ? CONFIG.DELIVERY_FEE : 0;
    const total = subtotal + deliveryFee;
    
    let message = `${CONFIG.WHATSAPP_MESSAGE}\n\n`;
    message += `*PEDIDO:*\n`;
    message += `━━━━━━━━━━━━━━━━━━━━\n`;
    
    appState.cart.forEach(item => {
        message += `• ${item.name} x${item.quantity} - ${CONFIG.CURRENCY} ${(item.price * item.quantity).toFixed(2)}\n`;
    });
    
    message += `━━━━━━━━━━━━━━━━━━━━\n`;
    message += `Subtotal: ${CONFIG.CURRENCY} ${subtotal.toFixed(2)}\n`;
    
    if (deliveryFee > 0) {
        message += `Taxa de entrega: ${CONFIG.CURRENCY} ${deliveryFee.toFixed(2)}\n`;
    }
    
    message += `*TOTAL: ${CONFIG.CURRENCY} ${total.toFixed(2)}*\n\n`;
    message += `Por favor, informe:\n`;
    message += `• Nome completo\n`;
    message += `• Endereço de entrega\n`;
    message += `• Telefone para contato\n`;
    message += `• Forma de pagamento\n\n`;
    message += `Obrigado! 🥖✨`;
    
    return message;
}

// Abrir WhatsApp diretamente
function openWhatsApp() {
    const message = `${CONFIG.WHATSAPP_MESSAGE}\n\nGostaria de fazer um pedido de entrega. Pode me enviar o cardápio?`;
    const whatsappUrl = `https://wa.me/${CONFIG.WHATSAPP_NUMBER}?text=${encodeURIComponent(message)}`;
    window.open(whatsappUrl, '_blank');
}

// Local Storage
function saveCartToStorage() {
    localStorage.setItem('padariaCart', JSON.stringify(appState.cart));
}

function loadCartFromStorage() {
    const savedCart = localStorage.getItem('padariaCart');
    if (savedCart) {
        appState.cart = JSON.parse(savedCart);
    }
}

// Navegação
function scrollToMenu() {
    const menuSection = document.getElementById('menu');
    if (menuSection) {
        menuSection.scrollIntoView({ behavior: 'smooth' });
    }
}

function setupSmoothScroll() {
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);
            if (targetSection) {
                targetSection.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
}

function setupMobileMenu() {
    if (elements.navToggle && elements.navMenu) {
        elements.navToggle.addEventListener('click', () => {
            elements.navMenu.classList.toggle('active');
        });
    }
}

// Formulário de contato
async function handleContactForm(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = {
        name: formData.get('name') || document.getElementById('name').value,
        email: formData.get('email') || document.getElementById('email').value,
        message: formData.get('message') || document.getElementById('message').value
    };
    
    if (!data.name || !data.email || !data.message) {
        showError('Por favor, preencha todos os campos.');
        return;
    }
    
    showLoading(true);
    
    try {
        // Simular envio (substitua por sua API real)
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        showSuccess('Mensagem enviada com sucesso! Entraremos em contato em breve.');
        e.target.reset();
    } catch (error) {
        showError('Erro ao enviar mensagem. Tente novamente.');
    } finally {
        showLoading(false);
    }
}

// Utilitários de UI
function showLoading(show) {
    appState.isLoading = show;
    if (elements.loadingOverlay) {
        elements.loadingOverlay.classList.toggle('show', show);
    }
}

function showSuccessModal() {
    if (elements.successModal) {
        elements.successModal.classList.add('show');
    }
}

function closeModal() {
    if (elements.successModal) {
        elements.successModal.classList.remove('show');
    }
}

function showNotification(message) {
    // Criar notificação toast
    const toast = document.createElement('div');
    toast.className = 'toast-notification';
    toast.innerHTML = `
        <i class="fas fa-check-circle"></i>
        <span>${message}</span>
    `;
    
    document.body.appendChild(toast);
    
    // Animar entrada
    setTimeout(() => toast.classList.add('show'), 100);
    
    // Remover após 3 segundos
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => document.body.removeChild(toast), 300);
    }, 3000);
}

function showSuccess(message) {
    showNotification(message);
}

function showError(message) {
    // Criar notificação de erro
    const toast = document.createElement('div');
    toast.className = 'toast-notification error';
    toast.innerHTML = `
        <i class="fas fa-exclamation-circle"></i>
        <span>${message}</span>
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => toast.classList.add('show'), 100);
    
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => document.body.removeChild(toast), 300);
    }, 4000);
}

// Adicionar estilos para notificações toast
const toastStyles = `
<style>
.toast-notification {
    position: fixed;
    top: 20px;
    right: 20px;
    background: #27ae60;
    color: white;
    padding: 1rem 1.5rem;
    border-radius: 8px;
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
    display: flex;
    align-items: center;
    gap: 0.5rem;
    z-index: 4000;
    transform: translateX(100%);
    transition: transform 0.3s ease;
    max-width: 300px;
}

.toast-notification.show {
    transform: translateX(0);
}

.toast-notification.error {
    background: #e74c3c;
}

.toast-notification i {
    font-size: 1.2rem;
}

.empty-cart {
    text-align: center;
    padding: 2rem;
    color: #666;
}

.empty-cart i {
    font-size: 3rem;
    margin-bottom: 1rem;
    color: #ddd;
}

.no-products {
    text-align: center;
    padding: 3rem;
    color: #666;
    grid-column: 1 / -1;
}

.no-products i {
    font-size: 3rem;
    margin-bottom: 1rem;
    color: #ddd;
}
</style>
`;

document.head.insertAdjacentHTML('beforeend', toastStyles);

// Fechar modal ao clicar fora
document.addEventListener('click', (e) => {
    if (elements.successModal && e.target === elements.successModal) {
        closeModal();
    }
});

// Atualizar carrinho quando a página é carregada
window.addEventListener('load', () => {
    updateCartDisplay();
}); 