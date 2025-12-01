#!/usr/bin/env python3
"""
Скрипт для проверки состояния переводов в Firestore
Проверяет наличие RU и EN версий для всех документов
"""

from services.firestore_service import firestore_service
from dotenv import load_dotenv
import sys

load_dotenv()

def check_translations():
    """Проверить все переводы в Firestore"""
    
    print("="*60)
    print("  🔍 ПРОВЕРКА ПЕРЕВОДОВ В FIRESTORE")
    print("="*60)
    
    # Инициализация
    try:
        firestore_service.initialize('firebase-credentials.json')
        print("\n✅ Firebase инициализирован\n")
    except Exception as e:
        print(f"\n❌ Ошибка инициализации: {e}\n")
        return
    
    db = firestore_service.db
    
    # Статистика
    stats = {
        'total': 0,
        'ru_only': 0,
        'en_only': 0,
        'both': 0,
        'neither': 0,
        'missing_en': []
    }
    
    # Проверка коллекции translations
    print("\n📁 КОЛЛЕКЦИЯ: translations")
    print("-" * 60)
    
    try:
        coll = db.collection('translations')
        docs = list(coll.stream())
        
        for doc in docs:
            doc_id = doc.id
            data = doc.to_dict()
            stats['total'] += 1
            
            # Проверяем какие языки есть
            if doc_id.startswith('ru_'):
                # Это русский документ
                en_id = doc_id.replace('ru_', 'en_', 1)
                en_doc = db.collection('translations').document(en_id).get()
                
                if en_doc.exists:
                    print(f"  ✅ {doc_id:25s} → {en_id:25s}")
                    stats['both'] += 1
                else:
                    print(f"  ⚠️  {doc_id:25s} → {en_id:25s} (ОТСУТСТВУЕТ)")
                    stats['ru_only'] += 1
                    stats['missing_en'].append(doc_id)
            
            elif doc_id.startswith('en_'):
                # Проверяем только если нет парного ru_
                ru_id = doc_id.replace('en_', 'ru_', 1)
                ru_doc = db.collection('translations').document(ru_id).get()
                
                if not ru_doc.exists:
                    print(f"  ⚠️  {doc_id:25s} (нет русской версии)")
                    stats['en_only'] += 1
        
    except Exception as e:
        print(f"  ❌ Ошибка: {e}")
    
    # Проверка коллекции team_members
    print("\n📁 КОЛЛЕКЦИЯ: team_members")
    print("-" * 60)
    
    try:
        coll = db.collection('team_members')
        docs = list(coll.stream())
        
        for doc in docs:
            doc_id = doc.id
            data = doc.to_dict()
            stats['total'] += 1
            
            has_ru = 'ru' in data
            has_en = 'en' in data
            
            if has_ru and has_en:
                print(f"  ✅ {doc_id:25s} → RU + EN")
                stats['both'] += 1
            elif has_ru:
                print(f"  ⚠️  {doc_id:25s} → только RU")
                stats['ru_only'] += 1
                stats['missing_en'].append(f'team_members/{doc_id}')
            elif has_en:
                print(f"  ⚠️  {doc_id:25s} → только EN")
                stats['en_only'] += 1
            else:
                print(f"  ❌ {doc_id:25s} → НЕТ ЯЗЫКОВ")
                stats['neither'] += 1
        
    except Exception as e:
        print(f"  ❌ Ошибка: {e}")
    
    # Проверка коллекции roadmap_milestones
    print("\n📁 КОЛЛЕКЦИЯ: roadmap_milestones")
    print("-" * 60)
    
    try:
        coll = db.collection('roadmap_milestones')
        docs = list(coll.stream())
        
        for doc in docs:
            doc_id = doc.id
            data = doc.to_dict()
            stats['total'] += 1
            
            has_ru = 'ru' in data
            has_en = 'en' in data
            
            if has_ru and has_en:
                print(f"  ✅ {doc_id:25s} → RU + EN")
                stats['both'] += 1
            elif has_ru:
                print(f"  ⚠️  {doc_id:25s} → только RU")
                stats['ru_only'] += 1
                stats['missing_en'].append(f'roadmap_milestones/{doc_id}')
            elif has_en:
                print(f"  ⚠️  {doc_id:25s} → только EN")
                stats['en_only'] += 1
            else:
                print(f"  ❌ {doc_id:25s} → НЕТ ЯЗЫКОВ")
                stats['neither'] += 1
        
    except Exception as e:
        print(f"  ❌ Ошибка: {e}")
    
    # Проверка коллекции roadmap_next_steps
    print("\n📁 КОЛЛЕКЦИЯ: roadmap_next_steps")
    print("-" * 60)
    
    try:
        coll = db.collection('roadmap_next_steps')
        docs = list(coll.stream())
        
        for doc in docs:
            doc_id = doc.id
            data = doc.to_dict()
            stats['total'] += 1
            
            has_ru = 'ru' in data
            has_en = 'en' in data
            
            if has_ru and has_en:
                print(f"  ✅ {doc_id:25s} → RU + EN")
                stats['both'] += 1
            elif has_ru:
                print(f"  ⚠️  {doc_id:25s} → только RU")
                stats['ru_only'] += 1
                stats['missing_en'].append(f'roadmap_next_steps/{doc_id}')
            elif has_en:
                print(f"  ⚠️  {doc_id:25s} → только EN")
                stats['en_only'] += 1
            else:
                print(f"  ❌ {doc_id:25s} → НЕТ ЯЗЫКОВ")
                stats['neither'] += 1
        
    except Exception as e:
        print(f"  ❌ Ошибка: {e}")
    
    # Итоговая статистика
    print("\n" + "="*60)
    print("  📊 СТАТИСТИКА")
    print("="*60)
    print(f"\nВсего документов:        {stats['total']}")
    print(f"✅ С обоими языками:     {stats['both']} ({stats['both']/stats['total']*100:.1f}%)")
    print(f"⚠️  Только RU:            {stats['ru_only']} ({stats['ru_only']/stats['total']*100:.1f}%)")
    print(f"⚠️  Только EN:            {stats['en_only']} ({stats['en_only']/stats['total']*100:.1f}%)")
    print(f"❌ Без языков:           {stats['neither']}")
    
    # Список отсутствующих английских переводов
    if stats['missing_en']:
        print("\n" + "="*60)
        print("  ⚠️  ОТСУТСТВУЮЩИЕ АНГЛИЙСКИЕ ПЕРЕВОДЫ")
        print("="*60)
        for item in stats['missing_en']:
            print(f"  - {item}")
    
    # Рекомендации
    print("\n" + "="*60)
    print("  💡 РЕКОМЕНДАЦИИ")
    print("="*60)
    
    if stats['ru_only'] > 0:
        print(f"\n⚠️  Найдено {stats['ru_only']} документов без английского перевода")
        print("   Действие: Обновите migrate_to_firestore.py и добавьте EN переводы")
    
    if stats['both'] == stats['total']:
        print("\n✅ Все документы имеют оба перевода! Отлично!")
    else:
        coverage = (stats['both'] / stats['total']) * 100
        print(f"\n📈 Покрытие переводов: {coverage:.1f}%")
        print(f"   Цель: 100%")
        print(f"   Осталось: {stats['total'] - stats['both']} документов")
    
    print("\n" + "="*60)
    print("  ✅ ПРОВЕРКА ЗАВЕРШЕНА")
    print("="*60)
    print("\nДля получения детальной информации откройте:")
    print("📄 MULTILANG_AUDIT_PROMPT.md")
    print("\n")

if __name__ == '__main__':
    try:
        check_translations()
    except KeyboardInterrupt:
        print("\n\n⚠️  Прервано пользователем")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Критическая ошибка: {e}")
        sys.exit(1)

