"""
Firestore Service для Smart Care
Управление переводами и контентом из Firebase Firestore
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from functools import lru_cache
import firebase_admin
from firebase_admin import credentials, firestore
from flask import current_app

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FirestoreService:
    """Сервис для работы с Firebase Firestore"""
    
    _instance = None
    _db = None
    _initialized = False
    
    def __new__(cls):
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = super(FirestoreService, cls).__new__(cls)
        return cls._instance
    
    def initialize(self, credentials_path: str = None):
        """
        Инициализация Firebase Admin SDK
        
        Args:
            credentials_path: Путь к файлу credentials.json
        """
        if self._initialized:
            logger.info("Firebase уже инициализирован")
            return
        
        try:
            # Определение пути к credentials
            if credentials_path is None:
                credentials_path = os.path.join(
                    os.path.dirname(os.path.dirname(__file__)),
                    'firebase-credentials.json'
                )
            
            if not os.path.exists(credentials_path):
                logger.warning(f"Firebase credentials не найдены: {credentials_path}")
                logger.warning("Работа будет продолжена с локальными данными")
                return
            
            # Инициализация Firebase
            cred = credentials.Certificate(credentials_path)
            firebase_admin.initialize_app(cred)
            
            # Получение клиента Firestore
            self._db = firestore.client()
            self._initialized = True
            
            logger.info("✓ Firebase Firestore успешно инициализирован")
            
        except Exception as e:
            logger.error(f"Ошибка инициализации Firebase: {e}")
            logger.warning("Приложение будет работать без Firebase")
    
    @property
    def db(self):
        """Получить клиент Firestore"""
        return self._db
    
    @property
    def is_available(self) -> bool:
        """Проверить доступность Firestore"""
        return self._initialized and self._db is not None
    
    @lru_cache(maxsize=128)
    def get_translations(self, lang: str = 'ru') -> Dict[str, Any]:
        """
        Получить все переводы для указанного языка
        
        Args:
            lang: Код языка (ru или en)
            
        Returns:
            Словарь с переводами
        """
        if not self.is_available:
            logger.warning("Firestore недоступен, используются локальные данные")
            return self._get_default_translations(lang)
        
        try:
            translations = {}
            
            # Получаем все документы из коллекции translations/{lang}
            lang_ref = self._db.collection('translations').document(lang)
            collections = lang_ref.collections()
            
            for collection in collections:
                collection_name = collection.id
                docs = collection.stream()
                
                translations[collection_name] = {}
                for doc in docs:
                    translations[collection_name][doc.id] = doc.to_dict()
            
            # Также получаем документы верхнего уровня
            doc = lang_ref.get()
            if doc.exists:
                translations.update(doc.to_dict())
            
            logger.info(f"✓ Загружены переводы для языка: {lang}")
            return translations
            
        except Exception as e:
            logger.error(f"Ошибка получения переводов из Firestore: {e}")
            return self._get_default_translations(lang)
    
    def get_document(self, collection: str, document_id: str, lang: str = 'ru') -> Optional[Dict]:
        """
        Получить конкретный документ
        
        Args:
            collection: Название коллекции
            document_id: ID документа
            lang: Язык
            
        Returns:
            Данные документа или None
        """
        if not self.is_available:
            return None
        
        try:
            doc_ref = self._db.collection(collection).document(document_id)
            doc = doc_ref.get()
            
            if doc.exists:
                data = doc.to_dict()
                # Если есть многоязычные поля, выбираем нужный язык
                return self._extract_lang_data(data, lang)
            return None
            
        except Exception as e:
            logger.error(f"Ошибка получения документа {collection}/{document_id}: {e}")
            return None
    
    def get_collection(self, collection: str, lang: str = 'ru') -> list:
        """
        Получить все документы из коллекции
        
        Args:
            collection: Название коллекции
            lang: Язык
            
        Returns:
            Список документов
        """
        if not self.is_available:
            return []
        
        try:
            docs = self._db.collection(collection).stream()
            result = []
            
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id
                result.append(self._extract_lang_data(data, lang))
            
            return result
            
        except Exception as e:
            logger.error(f"Ошибка получения коллекции {collection}: {e}")
            return []
    
    def _extract_lang_data(self, data: Dict, lang: str) -> Dict:
        """
        Извлечь данные для конкретного языка из многоязычных полей
        
        Args:
            data: Исходные данные
            lang: Язык
            
        Returns:
            Данные с извлеченным языком
        """
        # Проверяем, есть ли в данных ключи 'ru' и 'en' на верхнем уровне
        # Это означает структуру типа: {id: '...', ru: {...}, en: {...}}
        if 'ru' in data and 'en' in data:
            # Извлекаем данные для нужного языка
            lang_data = data.get(lang, data.get('ru', {}))
            
            # Добавляем обратно 'id' если он есть
            if 'id' in data:
                lang_data['id'] = data['id']
            
            return lang_data
        
        # Иначе обрабатываем каждое поле отдельно (старая логика)
        result = {}
        
        for key, value in data.items():
            if isinstance(value, dict) and lang in value:
                # Многоязычное поле
                result[key] = value.get(lang, value.get('ru', ''))
            else:
                result[key] = value
        
        return result
    
    def _get_default_translations(self, lang: str) -> Dict[str, Any]:
        """
        Получить дефолтные переводы (fallback)
        
        Args:
            lang: Язык
            
        Returns:
            Базовые переводы
        """
        # Здесь можно вернуть минимальный набор переводов
        # или загрузить из локального JSON файла
        return {
            'navigation': {
                'home': 'Главная' if lang == 'ru' else 'Home',
                'team': 'Команда' if lang == 'ru' else 'Team',
                'why_us': 'Почему мы' if lang == 'ru' else 'Why Us',
                'roadmap': 'Дорожная карта' if lang == 'ru' else 'Roadmap',
                'implementation': 'Реализация' if lang == 'ru' else 'Implementation'
            }
        }
    
    def update_document(self, collection: str, document_id: str, data: Dict) -> bool:
        """
        Обновить документ в Firestore
        
        Args:
            collection: Название коллекции
            document_id: ID документа
            data: Данные для обновления
            
        Returns:
            True если успешно
        """
        if not self.is_available:
            logger.error("Firestore недоступен")
            return False
        
        try:
            doc_ref = self._db.collection(collection).document(document_id)
            doc_ref.set(data, merge=True)
            
            # Очищаем кэш после обновления
            self.get_translations.cache_clear()
            
            logger.info(f"✓ Документ {collection}/{document_id} обновлен")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка обновления документа: {e}")
            return False
    
    def create_document(self, collection: str, document_id: str, data: Dict) -> bool:
        """
        Создать новый документ
        
        Args:
            collection: Название коллекции
            document_id: ID документа
            data: Данные
            
        Returns:
            True если успешно
        """
        if not self.is_available:
            return False
        
        try:
            doc_ref = self._db.collection(collection).document(document_id)
            doc_ref.set(data)
            
            # Очищаем кэш
            self.get_translations.cache_clear()
            
            logger.info(f"✓ Документ {collection}/{document_id} создан")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка создания документа: {e}")
            return False
    
    def delete_document(self, collection: str, document_id: str) -> bool:
        """
        Удалить документ
        
        Args:
            collection: Название коллекции
            document_id: ID документа
            
        Returns:
            True если успешно
        """
        if not self.is_available:
            return False
        
        try:
            doc_ref = self._db.collection(collection).document(document_id)
            doc_ref.delete()
            
            # Очищаем кэш
            self.get_translations.cache_clear()
            
            logger.info(f"✓ Документ {collection}/{document_id} удален")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка удаления документа: {e}")
            return False
    
    def clear_cache(self):
        """Очистить кэш переводов"""
        self.get_translations.cache_clear()
        logger.info("✓ Кэш переводов очищен")


# Глобальный экземпляр сервиса
firestore_service = FirestoreService()

