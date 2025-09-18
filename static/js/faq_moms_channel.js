        document.addEventListener('DOMContentLoaded', function() {
            const faqItems = document.querySelectorAll('.faq-item');

            faqItems.forEach(item => {
                const question = item.querySelector('.faq-question');

                question.addEventListener('click', () => {
                    // Закрываем все открытые элементы
                    faqItems.forEach(otherItem => {
                        if (otherItem !== item && otherItem.classList.contains('active')) {
                            otherItem.classList.remove('active');
                        }
                    });

                    // Переключаем текущий элемент
                    item.classList.toggle('active');
                });
            });

            // Открываем первый элемент по умолчанию
            if (faqItems.length > 0) {
                faqItems[0].classList.add('active');
            }
        });