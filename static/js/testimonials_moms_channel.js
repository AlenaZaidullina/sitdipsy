document.addEventListener('DOMContentLoaded', function() {
    console.log('Testimonials carousel script loaded');

    const carousel = document.querySelector('.testimonial-carousel');
    const slides = document.querySelectorAll('.testimonial-slide');
    const prevButton = document.querySelector('.carousel-button-prev');
    const nextButton = document.querySelector('.carousel-button-next');
    const indicators = document.querySelectorAll('.indicator');
    const jsStatus = document.getElementById('js-status');

    // Обновляем статус загрузки JS
    if (jsStatus) {
        jsStatus.textContent = 'Да';
    }

    // Если нет слайдов, выходим
    if (slides.length === 0) {
        console.log('No slides found');
        return;
    }

    console.log(`Found ${slides.length} slides`);

    let currentIndex = 0;
    const slideCount = slides.length;

    // Инициализация карусели
    function initCarousel() {
        console.log('Initializing carousel');

        // Показываем все слайды изначально
        slides.forEach((slide, index) => {
            slide.style.display = 'block';
            slide.style.transition = 'all 0.5s ease';
        });

        updateSlidePositions();
        updateIndicators();

        // Показываем кнопки только если есть больше 1 слайда
        if (slideCount <= 1) {
            prevButton.style.display = 'none';
            nextButton.style.display = 'none';
        }
    }

    // Обновление позиций слайдов
    function updateSlidePositions() {
        slides.forEach((slide, index) => {
            slide.style.opacity = '0';
            slide.style.transform = 'scale(0.7)';
            slide.style.zIndex = '0';
            slide.style.position = 'absolute';
            slide.style.top = '0';
            slide.style.left = '0';
            slide.style.width = '100%';

            if (index === currentIndex) {
                slide.style.opacity = '1';
                slide.style.transform = 'scale(1)';
                slide.style.zIndex = '2';
            } else if (index === (currentIndex - 1 + slideCount) % slideCount) {
                slide.style.opacity = '0.5';
                slide.style.transform = 'translateX(-100%) scale(0.8)';
                slide.style.zIndex = '1';
            } else if (index === (currentIndex + 1) % slideCount) {
                slide.style.opacity = '0.5';
                slide.style.transform = 'translateX(100%) scale(0.8)';
                slide.style.zIndex = '1';
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
        if (index >= 0 && index < slideCount) {
            currentIndex = index;
            updateCarousel();
        }
    }

    // Обновление всей карусели
    function updateCarousel() {
        updateSlidePositions();
        updateIndicators();
    }

    // Обработчики событий для кнопок
    if (prevButton) {
        prevButton.addEventListener('click', prevSlide);
    }

    if (nextButton) {
        nextButton.addEventListener('click', nextSlide);
    }

    // Обработчики для индикаторов
    indicators.forEach((indicator, index) => {
        indicator.addEventListener('click', () => goToSlide(index));
    });

    // Swipe для мобильных устройств
    if (carousel) {
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
                nextSlide();
            } else if (endX - startX > swipeThreshold) {
                prevSlide();
            }
        }
    }

    // Инициализируем карусель
    initCarousel();

    // Автопрокрутка
    // let autoScroll = setInterval(nextSlide, 5000);

    // Останавливаем автопрокрутку при наведении
    // carousel.addEventListener('mouseenter', () => clearInterval(autoScroll));
    // carousel.addEventListener('mouseleave', () => {
    //     autoScroll = setInterval(nextSlide, 5000);
    // });
});