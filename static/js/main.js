/**
 * Smart Care - Главный JavaScript файл
 * Реализация слайдера (desktop) и табов (mobile)
 */

// ===================================
// Глобальные переменные
// ===================================

let currentSlide = 0;
const totalSlides = 5;
let touchStartX = 0;
let touchEndX = 0;
let isDesktop = window.innerWidth >= 1024;

// ===================================
// DOM элементы
// ===================================

const slides = document.querySelectorAll('.slide');
const tabButtons = document.querySelectorAll('.tab-button');
const headerNavItems = document.querySelectorAll('.header-nav .nav-item');
const loader = document.getElementById('loader');

// ===================================
// Инициализация
// ===================================

document.addEventListener('DOMContentLoaded', () => {
    // Скрыть loader после загрузки
    setTimeout(() => {
        if (loader) {
            loader.classList.add('hidden');
        }
    }, 500);

    // Инициализация слайдера
    initSlider();
    
    // Установка обработчиков событий
    setupEventListeners();
    
    // Обработка изменения размера окна
    handleResize();
    
    console.log('Smart Care Demo - Initialized ✓');
});

// ===================================
// Инициализация слайдера
// ===================================

function initSlider() {
    showSlide(0);
    
    // Добавляем flip функционал для карточек команды
    initTeamCards();
}

// ===================================
// Навигация по слайдам
// ===================================

function showSlide(index) {
    // Проверка границ
    if (index < 0) {
        currentSlide = 0;
        return;
    }
    if (index >= totalSlides) {
        currentSlide = totalSlides - 1;
        return;
    }
    
    currentSlide = index;
    
    // Обновление слайдов
    slides.forEach((slide, i) => {
        if (i === currentSlide) {
            slide.classList.add('active');
        } else {
            slide.classList.remove('active');
        }
    });
    
    // Обновление табов (mobile)
    tabButtons.forEach((btn, i) => {
        if (i === currentSlide) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
    
    // Обновление header навигации (desktop)
    headerNavItems.forEach((item, i) => {
        if (i === currentSlide) {
            item.classList.add('active');
        } else {
            item.classList.remove('active');
        }
    });
    
    // Скролл наверх при смене слайда
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

function nextSlide() {
    showSlide(currentSlide + 1);
}

function prevSlide() {
    showSlide(currentSlide - 1);
}

function goToSlide(index) {
    showSlide(index);
}

// ===================================
// Обработчики событий
// ===================================

function setupEventListeners() {
    // Header навигация (desktop)
    headerNavItems.forEach((item, index) => {
        item.addEventListener('click', () => goToSlide(index));
    });
    
    // Табы (mobile)
    tabButtons.forEach((btn, index) => {
        btn.addEventListener('click', () => goToSlide(index));
    });
    
    // Обработка изменения размера окна
    window.addEventListener('resize', handleResize);
    
    // ❌ ОТКЛЮЧЕНО: Клавиатурная навигация
    // ❌ ОТКЛЮЧЕНО: Touch свайпы
    // ❌ ОТКЛЮЧЕНО: Колесо мыши
    // Навигация работает ТОЛЬКО по header кнопкам и табам
}

// ❌ ОТКЛЮЧЕНО: Клавиатурная навигация
// ❌ ОТКЛЮЧЕНО: Touch свайпы
// ❌ ОТКЛЮЧЕНО: Колесо мыши
// 
// Навигация работает ТОЛЬКО через:
// - Кнопки стрелок (← →)
// - Точки-индикаторы
// - Табы (mobile)

// Обработка изменения размера окна
function handleResize() {
    const wasDesktop = isDesktop;
    isDesktop = window.innerWidth >= 1024;
    
    // Если изменился режим (mobile <-> desktop), обновляем UI
    if (wasDesktop !== isDesktop) {
        console.log(`Режим изменён: ${isDesktop ? 'Desktop' : 'Mobile'}`);
    }
}

// ===================================
// Карточки команды (flip эффект)
// ===================================

function initTeamCards() {
    const teamCards = document.querySelectorAll('.team-card');
    
    teamCards.forEach(card => {
        const cardFront = card.querySelector('.team-card-front');
        const cardBack = card.querySelector('.team-card-back');
        const socialLinks = card.querySelectorAll('.social-link');
        
        // Для мобильных - flip по клику
        if (!isDesktop) {
            // Клик на лицевую сторону - переворачиваем
            cardFront.addEventListener('click', function(e) {
                e.stopPropagation();
                card.classList.add('flipped');
            });
            
            // Клик на обратную сторону (но не на ссылки) - переворачиваем обратно
            cardBack.addEventListener('click', function(e) {
                // Проверяем, что клик не по ссылке
                if (!e.target.closest('.social-link')) {
                    e.stopPropagation();
                    card.classList.remove('flipped');
                }
            });
            
            // Ссылки работают как обычно (не блокируем)
            socialLinks.forEach(link => {
                link.addEventListener('click', function(e) {
                    e.stopPropagation(); // Не даём карточке перевернуться
                    // Браузер откроет ссылку автоматически
                });
            });
        }
        
        // Для desktop - автоматический flip при наведении
        if (isDesktop) {
            card.addEventListener('mouseenter', function() {
                this.classList.add('flipped');
            });
            
            card.addEventListener('mouseleave', function() {
                this.classList.remove('flipped');
            });
            
            // На desktop ссылки тоже должны работать
            socialLinks.forEach(link => {
                link.addEventListener('click', function(e) {
                    e.stopPropagation();
                });
            });
        }
    });
}

// ===================================
// Плавная прокрутка для ссылок
// ===================================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        if (href !== '#') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
});

// ===================================
// Анимация элементов при скролле
// ===================================

const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Наблюдаем за карточками для анимации появления
document.addEventListener('DOMContentLoaded', () => {
    const animateElements = document.querySelectorAll(
        '.content-card, .team-card, .why-card, .timeline-item, .step-card, .feature-box'
    );
    
    animateElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
});

// ===================================
// Автоматическое обновление года в футере
// ===================================

const updateFooterYear = () => {
    const footerText = document.querySelector('.footer p');
    if (footerText) {
        const currentYear = new Date().getFullYear();
        footerText.innerHTML = `&copy; ${currentYear} Smart Care. Все права защищены.`;
    }
};

updateFooterYear();

// ===================================
// Предзагрузка изображений (если есть)
// ===================================

function preloadImages() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

preloadImages();

// ===================================
// Дебаг информация (только в dev mode)
// ===================================

if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    console.log(`
    ╔═══════════════════════════════════════╗
    ║      Smart Care Demo - Debug Info     ║
    ╠═══════════════════════════════════════╣
    ║ Total Slides: ${totalSlides}                      ║
    ║ Current Slide: ${currentSlide}                    ║
    ║ Device Mode: ${isDesktop ? 'Desktop' : 'Mobile '}              ║
    ║ Window Width: ${window.innerWidth}px              ║
    ╚═══════════════════════════════════════╝
    `);
    
    // Добавляем глобальные функции для дебага
    window.debugSlider = {
        goTo: goToSlide,
        next: nextSlide,
        prev: prevSlide,
        currentSlide: () => currentSlide,
        isDesktop: () => isDesktop
    };
    
    console.log('Debug functions available: window.debugSlider');
}

// ===================================
// Экспорт функций (если нужно)
// ===================================

window.SmartCare = {
    goToSlide,
    nextSlide,
    prevSlide,
    getCurrentSlide: () => currentSlide,
    getTotalSlides: () => totalSlides,
    isDesktopMode: () => isDesktop
};

// ===================================
// Обработка ошибок
// ===================================

window.addEventListener('error', (e) => {
    console.error('JavaScript Error:', e.message);
});

// Prevent console errors from breaking the app
window.addEventListener('unhandledrejection', (e) => {
    console.error('Unhandled Promise Rejection:', e.reason);
});

console.log('%c Smart Care Demo Ready! 🚀', 'color: #2196F3; font-size: 16px; font-weight: bold;');

