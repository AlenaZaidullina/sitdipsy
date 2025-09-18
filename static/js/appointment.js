document.addEventListener('DOMContentLoaded', function() {
    // Текущая дата
    let currentDate = new Date();
    let selectedDate = null;
    let selectedTime = null;
    let availableDates = [];

    // Элементы DOM
    const calendarDays = document.getElementById('calendar-days');
    const currentMonthYear = document.getElementById('current-month-year');
    const prevMonthBtn = document.getElementById('prev-month');
    const nextMonthBtn = document.getElementById('next-month');
    const selectedDateInput = document.getElementById('selected-date');
    const timeModal = document.getElementById('time-modal');
    const closeModal = document.querySelector('.close-modal');
    const selectedDaySpan = document.getElementById('selected-day');
    const timeList = document.getElementById('time-list');
    const consultationType = document.getElementById('consultation-type');
    const paymentNotice = document.getElementById('payment-notice');
    const consultationForm = document.getElementById('consultation-form');

    // Валидация телефона
    const phoneInput = document.getElementById('phone');
    phoneInput.addEventListener('input', function() {
        // Удаляем все нецифровые символы, кроме плюса
        let phoneNumber = this.value.replace(/[^\d+]/g, '');

        // Если в начале +7, оставляем как есть
        if (phoneNumber.startsWith('+7')) {
            phoneNumber = '+7' + phoneNumber.substring(2).replace(/\D/g, '');
            if (phoneNumber.length > 12) phoneNumber = phoneNumber.substring(0, 12);
        }
        // Если начинается с 7 или 8, приводим к формату +7
        else if (phoneNumber.startsWith('7') || phoneNumber.startsWith('8')) {
            phoneNumber = '+7' + phoneNumber.substring(1).replace(/\D/g, '');
            if (phoneNumber.length > 12) phoneNumber = phoneNumber.substring(0, 12);
        }
        // Для других случаев просто обрезаем
        else {
            phoneNumber = phoneNumber.replace(/\D/g, '');
            if (phoneNumber.length > 11) phoneNumber = phoneNumber.substring(0, 11);
        }

        this.value = phoneNumber;
    });

    // Показ подсказки при фокусе на поле телефона
    phoneInput.addEventListener('focus', function() {
        this.nextElementSibling.nextElementSibling.style.display = 'block';
    });

    phoneInput.addEventListener('blur', function() {
        this.nextElementSibling.nextElementSibling.style.display = 'none';
    });

    // Дополнение валидации при отправке формы
    const originalFormSubmit = consultationForm.onsubmit;
    consultationForm.onsubmit = function(event) {
        const phoneNumber = phoneInput.value.replace(/\D/g, '');

        // Проверяем российский номер (11 цифр, начинается с 7 или 8)
        if (!/^(7|8)\d{10}$/.test(phoneNumber)) {
            alert('Пожалуйста, введите корректный российский номер телефона (11 цифр, начинается с 7 или 8)');
            phoneInput.focus();
            event.preventDefault();
            return false;
        }

        // Если у вас был другой обработчик, вызываем его
        if (originalFormSubmit) {
            return originalFormSubmit.call(this, event);
        }

        return true;
    };

    // Инициализация календаря
    function initCalendar() {
        // Устанавливаем правильный текущий месяц и год
        updateCalendarHeader(currentDate);

        // Рендерим календарь с пустыми днями сначала
        renderCalendar(currentDate);

        // Загружаем доступные даты и обновляем календарь
        loadAvailableDates().then(() => {
            updateCalendarDays();
        });

        // Обработчики событий для навигации по месяцам
        prevMonthBtn.addEventListener('click', () => {
            currentDate.setMonth(currentDate.getMonth() - 1);
            updateCalendarHeader(currentDate);
            renderCalendar(currentDate);
            loadAvailableDates().then(() => {
                updateCalendarDays();
            });
        });

        nextMonthBtn.addEventListener('click', () => {
            currentDate.setMonth(currentDate.getMonth() + 1);
            updateCalendarHeader(currentDate);
            renderCalendar(currentDate);
            loadAvailableDates().then(() => {
                updateCalendarDays();
            });
        });

        // Обработчик для закрытия модального окна
        closeModal.addEventListener('click', () => {
            timeModal.style.display = 'none';
        });

        // Закрытие модального окна при клике вне его
        window.addEventListener('click', (event) => {
            if (event.target === timeModal) {
                timeModal.style.display = 'none';
            }
        });

        // Обработчик изменения типа консультации
        consultationType.addEventListener('change', function() {
            if (this.value === 'first') {
                paymentNotice.style.display = 'block';
            } else {
                paymentNotice.style.display = 'none';
            }
        });

        // Обработчик отправки формы
        consultationForm.addEventListener('submit', function(e) {
            e.preventDefault();


            // Проверка согласия
            if (!document.querySelector('input[name="pd_consent"]')?.checked) {
                    alert('Для записи на консультацию необходимо подтвердить согласие на обработку персональных данных');
                    return false;
                }

            // Проверка возраста
            if (!document.querySelector('input[name="age_confirm"]')?.checked) {
                alert('Для записи на консультацию необходимо подтвердить, что вам есть 18 лет');
                return false;
            }

            // Собираем данные формы
            const formData = {
                full_name: document.getElementById('fullname').value,
                phone: document.getElementById('phone').value,
                consultation_type: consultationType.value,
                selected_date: selectedDateInput.value,
                pd_consent: document.querySelector('input[name="pd_consent"]').checked
            };

            // Показываем индикатор загрузки
            const submitBtn = consultationForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'Записываю...';
            submitBtn.disabled = true;

            fetch('/appt/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                },
                body: JSON.stringify(formData)
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(errorData => {
                        throw new Error(errorData.message || 'Network response was not ok');
                    });
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    showConfirmationModal(data);
                } else {
                    alert('Ошибка: ' + (data.message || 'Неизвестная ошибка'));
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Ошибка: ' + error.message);

                // Если время занято, обновляем доступные временные слоты
                if (error.message.includes('занято') || error.message.includes('недоступно')) {
                    if (selectedDate) {
                        showTimeModal(selectedDate); // Показываем обновленный список времени
                    }
                }
            })
            .finally(() => {
                // Восстанавливаем кнопку
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
            });
        });
    }

    // Обновление заголовка календаря
    function updateCalendarHeader(date) {
        const monthNames = ['ЯНВАРЬ', 'ФЕВРАЛЬ', 'МАРТ', 'АПРЕЛЬ', 'МАЙ', 'ИЮНЬ',
                          'ИЮЛЬ', 'АВГУСТ', 'СЕНТЯБРЬ', 'ОКТЯБРЬ', 'НОЯБРЬ', 'ДЕКАБРЬ'];
        const year = date.getFullYear();
        const month = date.getMonth();
        currentMonthYear.textContent = `${monthNames[month]} / ${year}`;
    }

    // Загрузка доступных дат с сервера
    function loadAvailableDates() {
        return fetch('/appt/api/available-dates/')
            .then(response => response.json())
            .then(data => {
                availableDates = data.available_dates || [];
                return availableDates;
            })
            .catch(error => {
                console.error('Error loading available dates:', error);
                availableDates = [];
                return availableDates;
            });
    }

    // Рендер календаря для указанного месяца и года
    function renderCalendar(date) {
        const year = date.getFullYear();
        const month = date.getMonth();

        // Первый день месяца
        const firstDay = new Date(year, month, 1);
        // Последний день месяца
        const lastDay = new Date(year, month + 1, 0);
        // День недели первого дня месяца (0 - воскресенье, 1 - понедельник и т.д.)
        const firstDayOfWeek = firstDay.getDay() === 0 ? 6 : firstDay.getDay() - 1;

        // Очистка календаря
        calendarDays.innerHTML = '';

        // Пустые ячейки для дней предыдущего месяца
        for (let i = 0; i < firstDayOfWeek; i++) {
            const emptyDay = document.createElement('div');
            emptyDay.className = 'calendar-day empty';
            calendarDays.appendChild(emptyDay);
        }

        // Ячейки для дней текущего месяца
        for (let i = 1; i <= lastDay.getDate(); i++) {
            const day = document.createElement('div');
            day.className = 'calendar-day';
            day.textContent = i;

            // Форматирование даты для сравнения
            const formattedDate = `${year}-${String(month + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`;

            // Проверка, доступна ли дата для записи
            if (availableDates.includes(formattedDate)) {
                day.classList.add('available');
                day.addEventListener('click', () => selectDate(day, formattedDate));
            } else {
                day.classList.add('disabled');
            }

            calendarDays.appendChild(day);
        }
    }

    // Обновление отображения дней в календаре
    function updateCalendarDays() {
        const days = document.querySelectorAll('.calendar-day:not(.empty)');
        const year = currentDate.getFullYear();
        const month = currentDate.getMonth() + 1;

        days.forEach(day => {
            const dayNumber = day.textContent;
            const formattedDate = `${year}-${String(month).padStart(2, '0')}-${String(dayNumber).padStart(2, '0')}`;

            // Удаляем все старые обработчики событий
            const newDay = day.cloneNode(true);
            day.parentNode.replaceChild(newDay, day);

            if (availableDates.includes(formattedDate)) {
                newDay.classList.add('available');
                newDay.classList.remove('disabled');
                newDay.addEventListener('click', () => selectDate(newDay, formattedDate));
            } else {
                newDay.classList.remove('available');
                newDay.classList.add('disabled');
                newDay.removeEventListener('click', () => selectDate(newDay, formattedDate));
            }
        });
    }

    // Выбор даты
    function selectDate(dayElement, dateString) {
        // Снятие выделения со всех дней
        document.querySelectorAll('.calendar-day').forEach(day => {
            day.classList.remove('selected');
        });

        // Выделение выбранного дня
        dayElement.classList.add('selected');
        selectedDate = dateString;

        // Показ модального окна с выбором времени
        showTimeModal(dateString);
    }

    // Показ модального окна с выбором времени
    function showTimeModal(dateString) {
        fetch(`/appt/api/available-times/${dateString}/`)
            .then(response => response.json())
            .then(data => {
                const date = new Date(dateString);
                const options = { day: 'numeric', month: 'long' };
                const formattedDate = date.toLocaleDateString('ru-RU', options);

                selectedDaySpan.textContent = formattedDate;
                timeList.innerHTML = '';

                if (data.available_times && data.available_times.length === 0) {
                    timeList.innerHTML = '<p>Нет доступных временных слотов</p>';
                } else if (data.available_times) {
                    data.available_times.forEach(time => {
                        const timeSlot = document.createElement('button');
                        timeSlot.className = 'time-slot';
                        timeSlot.textContent = time;
                        timeSlot.addEventListener('click', () => {
                            selectTime(timeSlot, time);
                        });
                        timeList.appendChild(timeSlot);
                    });
                } else {
                    timeList.innerHTML = '<p>Ошибка загрузки временных слотов</p>';
                }

                timeModal.style.display = 'block';
            })
            .catch(error => {
                console.error('Error loading available times:', error);
                timeList.innerHTML = '<p>Ошибка загрузки временных слотов</p>';
                timeModal.style.display = 'block';
            });
    }

    // Выбор времени
    function selectTime(timeElement, time) {
        // Снятие выделения со всех временных слотов
        document.querySelectorAll('.time-slot').forEach(slot => {
            slot.classList.remove('selected');
        });

        // Выделение выбранного времени
        timeElement.classList.add('selected');
        selectedTime = time;

        // Обновление поля с выбранной датой и временем
        const date = new Date(selectedDate);
        const options = { day: 'numeric', month: 'long' };
        const formattedDate = date.toLocaleDateString('ru-RU', options);
        selectedDateInput.value = `${formattedDate}, ${time}`;

        // Закрытие модального окна
        setTimeout(() => {
            timeModal.style.display = 'none';
        }, 300);
    }

    // Функция показа модального окна подтверждения записи
    function showConfirmationModal(data) {
        const confirmationModal = document.createElement('div');
        confirmationModal.className = 'modal';
        confirmationModal.id = 'confirmation-modal';
        confirmationModal.innerHTML = `
            <div class="modal-content">
                <span class="close-modal">&times;</span>
                <h3>Вы записаны на консультацию</h3>
                <p>Дата: ${selectedDateInput.value}</p>
                <p>Тип консультации: ${consultationType.options[consultationType.selectedIndex].text}</p>
                <div class="confirmation-buttons">
                    <button id="pay-now-btn" class="submit-btn">Перейти в Telegram бот</button>
                    <button id="close-confirmation-btn" class="submit-btn">Закрыть</button>
                </div>
            </div>
        `;

        document.body.appendChild(confirmationModal);

        // Показываем модальное окно
        confirmationModal.style.display = 'block';

        // Обработчики событий для кнопок
        document.getElementById('pay-now-btn').addEventListener('click', function() {
            // Открываем Telegram бот в новой вкладке
            window.open('https://t.me/DaiOkoshkidiana_bot', '_blank');
        });

        document.getElementById('close-confirmation-btn').addEventListener('click', function() {
            confirmationModal.style.display = 'none';
            document.body.removeChild(confirmationModal);
        });

        // Закрытие при клике на крестик
        confirmationModal.querySelector('.close-modal').addEventListener('click', function() {
            confirmationModal.style.display = 'none';
            document.body.removeChild(confirmationModal);
        });

        // Закрытие при клике вне модального окна
        window.addEventListener('click', function(event) {
            if (event.target === confirmationModal) {
                confirmationModal.style.display = 'none';
                document.body.removeChild(confirmationModal);
            }
        });
    }

    // Инициализация календаря
    initCalendar();
});