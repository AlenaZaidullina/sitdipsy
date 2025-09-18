document.addEventListener('DOMContentLoaded', () => {
    // Функция для анимации элементов при прокрутке
    const animateElements = (elements, className) => {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add(className);
                }
            });
        }, { threshold: 0.1 });

        elements.forEach(el => observer.observe(el));
    };

    // Анимация заголовка
    const title = document.querySelector('.section-title');
    if (title) animateElements([title], 'visible');

    // Анимация пунктов таймлайна
    const timelineItems = document.querySelectorAll('.timeline-item');
    if (timelineItems.length) {
        animateElements(timelineItems, 'visible');

        // Задержка для последовательного появления пунктов
        timelineItems.forEach((item, index) => {
            item.style.transitionDelay = `${0.2 + index * 0.2}s`;
        });
    }

    // Анимация декоративной линии
    const line = document.querySelector('.decorative-line');
    if (line) animateElements([line], 'visible');

    // Работа с модальным окном для дипломов
    const diplomaLinks = document.querySelectorAll('.diploma-link[data-diploma-urls]');
    const modal = document.getElementById('diplomaModal');
    const modalImg = document.getElementById('diplomaImage');
    const closeModal = document.getElementById('closeModals');
    const prevBtn = document.getElementById('prevDiploma');
    const nextBtn = document.getElementById('nextDiploma');

    let currentImages = [];
    let currentIndex = 0;

    if (diplomaLinks.length && modal && modalImg && closeModal && prevBtn && nextBtn) {
        // Обработка кликов по дипломам
        diplomaLinks.forEach(link => {
            link.addEventListener('click', function() {
                const urls = this.getAttribute('data-diploma-urls').split(',');
                if (urls.length > 0 && urls[0] !== '') {
                    currentImages = urls;
                    currentIndex = 0;
                    showImage(currentIndex);
                    modal.style.display = 'flex';
                    document.body.style.overflow = 'hidden';
                }
            });
        });

        // Функция показа текущего изображения
        function showImage(index) {
            if (currentImages.length > 0) {
                modalImg.src = currentImages[index];
                prevBtn.style.display = index > 0 ? 'block' : 'none';
                nextBtn.style.display = index < currentImages.length - 1 ? 'block' : 'none';
            }
        }

        // Кнопка "Назад"
        prevBtn.addEventListener('click', () => {
            if (currentIndex > 0) {
                currentIndex--;
                showImage(currentIndex);
            }
        });

        // Кнопка "Вперед"
        nextBtn.addEventListener('click', () => {
            if (currentIndex < currentImages.length - 1) {
                currentIndex++;
                showImage(currentIndex);
            }
        });

        // Закрытие модального окна
        closeModal.addEventListener('click', () => {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        });

        // Закрытие по клику вне изображения
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
        });

        // Закрытие по клавише Esc
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && modal.style.display === 'flex') {
                modal.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
        });
    }
});