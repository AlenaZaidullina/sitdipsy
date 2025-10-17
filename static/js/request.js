document.addEventListener('DOMContentLoaded', function() {
    const circlesContainer = document.querySelector('.circles-container-requests');
    const circles = document.querySelectorAll('.circle-requests');

    // Проверяем, мобильное ли устройство или touch-симуляция
    function isTouchDevice() {
        return (('ontouchstart' in window) ||
            (navigator.maxTouchPoints > 0) ||
            (navigator.msMaxTouchPoints > 0));
    }

    if (window.innerWidth <= 528 || isTouchDevice()) {
        let scrollTimeout;
        let isProgrammaticScroll = false;

        // Функция для активации центрального круга
        function activateCenterCircle() {
            if (isProgrammaticScroll) return;

            const containerRect = circlesContainer.getBoundingClientRect();
            const containerCenter = containerRect.left + containerRect.width / 2;

            let activeCircle = null;
            let minDistance = Infinity;

            circles.forEach(circle => {
                const circleRect = circle.getBoundingClientRect();
                const circleCenter = circleRect.left + circleRect.width / 2;
                const distance = Math.abs(circleCenter - containerCenter);

                // Снимаем активный класс со всех кругов
                circle.classList.remove('active');

                // Находим ближайший к центру круг
                if (distance < minDistance) {
                    minDistance = distance;
                    activeCircle = circle;
                }
            });

            // Активируем ближайший круг
            if (activeCircle && minDistance < activeCircle.offsetWidth / 2) {
                activeCircle.classList.add('active');
            }
        }

        // Функция для плавного выравнивания
        function smoothSnapToCenter() {
            const containerRect = circlesContainer.getBoundingClientRect();
            const containerCenter = containerRect.left + containerRect.width / 2;

            let closestCircle = null;
            let minDistance = Infinity;

            circles.forEach(circle => {
                const circleRect = circle.getBoundingClientRect();
                const circleCenter = circleRect.left + circleRect.width / 2;
                const distance = Math.abs(circleCenter - containerCenter);

                if (distance < minDistance) {
                    minDistance = distance;
                    closestCircle = circle;
                }
            });

            if (closestCircle) {
                isProgrammaticScroll = true;

                closestCircle.scrollIntoView({
                    behavior: 'smooth',
                    inline: 'center',
                    block: 'nearest'
                });

                // Снимаем флаг после завершения анимации
                setTimeout(() => {
                    isProgrammaticScroll = false;
                }, 500);
            }
        }

        // Инициализация
        function initCarousel() {
            activateCenterCircle();

            // Центрируем при загрузке
            setTimeout(() => {
                if (circles.length > 0) {
                    isProgrammaticScroll = true;
                    circles[Math.floor(circles.length / 2)].scrollIntoView({
                        behavior: 'smooth',
                        inline: 'center',
                        block: 'nearest'
                    });

                    setTimeout(() => {
                        isProgrammaticScroll = false;
                        activateCenterCircle();
                    }, 600);
                }
            }, 100);
        }

        // Обработчики событий
        circlesContainer.addEventListener('scroll', () => {
            activateCenterCircle();

            // Автоматическое выравнивание после остановки прокрутки
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(smoothSnapToCenter, 150);
        });

        // Обработка кликов для мгновенного перехода
        circles.forEach(circle => {
            circle.addEventListener('click', () => {
                isProgrammaticScroll = true;

                circle.scrollIntoView({
                    behavior: 'smooth',
                    inline: 'center',
                    block: 'nearest'
                });

                circles.forEach(c => c.classList.remove('active'));
                circle.classList.add('active');

                setTimeout(() => {
                    isProgrammaticScroll = false;
                }, 500);
            });
        });

        // Обработка touch событий для лучшей производительности
        circlesContainer.addEventListener('touchstart', () => {
            clearTimeout(scrollTimeout);
        });

        circlesContainer.addEventListener('touchend', () => {
            scrollTimeout = setTimeout(smoothSnapToCenter, 100);
        });

        // Инициализируем карусель
        initCarousel();

        // Переинициализация при изменении размера окна
        window.addEventListener('resize', () => {
            if (window.innerWidth <= 528) {
                initCarousel();
            }
        });
    } else {
        // Для десктопов оставляем только hover-эффекты
        circles.forEach(circle => {
            circle.addEventListener('mouseenter', () => {
                circle.style.transform = 'scale(1.05)';
                circle.style.zIndex = '10';
                circle.style.boxShadow = '0 0 15px rgba(106, 111, 76, 0.5)';
                circle.style.backgroundColor = 'var(--bg-color)';
            });

            circle.addEventListener('mouseleave', () => {
                circle.style.transform = 'scale(1)';
                circle.style.zIndex = '1';
                circle.style.boxShadow = 'none';
                circle.style.backgroundColor = 'transparent';
            });
        });
    }
});