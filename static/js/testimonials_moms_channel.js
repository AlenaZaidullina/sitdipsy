document.addEventListener('DOMContentLoaded', function() {
    const carousel = document.querySelector('.testimonial-carousel');
    const slides = document.querySelectorAll('.testimonial-slide');
    const prevButton = document.querySelector('.carousel-button-prev');
    const nextButton = document.querySelector('.carousel-button-next');
    const indicators = document.querySelectorAll('.indicator');

    let currentIndex = 0;
    const slideCount = slides.length;

    // Инициализация карусели
    function initCarousel() {
        updateSlidePositions();
        updateIndicators();
    }

    // Обновление позиций слайдов
    function updateSlidePositions() {
        slides.forEach((slide, index) => {
            slide.classList.remove('prev', 'active', 'next');

            if (index === currentIndex) {
                slide.classList.add('active');
            } else if (index === (currentIndex - 1 + slideCount) % slideCount) {
                slide.classList.add('prev');
            } else if (index === (currentIndex + 1) % slideCount) {
                slide.classList.add('next');
            } else {
                // Скрываем остальные слайды
                slide.style.opacity = '0';
                slide.style.transform = 'scale(0.7)';
                slide.style.zIndex = '0';
            }
        });
    }

    // Обновление индикаторов
    function updateIndicators() {
        indicators.forEach((indicator, index) => {
            indicator.classList.toggle('active', index === currentIndex);
        });
    }

    // Переход к следующему слайду
    function nextSlide() {
        currentIndex = (currentIndex + 1) % slideCount;
        updateCarousel();
    }

    // Переход к предыдущему слайду
    function prevSlide() {
        currentIndex = (currentIndex - 1 + slideCount) % slideCount;
        updateCarousel();
    }

    // Переход к конкретному слайду
    function goToSlide(index) {
        currentIndex = index;
        updateCarousel();
    }

    // Обновление всей карусели
    function updateCarousel() {
        updateSlidePositions();
        updateIndicators();
    }

    // Обработчики событий для кнопок
    nextButton.addEventListener('click', nextSlide);
    prevButton.addEventListener('click', prevSlide);

    // Обработчики для индикаторов
    indicators.forEach((indicator, index) => {
        indicator.addEventListener('click', () => goToSlide(index));
    });

    // Swipe для мобильных устройств
    let startX = 0;
    let endX = 0;

    carousel.addEventListener('touchstart', (e) => {
        startX = e.touches[0].clientX;
    });

    carousel.addEventListener('touchend', (e) => {
        endX = e.changedTouches[0].clientX;
        handleSwipe();
    });

    function handleSwipe() {
        const swipeThreshold = 50;

        if (startX - endX > swipeThreshold) {
            // Свайп влево - следующий слайд
            nextSlide();
        } else if (endX - startX > swipeThreshold) {
            // Свайп вправо - предыдущий слайд
            prevSlide();
        }
    }

    // Инициализируем карусель
    initCarousel();

    // Автопрокрутка (опционально)
    // setInterval(nextSlide, 5000);
});