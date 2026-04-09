class PopupManager {
    constructor() {
        this.popup = document.getElementById('products-popup');
        if (!this.popup) return;

        this.init();
        this.setupTriggers();
    }

    init() {
        // Закрытие по крестику
        document.querySelectorAll('.popup-close').forEach(btn => {
            btn.addEventListener('click', () => this.hidePopup());
        });

        // Закрытие по клику вне popup
        this.popup.addEventListener('click', (e) => {
            if (e.target === this.popup) this.hidePopup();
        });

        // Закрытие по ESC
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') this.hidePopup();
        });

        // Отслеживание кликов по ссылкам для статистики
        document.querySelectorAll('.option-link').forEach(link => {
            link.addEventListener('click', () => {
                this.trackClick(link.href);
            });
        });
    }

    setupTriggers() {
        // Показ через 30 секунд
        setTimeout(() => {
            if (!this.wasShown()) {
                this.showPopup();
                this.setShown();
            }
        }, 180000);
    }

    showPopup() {
        this.popup.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    hidePopup() {
        this.popup.classList.remove('active');
        document.body.style.overflow = '';
    }

    wasShown() {
        return sessionStorage.getItem('popup_shown') === 'true';
    }

    setShown() {
        sessionStorage.setItem('popup_shown', 'true');
    }

    trackClick(url) {
        // Здесь можно добавить отправку данных в аналитику
        console.log('Popup click tracked:', url);
        // Например: sendToAnalytics('popup_click', { url: url });
    }
}

class ChatbotPopupManager {
    constructor() {
        this.popup = document.getElementById('chatbot-popup');
        this.appointmentSection = document.getElementById('appointment');
        if (!this.popup || !this.appointmentSection) return;

        this.hasShown = false;
        this.cameFromBot = this.checkIfFromBot();

        this.init();
        this.setupIntersectionObserver();
    }

    init() {
        // Закрытие по крестику
        this.popup.querySelector('.popup-close').addEventListener('click', () => this.hidePopup());

        // Закрытие по клику вне popup
        this.popup.addEventListener('click', (e) => {
            if (e.target === this.popup) this.hidePopup();
        });

        // Закрытие по ESC
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.popup.classList.contains('active')) {
                this.hidePopup();
            }
        });
    }

    checkIfFromBot() {
        return window.isFromTelegramBot ? window.isFromTelegramBot() : false;
    }

    setupIntersectionObserver() {
        if (this.cameFromBot) {
            console.log('User came from Telegram bot, skipping chatbot popup');
            return;
        }

        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting && !this.hasShown && !this.cameFromBot) {
                        // Ждем 2 секунды после появления секции
                        setTimeout(() => {
                            this.showPopup();
                            this.hasShown = true;
                        }, 2000);
                    }
                });
            },
            {
                threshold: 0.5, // Секция должна быть видна хотя бы на 50%
                rootMargin: '0px'
            }
        );

        observer.observe(this.appointmentSection);
    }

    showPopup() {
        if (this.wasShown()) return;

        this.popup.classList.add('active');
        document.body.style.overflow = 'hidden';
        this.setShown();
    }

    hidePopup() {
        this.popup.classList.remove('active');
        document.body.style.overflow = '';
    }

    wasShown() {
        return sessionStorage.getItem('chatbot_popup_shown') === 'true';
    }

    setShown() {
        sessionStorage.setItem('chatbot_popup_shown', 'true');
    }
}

// Проверяем, пришел ли пользователь из Telegram-бота
function checkIfFromTelegramBot() {
    // Проверяем параметр URL
    const urlParams = new URLSearchParams(window.location.search);
    const fromBot = urlParams.get('source') === 'telegram_bot';

    // Проверяем реферер (если пришел из Telegram)
    const isFromTelegram = document.referrer.includes('t.me');

    // Проверяем sessionStorage
    const fromSessionStorage = sessionStorage.getItem('from_telegram_bot') === 'true';

    return fromBot || isFromTelegram || fromSessionStorage;
}

// Устанавливаем флаг, если пользователь пришел из бота
if (checkIfFromTelegramBot()) {
    sessionStorage.setItem('from_telegram_bot', 'true');

    // Можно также очистить параметр URL для чистоты
    if (window.history.replaceState && window.location.search.includes('source=telegram_bot')) {
        const newUrl = window.location.pathname + window.location.search.replace(/[?&]source=telegram_bot/, '').replace(/^&/, '?');
        window.history.replaceState({}, document.title, newUrl);
    }
}

// Функция для проверки (используется в ChatbotPopupManager)
window.isFromTelegramBot = function() {
    return sessionStorage.getItem('from_telegram_bot') === 'true';
};

// Инициализация только на главной странице
document.addEventListener('DOMContentLoaded', () => {
    if (window.location.pathname === '/' || window.location.pathname === '/index.html') {
        document.body.classList.add('index-page');
        new PopupManager();
        new ChatbotPopupManager();
   }
});