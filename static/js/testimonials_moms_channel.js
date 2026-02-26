document.addEventListener('DOMContentLoaded', function() {
    console.log('Testimonials carousel script loaded');

    const slides = document.querySelectorAll('.testimonial-slide');
    const prevButton = document.querySelector('.carousel-button-prev');
    const nextButton = document.querySelector('.carousel-button-next');
    const indicators = document.querySelectorAll('.indicator');
    const jsStatus = document.getElementById('js-status');

    // Обновляет статус загрузки JS
    if (jsStatus) {
        jsStatus.textContent = 'Да';
    }

    // Если нет слайдов, выходит
    if (slides.length === 0) {
        console.log('No slides found');
        return;
    }

    console.log(`Found ${slides.length} slides`);

    let currentIndex = 0;
    const slideCount = slides.length;

    // Показать слайд по индексу
    function showSlide(index) {
        // Скрывает все слайды
        slides.forEach(slide => {
            slide.classList.remove('active');
        });

        // Убирает активный класс у всех индикаторов
        indicators.forEach(indicator => {
            indicator.classList.remove('active');
        });

        // Показывает нужный слайд
        slides[index].classList.add('active');

        // Активирует соответствующий индикатор
        if (indicators[index]) {
            indicators[index].classList.add('active');
        }

        currentIndex = index;
    }

    // Следующий слайд
    function nextSlide() {
        let newIndex = currentIndex + 1;
        if (newIndex >= slideCount) {
            newIndex = 0;
        }
        showSlide(newIndex);
    }

    // Предыдущий слайд
    function prevSlide() {
        let newIndex = currentIndex - 1;
        if (newIndex < 0) {
            newIndex = slideCount - 1;
        }
        showSlide(newIndex);
    }

    // Показывает первый слайд при загрузке
    showSlide(0);

    // Скрываются кнопки если слайд всего 1
    if (slideCount <= 1) {
        if (prevButton) prevButton.style.display = 'none';
        if (nextButton) nextButton.style.display = 'none';
    }

    // Обработчики событий
    if (prevButton) {
        prevButton.addEventListener('click', prevSlide);
    }

    if (nextButton) {
        nextButton.addEventListener('click', nextSlide);
    }

    // Обработчики для индикаторов
    indicators.forEach((indicator, index) => {
        indicator.addEventListener('click', () => {
            showSlide(index);
        });
    });

    // Клавиатурная навигация (для доступности)
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft') {
            prevSlide();
        } else if (e.key === 'ArrowRight') {
            nextSlide();
        }
    });
});