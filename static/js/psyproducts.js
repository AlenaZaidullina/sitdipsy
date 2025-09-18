document.addEventListener('DOMContentLoaded', function() {
    let cart = [];
    const cartItems = document.getElementById('cart-items');
    const emptyCart = document.getElementById('empty-cart');
    const cartTotal = document.getElementById('cart-total');
    const totalAmount = document.getElementById('total-amount');
    const purchaseBtn = document.getElementById('purchase-btn');

    // Константа с вашим телеграм каналом
    const TELEGRAM_CHANNEL = 'sitdipsy';

    // 1. Инициализация корзины из localStorage
    function initCart() {
        const savedCart = localStorage.getItem('product_cart');
        if (savedCart) {
            cart = JSON.parse(savedCart);
            updateCartDisplay();
        }
    }

    // 2. Сохранение корзины в localStorage
    function saveCart() {
        localStorage.setItem('product_cart', JSON.stringify(cart));
    }

    // 3. Обновление отображения корзины
    function updateCartDisplay() {
        if (cart.length === 0) {
            emptyCart.style.display = 'block';
            cartTotal.style.display = 'none';
            cartItems.innerHTML = '<p class="empty-basket" id="empty-cart">Корзина пуста</p>';
        } else {
            emptyCart.style.display = 'none';
            cartTotal.style.display = 'block';

            let html = '';
            let total = 0;

            cart.forEach((item, index) => {
                total += parseFloat(item.price);
                html += `
                    <div class="cart-item">
                        <span class="cart-item-name">${item.name}</span>
                        <span class="cart-item-price">${item.price} ₽</span>
                        <button class="remove-from-cart-btn" data-index="${index}">
                            Удалить
                        </button>
                    </div>
                `;
            });

            cartItems.innerHTML = html;
            totalAmount.textContent = total.toFixed(2);

            // Добавляем обработчики для кнопок удаления
            document.querySelectorAll('.remove-from-cart-btn').forEach(btn => {
                btn.addEventListener('click', function() {
                    const index = parseInt(this.getAttribute('data-index'));
                    removeFromCart(index);
                });
            });
        }
    }

    // 4. Добавление товара в корзину
    function addToCart(product) {
        // Проверяем, нет ли уже этого товара в корзине
        const existingItem = cart.find(item => item.id === product.id);
        if (!existingItem) {
            cart.push(product);
            saveCart();
            updateCartDisplay();
            showNotification(`"${product.name}" добавлен в корзину!`);
        } else {
            showNotification('Этот товар уже в корзине');
        }
    }

    // 5. Удаление товара из корзины
    function removeFromCart(index) {
        const removedItem = cart[index];
        cart.splice(index, 1);
        saveCart();
        updateCartDisplay();
        showNotification(`"${removedItem.name}" удален из корзины`);
    }

    // 6. Показать уведомление
    function showNotification(message) {
        // Создаем уведомление
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--organic);
            color: white;
            padding: 1rem 2rem;
            border-radius: 8px;
            z-index: 10000;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        `;
        notification.textContent = message;
        document.body.appendChild(notification);

        // Удаляем через 3 секунды
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    // 7. Обработчик для кнопок "Добавить"
    document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const product = {
                id: this.getAttribute('data-product-id'),
                name: this.getAttribute('data-product-name'),
                price: this.getAttribute('data-product-price')
            };
            addToCart(product);
        });
    });


    // 8. Обработчик для кнопки "Хочу приобрести"
    purchaseBtn.addEventListener('click', function() {
        if (cart.length === 0) {
            showNotification('Корзина пуста');
            return;
        }

        // Формируем текст сообщения
        const productNames = cart.map(item => `"${item.name}"`).join(', ');
        const totalPrice = cart.reduce((sum, item) => sum + parseFloat(item.price), 0);

        const message = `Добрый день. Я бы хотел(а) приобрести методические материалы с названиями: ${productNames}. Общая сумма: ${totalPrice.toFixed(2)} ₽.`;

        // Пробуем открыть Telegram с сообщением
        const encodedMessage = encodeURIComponent(message);

        // Основная попытка - через share механизм
        const telegramShareUrl = `https://t.me/sitdipsy?text=${encodedMessage}`;
        const newWindow = window.open(telegramShareUrl, '_blank');

        // Резервный вариант через 1 секунду
        setTimeout(() => {
            if (!newWindow || newWindow.closed || typeof newWindow.closed == 'undefined') {
                // Если не получилось, пробуем прямой переход в канал
                const telegramDirectUrl = `https://t.me/sitdipsy?text=${encodedMessage}`;
                window.open(telegramDirectUrl, '_blank');
            }
        }, 1000);
    });

    // 9. Обработчик для кнопок "Подробнее"
    document.querySelectorAll('.details-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const productName = this.getAttribute('data-product-name');
            const productDescription = this.getAttribute('data-product-description');

            document.getElementById('modalProductName').textContent = productName;
            document.getElementById('modalProductDescription').textContent = productDescription;
            document.getElementById('productModal').style.display = 'block';
        });
    });

    // 10. Обработчик для кнопок "Скачать"
    document.querySelectorAll('.download-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const downloadUrl = this.getAttribute('data-download-url');
            if (downloadUrl) {
                window.location.href = downloadUrl;
            } else {
                showNotification('Файл недоступен для скачивания');
            }
        });
    });

    // 11. Закрытие модального окна
    if (document.querySelector('.close')) {
        document.querySelector('.close').addEventListener('click', function() {
            document.getElementById('productModal').style.display = 'none';
        });
    }

    // 12. Закрытие при клике вне окна
    window.addEventListener('click', function(event) {
        if (event.target === document.getElementById('productModal')) {
            document.getElementById('productModal').style.display = 'none';
        }
    });

    // Инициализируем корзину при загрузке
    initCart();
});