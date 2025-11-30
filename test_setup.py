#!/usr/bin/env python3
"""
Тестовый скрипт для проверки настройки Smart Care
"""

import sys
import os

def print_header(text):
    """Печатает красивый заголовок"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def check_python_version():
    """Проверяет версию Python"""
    print_header("Проверка версии Python")
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    if version.major >= 3 and version.minor >= 8:
        print("✓ Версия Python подходит!")
        return True
    else:
        print("✗ Требуется Python 3.8 или выше")
        return False

def check_imports():
    """Проверяет импорты"""
    print_header("Проверка зависимостей")
    
    required_modules = {
        'flask': 'Flask',
        'jinja2': 'Jinja2',
        'werkzeug': 'Werkzeug'
    }
    
    all_ok = True
    for module, name in required_modules.items():
        try:
            __import__(module)
            print(f"✓ {name} установлен")
        except ImportError:
            print(f"✗ {name} не найден")
            all_ok = False
    
    return all_ok

def check_files():
    """Проверяет наличие необходимых файлов"""
    print_header("Проверка файлов проекта")
    
    required_files = [
        'app.py',
        'config.py',
        'requirements.txt',
        'templates/base.html',
        'templates/index.html',
        'static/css/style.css',
        'static/js/main.js',
    ]
    
    all_ok = True
    for file_path in required_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✓ {file_path} ({size} bytes)")
        else:
            print(f"✗ {file_path} не найден")
            all_ok = False
    
    return all_ok

def check_syntax():
    """Проверяет синтаксис Python файлов"""
    print_header("Проверка синтаксиса Python")
    
    python_files = ['app.py', 'config.py']
    all_ok = True
    
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
                compile(code, file_path, 'exec')
            print(f"✓ {file_path} - синтаксис корректен")
        except SyntaxError as e:
            print(f"✗ {file_path} - ошибка синтаксиса: {e}")
            all_ok = False
        except FileNotFoundError:
            print(f"✗ {file_path} - файл не найден")
            all_ok = False
    
    return all_ok

def check_config():
    """Проверяет конфигурацию"""
    print_header("Проверка конфигурации")
    
    try:
        from config import config
        print(f"✓ Конфигурация загружена")
        print(f"✓ Доступные режимы: {', '.join(config.keys())}")
        
        dev_config = config['development']
        print(f"✓ Port: {dev_config.PORT}")
        print(f"✓ Debug: {dev_config.DEBUG}")
        
        return True
    except Exception as e:
        print(f"✗ Ошибка загрузки конфигурации: {e}")
        return False

def check_app():
    """Проверяет основное приложение"""
    print_header("Проверка Flask приложения")
    
    try:
        from app import app, TEAM_DATA, ROADMAP_DATA
        print(f"✓ Flask приложение создано")
        print(f"✓ Членов команды: {len(TEAM_DATA)}")
        print(f"✓ Этапов в roadmap: {len(ROADMAP_DATA['milestones'])}")
        
        # Проверка routes
        routes = [rule.rule for rule in app.url_map.iter_rules() if rule.endpoint != 'static']
        print(f"✓ Зарегистрированные маршруты:")
        for route in routes:
            print(f"  - {route}")
        
        return True
    except Exception as e:
        print(f"✗ Ошибка загрузки приложения: {e}")
        import traceback
        traceback.print_exc()
        return False

def print_summary(results):
    """Печатает итоговую сводку"""
    print_header("ИТОГОВАЯ СВОДКА")
    
    total = len(results)
    passed = sum(results.values())
    
    print(f"\nПройдено тестов: {passed}/{total}")
    
    if passed == total:
        print("\n✅ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ УСПЕШНО!")
        print("\n🚀 Приложение готово к запуску!")
        print("\nЗапустите: python app.py")
        print("Затем откройте: http://localhost:5001")
    else:
        print("\n⚠️  НЕКОТОРЫЕ ПРОВЕРКИ НЕ ПРОЙДЕНЫ")
        print("\nПожалуйста, исправьте ошибки перед запуском.")
    
    print("\n" + "="*60 + "\n")

def main():
    """Главная функция"""
    print("\n" + "🛡️ "*20)
    print("   SMART CARE - ТЕСТИРОВАНИЕ НАСТРОЙКИ")
    print("🛡️ "*20)
    
    results = {
        'Python версия': check_python_version(),
        'Зависимости': check_imports(),
        'Файлы проекта': check_files(),
        'Синтаксис Python': check_syntax(),
        'Конфигурация': check_config(),
        'Flask приложение': check_app(),
    }
    
    print_summary(results)
    
    # Возвращаем код выхода
    return 0 if all(results.values()) else 1

if __name__ == '__main__':
    sys.exit(main())

