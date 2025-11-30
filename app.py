"""
Smart Care - Демо-сайт для хакатона
Приложение для помощи людям с заболеваниями
С поддержкой Firebase Firestore и многоязычности
"""

from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_caching import Cache
from config import config
from services.firestore_service import firestore_service
import logging
import os

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация приложения
app = Flask(__name__)
env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config.get(env, config['development']))

# Инициализация кэша
cache = Cache(app)

# Инициализация Firebase Firestore
if app.config.get('USE_FIRESTORE', True):
    try:
        credentials_path = app.config.get('FIREBASE_CREDENTIALS_PATH')
        firestore_service.initialize(credentials_path)
        logger.info("✓ Firebase Firestore инициализирован")
    except Exception as e:
        logger.error(f"Ошибка инициализации Firebase: {e}")
        logger.warning("Приложение будет работать с локальными данными")

# ==========================================
# ЛОКАЛЬНЫЕ ДАННЫЕ (Fallback)
# ==========================================

# Локальные данные команды (fallback если Firestore недоступен)
LOCAL_TEAM_DATA = [
    {
        'name': 'Асадбек Фазлиддинов',
        'role': 'Team Lead & Developer',
        'experience': ['Uzum Market', 'Yandex Taxi'],
        'responsibilities': 'Руководство командой, разработка backend на Flask, интеграция ML моделей, создание API',
        'links': {
            'linkedin': 'https://www.linkedin.com/in/asadbek-fazliddinov',
            'github': 'https://github.com/asadfaza',
            'portfolio': '#'
        }
    },
    {
        'name': 'Сайдулло Султонов',
        'role': 'Business Researcher',
        'experience': ['Ermak', 'abnmb group', 'cau akfa group'],
        'responsibilities': 'Анализ рынка и конкурентов, исследование потребностей пользователей, разработка бизнес-модели',
        'links': {
            'linkedin': 'https://www.linkedin.com/in/saydullo-sultonov-837347255/',
            'github': '#',
            'portfolio': '#'
        }
    },
]

# Локальная дорожная карта (fallback)
LOCAL_ROADMAP_DATA = {
    'current_stage': 'MVP Development',
    'milestones': [
        {
            'title': 'Исследование и концепция',
            'date': 'Ноябрь 2025',
            'status': 'completed',
            'description': 'Анализ проблемы, исследование рынка, разработка концепции'
        },
        {
            'title': 'Прототип MVP',
            'date': 'Декабрь 2025',
            'status': 'in_progress',
            'description': 'Разработка базового функционала, обучение ML модели'
        },
        {
            'title': 'Тестирование',
            'date': 'Январь 2026',
            'status': 'upcoming',
            'description': 'Альфа-тестирование с фокус-группой пользователей'
        },
        {
            'title': 'Публичный релиз',
            'date': 'Февраль 2026',
            'status': 'upcoming',
            'description': 'Запуск приложения в App Store и Google Play'
        }
    ]
}

# ==========================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ==========================================

def get_current_language():
    """Получить текущий язык из сессии или определить по умолчанию"""
    if 'language' in session:
        return session['language']
    
    # Автоопределение языка браузера
    accept_language = request.headers.get('Accept-Language', '')
    if 'en' in accept_language.lower():
        return 'en'
    
    return app.config['DEFAULT_LANGUAGE']

def set_language(lang):
    """Установить язык в сессии"""
    if lang in app.config['SUPPORTED_LANGUAGES']:
        session['language'] = lang
        return True
    return False

@cache.memoize(timeout=3600)
def get_team_from_firestore(lang='ru'):
    """Получить данные команды из Firestore с кэшированием"""
    if not firestore_service.is_available:
        return LOCAL_TEAM_DATA
    
    try:
        team = firestore_service.get_collection('team_members', lang)
        return team if team else LOCAL_TEAM_DATA
    except Exception as e:
        logger.error(f"Ошибка получения команды: {e}")
        return LOCAL_TEAM_DATA

@cache.memoize(timeout=3600)
def get_roadmap_from_firestore(lang='ru'):
    """Получить дорожную карту из Firestore с кэшированием"""
    if not firestore_service.is_available:
        return LOCAL_ROADMAP_DATA
    
    try:
        # Получаем заголовки секции
        roadmap_meta = firestore_service.get_document('translations', f'{lang}_roadmap', lang)
        
        # Получаем milestones
        milestones = firestore_service.get_collection('roadmap_milestones', lang)
        
        # Получаем next steps
        next_steps = firestore_service.get_collection('roadmap_next_steps', lang)
        
        return {
            'current_stage': roadmap_meta.get('current_stage', 'MVP Development') if roadmap_meta else 'MVP Development',
            'milestones': milestones if milestones else LOCAL_ROADMAP_DATA['milestones'],
            'next_steps': next_steps
        }
    except Exception as e:
        logger.error(f"Ошибка получения roadmap: {e}")
        return LOCAL_ROADMAP_DATA

@cache.memoize(timeout=3600)
def get_translations(lang='ru'):
    """Получить все переводы для языка"""
    if not firestore_service.is_available:
        return {}
    
    try:
        translations = {}
        
        # Получаем все документы переводов
        translation_keys = [
            'navigation', 'hero', 'problem', 'solution', 'sectors',
            'team_section', 'why_us', 'roadmap', 'meta', 'footer', 'errors'
        ]
        
        for key in translation_keys:
            doc = firestore_service.get_document('translations', f'{lang}_{key}', lang)
            if doc:
                translations[key] = doc
        
        return translations
    except Exception as e:
        logger.error(f"Ошибка получения переводов: {e}")
        return {}

# ==========================================
# МАРШРУТЫ
# ==========================================

@app.route('/')
@app.route('/<lang>')
def index(lang=None):
    """Главная страница с презентацией проекта"""
    
    # Определение языка
    if lang:
        if lang in app.config['SUPPORTED_LANGUAGES']:
            set_language(lang)
        else:
            return redirect(url_for('index'))
    
    current_lang = get_current_language()
    
    # Получение данных
    team = get_team_from_firestore(current_lang)
    roadmap = get_roadmap_from_firestore(current_lang)
    translations = get_translations(current_lang)
    
    return render_template(
        'index.html',
        team=team,
        roadmap=roadmap,
        translations=translations,
        colors=app.config['COLORS'],
        current_lang=current_lang,
        supported_languages=app.config['SUPPORTED_LANGUAGES']
    )

@app.route('/set-language/<lang>')
def set_lang(lang):
    """Установить язык и перенаправить на главную"""
    if set_language(lang):
        logger.info(f"Язык изменён на: {lang}")
        # Очищаем кэш при смене языка
        cache.clear()
    return redirect(url_for('index', lang=lang))

@app.route('/admin')
def admin():
    """Admin панель для управления контентом"""
    # В production добавить аутентификацию!
    if not app.config['DEBUG']:
        return "Access denied", 403
    
    current_lang = get_current_language()
    return render_template('admin.html', current_lang=current_lang)

# API эндпоинты
@app.route('/api/health')
def health():
    """Проверка здоровья приложения"""
    return jsonify({
        'status': 'healthy',
        'service': 'smart_care',
        'version': app.config['APP_VERSION'],
        'firestore_available': firestore_service.is_available
    })

@app.route('/api/team')
@app.route('/api/team/<lang>')
def get_team(lang=None):
    """Получить данные команды через API"""
    current_lang = lang if lang in app.config['SUPPORTED_LANGUAGES'] else get_current_language()
    team = get_team_from_firestore(current_lang)
    return jsonify(team)

@app.route('/api/roadmap')
@app.route('/api/roadmap/<lang>')
def get_roadmap(lang=None):
    """Получить дорожную карту через API"""
    current_lang = lang if lang in app.config['SUPPORTED_LANGUAGES'] else get_current_language()
    roadmap = get_roadmap_from_firestore(current_lang)
    return jsonify(roadmap)

@app.route('/api/translations/<lang>')
def get_translations_api(lang):
    """Получить все переводы для языка через API"""
    if lang not in app.config['SUPPORTED_LANGUAGES']:
        return jsonify({'error': 'Unsupported language'}), 400
    
    translations = get_translations(lang)
    return jsonify(translations)

@app.route('/api/clear-cache')
def clear_cache():
    """Очистить кэш (для разработки)"""
    if app.config['DEBUG']:
        cache.clear()
        firestore_service.clear_cache()
        return jsonify({'status': 'cache cleared'})
    return jsonify({'error': 'not allowed'}), 403

# Обработка ошибок
@app.errorhandler(404)
def not_found(error):
    """Обработка 404 ошибки"""
    current_lang = get_current_language()
    translations = get_translations(current_lang)
    return render_template(
        '404.html',
        translations=translations,
        current_lang=current_lang
    ), 404

@app.errorhandler(500)
def internal_error(error):
    """Обработка 500 ошибки"""
    current_lang = get_current_language()
    translations = get_translations(current_lang)
    return render_template(
        '500.html',
        translations=translations,
        current_lang=current_lang
    ), 500

# ==========================================
# ЗАПУСК ПРИЛОЖЕНИЯ
# ==========================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("  🛡️  SMART CARE - Запуск приложения")
    print("="*60)
    print(f"\n✓ Версия: {app.config['APP_VERSION']}")
    print(f"✓ Debug режим: {app.config['DEBUG']}")
    print(f"✓ Firestore: {'✓ Подключен' if firestore_service.is_available else '✗ Не подключен (используются локальные данные)'}")
    print(f"✓ Поддерживаемые языки: {', '.join(app.config['SUPPORTED_LANGUAGES'])}")
    print(f"✓ Язык по умолчанию: {app.config['DEFAULT_LANGUAGE']}")
    print(f"\n🌐 Приложение доступно по адресу: http://{app.config['HOST']}:{app.config['PORT']}")
    print(f"🌍 Русский: http://localhost:{app.config['PORT']}/ru")
    print(f"🌍 English: http://localhost:{app.config['PORT']}/en")
    print("\n" + "="*60 + "\n")
    
    app.run(
        debug=app.config['DEBUG'],
        host=app.config['HOST'],
        port=app.config['PORT']
    )
