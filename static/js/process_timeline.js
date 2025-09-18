document.addEventListener('DOMContentLoaded', function() {
    const desktopSvg = document.querySelector('.desktop-line');
    const mobileSvg = document.querySelector('.mobile-line');
    const descriptionBox = document.getElementById('description-box');
    const descriptionTitle = document.getElementById('description-title');
    const descriptionText = document.getElementById('description-text');

    let activeCircle = null;
    let isMobile = window.innerWidth < 768;

    // Создаем шаблон круга
    function createCircle(number, title, text, isTopLabel) {
        const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
        g.className.baseVal = "numbered-circle";
        g.setAttribute('data-number', number);
        g.setAttribute('data-title', title);
        g.setAttribute('data-text', text);

        const labelClass = isTopLabel ? 'point-label top' : 'point-label bottom';
        const labelY = isTopLabel ? '-70' : '70';
        const connectorY2 = isTopLabel ? '-40' : '60';
        const hintY = isTopLabel ? '30' : '-30';

        g.innerHTML = `
            <text class="${labelClass}" x="0" y="${labelY}" fill="#333">
                <tspan x="0" dy="0">${title.split(' ').slice(0, 3).join(' ')}</tspan>
                <tspan x="0" dy="16">${title.split(' ').slice(3).join(' ')}</tspan>
            </text>
            <line class="connector-line" x1="0" y1="0" x2="0" y2="${connectorY2}" stroke="#76805D" stroke-width="1"/>
            <circle cx="0" cy="0" r="18" fill="white" stroke="#76805D" stroke-width="1.5"/>
            <circle cx="0" cy="0" r="16" fill="#76805D"/>
            <text x="0" y="0" fill="white" text-anchor="middle" dominant-baseline="middle" font-size="12" font-weight="bold">${number}</text>
        `;

        g.addEventListener('click', function() {
            showDescription(this);
        });

        return g;
    }

    // Данные для кругов
        const circleData = [
            {
                number: 1,
                title: "Знакомство и понимание вашей ситуации",
                text: `На первой встрече мы познакомимся, и я аккуратно расспрошу вас о том, что вас беспокоит — будь то тревога, стресс, сложности в отношениях или что-то ещё. Вы сможете рассказать о себе в комфортном темпе, без давления.

        Это нужно, чтобы я могла лучше понять, как вам помочь, а вы — как вообще строится терапия. Вместе мы определим ваши цели: например, «хочу меньше тревожиться на работе» или «научиться справляться с чувством одиночества».

        Важно: вы не обязаны сразу раскрывать всё — говорите только о том, чем готовы поделиться.`,
                topLabel: true
            },
            {
                number: 2,
                title: "Разбираем, как мысли влияют на эмоции",
                text: `Здесь я помогу вам заметить, как ваши мысли (например, «У меня ничего не получится») связаны с эмоциями (страх, грусть) и действиями (избегание, прокрастинация). Мы будем разбирать это на примерах из вашей жизни.

        Это как инструкция к вашему собственному мышлению — когда вы поймёте эти связи, вам станет проще ими управлять.

        Например, если вы боитесь публичных выступлений, мы исследуем, какие именно мысли («Я опозорюсь») усиливают этот страх.`,
                topLabel: false
            },
            {
                number: 3,
                title: "Учимся работать с тревожными мыслями",
                text: `Вы начнёте замечать и записывать свои тревожные или пессимистичные мысли — например, в дневник. А потом мы вместе проверим, насколько они соответствуют реальности.

        Часто наш мозг преувеличивает риски («Если я ошибусь, меня уволят»), и терапия помогает найти более взвешенный взгляд на ситуацию.

        Я не буду просто говорить «думайте позитивнее» — вместо этого мы найдём альтернативные, более гибкие мысли, которые лучше соответствуют реальности.`,
                topLabel: true
            },
            {
                number: 4,
                title: "Эксперименты: проверяем мысли на практике",
                text: `Мы будем пробовать небольшие эксперименты. Например, если вы уверены, что люди осудят вас за ошибку в докладе, мы проверим это на деле (и обычно оказывается, что никто даже не заметил или не придал значения).

        Это помогает убедиться, что многие страхи — просто «ложная тревога», а не реальная угроза.`,
                topLabel: false
            },
            {
                number: 5,
                title: "Работа с глубинными установками",
                text: `Здесь мы исследуем ваши давние убеждения, которые могли формироваться годами — например, «Я должен всё делать идеально» или «Я не заслуживаю любви». Вы поймёте, откуда они взялись и как сейчас мешают вам жить.

        Наша задача — не просто осознать их, но и постепенно заменить на более полезные и добрые к себе.`,
                topLabel: true
            },
            {
                number: 6,
                title: "Закрепляем результаты и завершаем терапию",
                text: `В конце мы подведём итоги: что изменилось, какие навыки вы освоили. Я дам вам инструменты, чтобы вы могли применять их самостоятельно.

        Терапия — это не навсегда. Но если в будущем вы столкнётесь с новыми сложностями, всегда можно вернуться на несколько сессий для поддержки.`,
                topLabel: false
            }
        ];

    // Позиции для десктопной линии
    const desktopPositions = [0.02, 0.20, 0.35, 0.5, 0.65, 0.80];

    // Позиции для мобильной линии (адаптированы под кривую)
    const mobilePositions = [0.00, 0.1, 0.38, 0.53, 0.80, 1];

    // Инициализация кругов
    function initCircles() {
        // Очищаем предыдущие круги
        document.querySelectorAll('.numbered-circle').forEach(circle => circle.remove());

        const currentSvg = isMobile ? mobileSvg : desktopSvg;
        const pathId = isMobile ? 'mobile-wave-line' : 'desktop-wave-line';
        const path = document.getElementById(pathId);
        const positions = isMobile ? mobilePositions : desktopPositions;

        if (!path) return;

        const pathLength = path.getTotalLength();

        circleData.forEach((data, index) => {
            const position = pathLength * positions[index];
            const point = path.getPointAtLength(position);

            const circle = createCircle(data.number, data.title, data.text, data.topLabel);
            circle.setAttribute('transform', `translate(${point.x}, ${point.y})`);

            currentSvg.appendChild(circle);
        });
    }

    // Показ описания
    function showDescription(circle) {
        if (activeCircle === circle) {
            descriptionBox.classList.remove('active');
            activeCircle = null;
            return;
        }

        descriptionTitle.textContent = circle.getAttribute('data-title');
        descriptionText.textContent = circle.getAttribute('data-text');

        descriptionBox.classList.add('active');
        activeCircle = circle;

        descriptionBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    // Обработчик ресайза
    function handleResize() {
        const newIsMobile = window.innerWidth < 768;

        if (newIsMobile !== isMobile) {
            isMobile = newIsMobile;
            initCircles();
        }
    }

    // Инициализация
    initCircles();
    window.addEventListener('resize', handleResize);
});