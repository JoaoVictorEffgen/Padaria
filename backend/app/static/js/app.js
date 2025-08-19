// Configurações da aplicação
const CONFIG = {
    API_BASE_URL: window.location.origin,
    WHATSAPP_NUMBER: '5511999999999', // Substitua pelo número real da padaria
    WHATSAPP_MESSAGE: 'Olá! Gostaria de fazer um pedido de entrega.',
    CURRENCY: 'R$',
    DELIVERY_FEE: 5.00,
    MINIMUM_ORDER: 1.00
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
    loadMesas();
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

// Carregar mesas da API
async function loadMesas() {
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/mesas/`);
        if (!response.ok) throw new Error('Erro ao carregar mesas');
        
        const mesas = await response.json();
        renderMesas(mesas);
    } catch (error) {
        console.error('Erro ao carregar mesas:', error);
        showError('Erro ao carregar mesas. Tente novamente.');
    }
}

// Renderizar mesas
function renderMesas(mesas) {
    const mesasGrid = document.getElementById('mesasGrid');
    if (!mesasGrid) return;
    
    mesasGrid.innerHTML = '';
    
    if (mesas.length === 0) {
        mesasGrid.innerHTML = `
            <div class="no-mesas">
                <i class="fas fa-table"></i>
                <h3>Nenhuma mesa disponível</h3>
                <p>Entre em contato conosco para mais informações</p>
            </div>
        `;
        return;
    }
    
    mesas.forEach(mesa => {
        const mesaCard = createMesaCard(mesa);
        mesasGrid.appendChild(mesaCard);
    });
}

// Criar card de mesa
function createMesaCard(mesa) {
    const card = document.createElement('div');
    card.className = `mesa-card ${mesa.status}`;
    
    // Ícone baseado no status
    const statusIcons = {
        'livre': 'fas fa-check-circle',
        'ocupada': 'fas fa-times-circle',
        'reservada': 'fas fa-clock'
    };
    
    const icon = statusIcons[mesa.status] || 'fas fa-table';
    
    // Texto do status
    const statusTexts = {
        'livre': 'LIVRE',
        'ocupada': 'OCUPADA',
        'reservada': 'RESERVADA'
    };
    
    const statusText = statusTexts[mesa.status] || mesa.status.toUpperCase();
    
    // Botão baseado no status
    let actionButton = '';
    if (mesa.status === 'livre') {
        actionButton = `
            <button class="mesa-btn reservar" onclick="abrirModalReserva(${mesa.id})">
                <i class="fas fa-bookmark"></i>
                Reservar
            </button>
        `;
    } else if (mesa.status === 'reservada') {
        actionButton = `
            <button class="mesa-btn ver-reserva" onclick="verReservaMesa(${mesa.id})">
                <i class="fas fa-eye"></i>
                Ver Reserva
            </button>
        `;
    } else {
        actionButton = `
            <button class="mesa-btn" disabled>
                <i class="fas fa-ban"></i>
                Indisponível
            </button>
        `;
    }
    
    card.innerHTML = `
        <div class="mesa-icon">
            <i class="${icon}"></i>
        </div>
        <div class="mesa-numero">Mesa ${mesa.numero}</div>
        <div class="mesa-status ${mesa.status}">${statusText}</div>
        <div class="mesa-actions">
            ${actionButton}
        </div>
    `;
    
    return card;
}

// Reservar mesa
async function reservarMesa(mesaId) {
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/mesas/${mesaId}/reservar`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Erro ao reservar mesa');
        }
        
        showSuccess('Mesa reservada com sucesso!');
        loadMesas(); // Recarregar mesas
    } catch (error) {
        console.error('Erro ao reservar mesa:', error);
        showError(error.message || 'Erro ao reservar mesa. Tente novamente.');
    }
}

// Liberar mesa
async function liberarMesa(mesaId) {
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/mesas/${mesaId}/liberar`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Erro ao liberar mesa');
        }
        
        showSuccess('Mesa liberada com sucesso!');
        loadMesas(); // Recarregar mesas
    } catch (error) {
        console.error('Erro ao liberar mesa:', error);
        showError(error.message || 'Erro ao liberar mesa. Tente novamente.');
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
        showError('Adicione itens ao carrinho antes de finalizar o pedido.');
        return;
    }
    
    // Verificar valor mínimo
    const total = calculateCartTotal();
    if (total < CONFIG.MINIMUM_ORDER) {
        showError(`Pedido mínimo de ${CONFIG.CURRENCY} ${CONFIG.MINIMUM_ORDER.toFixed(2)}`);
        return;
    }
    
    // Mostrar modal de finalização
    showOrderModal();
}

function calculateCartTotal() {
    return appState.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
}

function showOrderModal() {
    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.id = 'orderModal';
    
    const total = calculateCartTotal();
    
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h3><i class="fas fa-shopping-cart"></i> Finalizar Pedido</h3>
                <button class="modal-close" onclick="closeOrderModal()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="modal-body">
                <form id="orderForm">
                    <div class="form-group">
                        <label for="customerName">Nome Completo *</label>
                        <input type="text" id="customerName" required>
                    </div>
                    <div class="form-group">
                        <label for="customerPhone">Telefone *</label>
                        <input type="tel" id="customerPhone" placeholder="(11) 99999-9999" required>
                    </div>
                    <div class="form-group">
                        <label for="customerAddress">Endereço de Entrega *</label>
                        <textarea id="customerAddress" rows="3" placeholder="Rua, número, bairro, cidade" required></textarea>
                    </div>
                    <div class="form-group">
                        <label for="paymentMethod">Forma de Pagamento *</label>
                        <select id="paymentMethod" required>
                            <option value="">Selecione...</option>
                            <option value="dinheiro">Dinheiro</option>
                            <option value="pix">PIX</option>
                            <option value="cartao">Cartão de Crédito/Débito</option>
                            <option value="transferencia">Transferência Bancária</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="orderNotes">Observações</label>
                        <textarea id="orderNotes" rows="2" placeholder="Instruções especiais, troco, etc."></textarea>
                    </div>
                    <div class="order-summary">
                        <h4>Resumo do Pedido</h4>
                        <div class="order-items">
                            ${appState.cart.map(item => `
                                <div class="order-item">
                                    <span>${item.quantity}x ${item.name}</span>
                                    <span>${CONFIG.CURRENCY} ${(item.price * item.quantity).toFixed(2)}</span>
                                </div>
                            `).join('')}
                        </div>
                        <div class="order-total">
                            <strong>Total: ${CONFIG.CURRENCY} ${total.toFixed(2)}</strong>
                        </div>
                    </div>
                    <div class="form-actions">
                        <button type="button" class="btn btn-secondary" onclick="closeOrderModal()">
                            Cancelar
                        </button>
                        <button type="submit" class="btn btn-primary">
                            <i class="fas fa-paper-plane"></i>
                            Enviar Pedido
                        </button>
                    </div>
                </form>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Configurar formulário
    const form = document.getElementById('orderForm');
    form.addEventListener('submit', handleOrderSubmit);
    
    // Focar no primeiro campo
    document.getElementById('customerName').focus();
}

function closeOrderModal() {
    const modal = document.getElementById('orderModal');
    if (modal) {
        modal.remove();
    }
}

async function handleOrderSubmit(e) {
    e.preventDefault();
    
    const formData = {
        nome_cliente: document.getElementById('customerName').value,
        telefone: document.getElementById('customerPhone').value,
        endereco: document.getElementById('customerAddress').value,
        forma_pagamento: document.getElementById('paymentMethod').value,
        observacoes: document.getElementById('orderNotes').value,
        itens: appState.cart.map(item => ({
            produto_id: item.id,
            quantidade: item.quantity,
            preco_unitario: item.price,
            observacoes: null
        }))
    };
    
    try {
        showLoading(true);
        
        const response = await fetch(`${CONFIG.API_BASE_URL}/pedidos-online/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            throw new Error('Erro ao enviar pedido');
        }
        
        const result = await response.json();
        
        // Fechar modal
        closeOrderModal();
        
        // Limpar carrinho
        appState.cart = [];
        saveCartToStorage();
        updateCartDisplay();
        updateProductQuantities();
        
        // Mostrar sucesso
        showSuccess('Pedido enviado com sucesso! Entraremos em contato em breve.');
        
    } catch (error) {
        console.error('Erro ao enviar pedido:', error);
        showError('Erro ao enviar pedido. Tente novamente.');
    } finally {
        showLoading(false);
    }
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
    // Mostrar mensagem informativa em vez de abrir WhatsApp
    showSuccess('Para fazer um pedido, adicione produtos ao carrinho e clique em "Finalizar Pedido"!');
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

// ============================================================================
// SISTEMA DE RESERVAS
// ============================================================================

let mesaSelecionada = null;
let clienteAtual = null;

// Abrir modal de reserva
function abrirModalReserva(mesaId) {
    mesaSelecionada = mesaId;
    document.getElementById('reservaModal').classList.add('show');
    
    // Definir data mínima como hoje
    const hoje = new Date().toISOString().split('T')[0];
    document.getElementById('dataReserva').min = hoje;
}

// Fechar modal de reserva
function closeReservaModal() {
    document.getElementById('reservaModal').classList.remove('show');
    document.getElementById('reservaForm').reset();
    mesaSelecionada = null;
}

// Abrir modal de cliente existente
function abrirModalClienteExistente(cliente) {
    clienteAtual = cliente;
    
    // Preencher informações do cliente
    document.getElementById('clienteNomeExibicao').textContent = cliente.nome;
    document.getElementById('clienteTelefoneExibicao').textContent = cliente.telefone;
    document.getElementById('clienteEnderecoExibicao').textContent = cliente.endereco;
    
    // Definir data mínima como hoje
    const hoje = new Date().toISOString().split('T')[0];
    document.getElementById('dataReservaExistente').min = hoje;
    
    document.getElementById('clienteModal').classList.add('show');
}

// Fechar modal de cliente existente
function closeClienteModal() {
    document.getElementById('clienteModal').classList.remove('show');
    document.getElementById('dataReservaExistente').value = '';
    document.getElementById('horarioReservaExistente').value = '';
    document.getElementById('observacoesExistente').value = '';
    clienteAtual = null;
}

// Ver reserva de uma mesa
async function verReservaMesa(mesaId) {
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/reservas/mesa/${mesaId}`);
        if (!response.ok) throw new Error('Erro ao carregar reserva');
        
        const data = await response.json();
        
        if (data.reservas && data.reservas.length > 0) {
            const reserva = data.reservas[0];
            showNotification(`Mesa reservada para ${reserva.nome_cliente} às ${reserva.horario_reserva}`);
        } else {
            showNotification('Mesa sem reservas ativas');
        }
    } catch (error) {
        console.error('Erro ao ver reserva:', error);
        showError('Erro ao carregar informações da reserva');
    }
}

// Configurar formulário de reserva
document.addEventListener('DOMContentLoaded', function() {
    const reservaForm = document.getElementById('reservaForm');
    if (reservaForm) {
        reservaForm.addEventListener('submit', handleReservaForm);
    }
});

// Processar formulário de reserva
async function handleReservaForm(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const telefone = formData.get('clienteTelefone');
    
    try {
        // Verificar se cliente já existe
        const clienteResponse = await fetch(`${CONFIG.API_BASE_URL}/clientes/telefone/${telefone}`);
        
        if (clienteResponse.ok) {
            // Cliente existe - mostrar modal de cliente existente
            const cliente = await clienteResponse.json();
            closeReservaModal();
            abrirModalClienteExistente(cliente);
            return;
        }
        
        // Cliente não existe - criar novo cliente e reserva
        await criarClienteEReserva(formData);
        
    } catch (error) {
        console.error('Erro ao processar reserva:', error);
        showError('Erro ao processar reserva. Tente novamente.');
    }
}

// Criar cliente e reserva
async function criarClienteEReserva(formData) {
    try {
        // 1. Criar cliente
        const clienteData = {
            nome: formData.get('clienteNome'),
            telefone: formData.get('clienteTelefone'),
            endereco: formData.get('clienteEndereco')
        };
        
        const clienteResponse = await fetch(`${CONFIG.API_BASE_URL}/clientes/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(clienteData)
        });
        
        if (!clienteResponse.ok) throw new Error('Erro ao criar cliente');
        
        const cliente = await clienteResponse.json();
        
        // 2. Criar reserva
        const reservaData = {
            mesa_id: mesaSelecionada,
            cliente_id: cliente.id,
            data_reserva: formData.get('dataReserva'),
            horario_reserva: formData.get('horarioReserva'),
            observacoes: formData.get('observacoes') || ''
        };
        
        const reservaResponse = await fetch(`${CONFIG.API_BASE_URL}/reservas/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(reservaData)
        });
        
        if (!reservaResponse.ok) throw new Error('Erro ao criar reserva');
        
        // 3. Sucesso
        closeReservaModal();
        showSuccess('Reserva criada com sucesso!');
        loadMesas(); // Recarregar mesas
        
    } catch (error) {
        console.error('Erro ao criar cliente e reserva:', error);
        showError('Erro ao criar reserva. Tente novamente.');
    }
}

// Confirmar reserva para cliente existente
async function confirmarReservaClienteExistente() {
    if (!clienteAtual || !mesaSelecionada) {
        showError('Dados inválidos para reserva');
        return;
    }
    
    try {
        const reservaData = {
            mesa_id: mesaSelecionada,
            cliente_id: clienteAtual.id,
            data_reserva: document.getElementById('dataReservaExistente').value,
            horario_reserva: document.getElementById('horarioReservaExistente').value,
            observacoes: document.getElementById('observacoesExistente').value || ''
        };
        
        const reservaResponse = await fetch(`${CONFIG.API_BASE_URL}/reservas/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(reservaData)
        });
        
        if (!reservaResponse.ok) throw new Error('Erro ao criar reserva');
        
        // Sucesso
        closeClienteModal();
        showSuccess('Reserva criada com sucesso!');
        loadMesas(); // Recarregar mesas
        
    } catch (error) {
        console.error('Erro ao criar reserva:', error);
        showError('Erro ao criar reserva. Tente novamente.');
    }
}

// Atualizar carrinho quando a página é carregada
window.addEventListener('load', () => {
    updateCartDisplay();
}); 