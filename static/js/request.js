document.addEventListener('DOMContentLoaded', function() {
    const circlesContainer = document.querySelector('.circles-container-requests');
    const circles = document.querySelectorAll('.circle-requests');

    if (window.innerWidth <= 528) {
        // Функция для активации центрального круга
        function activateCenterCircle() {
            const containerRect = circlesContainer.getBoundingClientRect();
            const containerCenter = containerRect.left + containerRect.width / 2;

            circles.forEach(circle => {
                const circleRect = circle.getBoundingClientRect();
                const circleCenter = circleRect.left + circleRect.width / 2;

                // Если круг находится в центре контейнера
                if (Math.abs(circleCenter - containerCenter) < circleRect.width / 3) {
                    circle.classList.add('active');
                } else {
                    circle.classList.remove('active');
                }
            });
        }

        // Инициализация при загрузке
        activateCenterCircle();

        // Обработка события прокрутки
        circlesContainer.addEventListener('scroll', activateCenterCircle);

        // Автоматическая прокрутка к центру при загрузке (опционально)
        setTimeout(() => {
            circlesContainer.scrollLeft = circlesContainer.scrollWidth / 2 - circlesContainer.offsetWidth / 2;
        }, 100);

        // Добавляем инерцию для плавной прокрутки
        let isScrolling;
        circlesContainer.addEventListener('scroll', () => {
            window.clearTimeout(isScrolling);
            isScrolling = setTimeout(() => {
                // Находим ближайший круг к центру и скроллим к нему
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
                    closestCircle.scrollIntoView({
                        behavior: 'smooth',
                        inline: 'center',
                        block: 'nearest'
                    });
                }
            }, 150); // Задержка перед автоматическим выравниванием
        });
    }
});
