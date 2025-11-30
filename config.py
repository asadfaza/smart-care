"""
Конфигурация Flask приложения Smart Care
"""

import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()


class Config:
    """Базовая конфигурация"""
    
    # Основные настройки приложения
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    APP_VERSION = '1.0.0'
    
    # Настройки сервера
    DEBUG = False
    HOST = '0.0.0.0'
    PORT = 5001
    
    # Firebase настройки
    FIREBASE_CREDENTIALS_PATH = os.environ.get('FIREBASE_CREDENTIALS_PATH') or 'firebase-credentials.json'
    USE_FIRESTORE = True  # Использовать Firestore для данных (если False - локальные данные)
    
    # Настройки кэширования
    CACHE_TYPE = os.environ.get('CACHE_TYPE') or 'simple'
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get('CACHE_DEFAULT_TIMEOUT') or 3600)  # 1 час
    
    # Настройки многоязычности
    SUPPORTED_LANGUAGES = ['ru', 'en']
    DEFAULT_LANGUAGE = 'ru'
    
    # Цветовая схема приложения (бело-синяя)
    COLORS = {
        'primary_blue': '#2196F3',
        'light_blue': '#64B5F6',
        'dark_blue': '#1976D2',
        'white': '#FFFFFF',
        'light_gray': '#F5F5F5',
        'text': '#333333',
        'text_light': '#666666'
    }


class DevelopmentConfig(Config):
    """Конфигурация для разработки"""
    DEBUG = True
    HOST = '127.0.0.1'
    CACHE_TYPE = 'simple'  # Простое кэширование для разработки


class ProductionConfig(Config):
    """Конфигурация для продакшена"""
    DEBUG = False
    # В продакшене SECRET_KEY должен быть задан через переменные окружения
    SECRET_KEY = os.environ.get('SECRET_KEY')
    HOST = '0.0.0.0'
    PORT = int(os.environ.get('PORT', 10000))
    # Redis cache для production (опционально)
    # CACHE_TYPE = 'redis'
    # CACHE_REDIS_URL = os.environ.get('REDIS_URL')


class TestingConfig(Config):
    """Конфигурация для тестирования"""
    TESTING = True
    DEBUG = True


# Словарь конфигураций
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
