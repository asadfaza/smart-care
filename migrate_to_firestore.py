#!/usr/bin/env python3
"""
Скрипт миграции данных Smart Care в Firebase Firestore
Извлекает текущий контент и загружает его с поддержкой многоязычности
"""

import os
import sys
import json
from services.firestore_service import firestore_service

# Инициализация Firestore
print("🔥 Инициализация Firebase Firestore...")
firestore_service.initialize()

if not firestore_service.is_available:
    print("❌ Ошибка: Firestore недоступен. Проверьте credentials.")
    sys.exit(1)

print("✓ Firebase подключен успешно!\n")

# ==========================================
# ДАННЫЕ ДЛЯ МИГРАЦИИ
# ==========================================

# Навигация
navigation_data = {
    'ru': {
        'desktop': [
            {'id': 'home', 'text': 'Главная', 'icon': 'home'},
            {'id': 'team', 'text': 'Команда', 'icon': 'users'},
            {'id': 'why_us', 'text': 'Почему мы', 'icon': 'star'},
            {'id': 'roadmap', 'text': 'Дорожная карта', 'icon': 'road'},
            {'id': 'implementation', 'text': 'Реализация', 'icon': 'rocket'}
        ],
        'mobile': [
            {'id': 'home', 'text': 'Главная', 'icon': 'home'},
            {'id': 'team', 'text': 'Команда', 'icon': 'users'},
            {'id': 'why_us', 'text': 'О нас', 'icon': 'star'},
            {'id': 'roadmap', 'text': 'Карта', 'icon': 'road'},
            {'id': 'implementation', 'text': 'План', 'icon': 'rocket'}
        ]
    },
    'en': {
        'desktop': [
            {'id': 'home', 'text': 'Home', 'icon': 'home'},
            {'id': 'team', 'text': 'Team', 'icon': 'users'},
            {'id': 'why_us', 'text': 'Why Us', 'icon': 'star'},
            {'id': 'roadmap', 'text': 'Roadmap', 'icon': 'road'},
            {'id': 'implementation', 'text': 'Implementation', 'icon': 'rocket'}
        ],
        'mobile': [
            {'id': 'home', 'text': 'Home', 'icon': 'home'},
            {'id': 'team', 'text': 'Team', 'icon': 'users'},
            {'id': 'why_us', 'text': 'About', 'icon': 'star'},
            {'id': 'roadmap', 'text': 'Map', 'icon': 'road'},
            {'id': 'implementation', 'text': 'Plan', 'icon': 'rocket'}
        ]
    }
}

# Hero секция (главная страница)
hero_data = {
    'ru': {
        'logo_icon': 'shield-heart',
        'title': 'Smart Care',
        'subtitle': 'Ваш умный помощник для безопасного питания',
        'description': 'Приложение для помощи людям с заболеваниями'
    },
    'en': {
        'logo_icon': 'shield-heart',
        'title': 'Smart Care',
        'subtitle': 'Your smart assistant for safe nutrition',
        'description': 'An application to help people with chronic diseases'
    }
}

# Проблема
problem_data = {
    'ru': {
        'icon': 'exclamation-triangle',
        'title': 'Проблема',
        'intro': 'Люди с хроническими заболеваниями (диабет, целиакия, пищевые аллергии) сталкиваются с серьёзными трудностями:',
        'points': [
            'Тратят много времени на изучение состава продуктов',
            'Сложно найти мелкий шрифт на упаковках',
            'Ошибки могут привести к серьёзным последствиям для здоровья',
            'Непонятные химические названия ингредиентов',
            'Постоянный стресс при покупке продуктов'
        ],
        'stat_number': '~60 млн',
        'stat_label': 'человек в мире живут с диабетом и аллергиями'
    },
    'en': {
        'icon': 'exclamation-triangle',
        'title': 'Problem',
        'intro': 'People with chronic diseases (diabetes, celiac disease, food allergies) face serious difficulties:',
        'points': [
            'Spend a lot of time studying product composition',
            'Difficult to find small print on packages',
            'Mistakes can lead to serious health consequences',
            'Incomprehensible chemical names of ingredients',
            'Constant stress when buying products'
        ],
        'stat_number': '~60 million',
        'stat_label': 'people worldwide live with diabetes and allergies'
    }
}

# Решение
solution_data = {
    'ru': {
        'icon': 'lightbulb',
        'title': 'Наше решение',
        'intro': 'Smart Care использует компьютерное зрение и AI для мгновенного анализа продуктов через камеру смартфона.',
        'features': [
            {'icon': 'camera', 'title': 'Сканируй', 'text': 'Наведи камеру на продукт'},
            {'icon': 'brain', 'title': 'Анализируй', 'text': 'AI обрабатывает состав'},
            {'icon': 'check-circle', 'title': 'Получай ответ', 'text': 'Безопасно или нет'}
        ],
        'tech_title': 'Технологии',
        'technologies': [
            {'icon': 'eye', 'name': 'Computer Vision'},
            {'icon': 'robot', 'name': 'Machine Learning'},
            {'icon': 'font', 'name': 'OCR'},
            {'icon': 'mobile-alt', 'name': 'Mobile App'}
        ],
        'stat_number': '98.5%',
        'stat_label': 'точность распознавания'
    },
    'en': {
        'icon': 'lightbulb',
        'title': 'Our Solution',
        'intro': 'Smart Care uses computer vision and AI for instant product analysis via smartphone camera.',
        'features': [
            {'icon': 'camera', 'title': 'Scan', 'text': 'Point camera at product'},
            {'icon': 'brain', 'title': 'Analyze', 'text': 'AI processes composition'},
            {'icon': 'check-circle', 'title': 'Get Answer', 'text': 'Safe or not'}
        ],
        'tech_title': 'Technologies',
        'technologies': [
            {'icon': 'eye', 'name': 'Computer Vision'},
            {'icon': 'robot', 'name': 'Machine Learning'},
            {'icon': 'font', 'name': 'OCR'},
            {'icon': 'mobile-alt', 'name': 'Mobile App'}
        ],
        'stat_number': '98.5%',
        'stat_label': 'recognition accuracy'
    }
}

# Сферы применения
sectors_data = {
    'ru': {
        'title': 'Сфера применения',
        'icon': 'bullseye',
        'sectors': [
            {
                'icon': 'heartbeat',
                'title': 'Здравоохранение',
                'description': 'Помощь в управлении хроническими заболеваниями'
            },
            {
                'icon': 'universal-access',
                'title': 'Доступность',
                'description': 'Технология для всех возрастов и способностей'
            },
            {
                'icon': 'hands-helping',
                'title': 'Социальное воздействие',
                'description': 'Улучшение качества жизни миллионов людей'
            }
        ]
    },
    'en': {
        'title': 'Application Areas',
        'icon': 'bullseye',
        'sectors': [
            {
                'icon': 'heartbeat',
                'title': 'Healthcare',
                'description': 'Help managing chronic diseases'
            },
            {
                'icon': 'universal-access',
                'title': 'Accessibility',
                'description': 'Technology for all ages and abilities'
            },
            {
                'icon': 'hands-helping',
                'title': 'Social Impact',
                'description': 'Improving the quality of life for millions'
            }
        ]
    }
}

# Команда - заголовки
team_section_data = {
    'ru': {
        'title': 'Наша команда',
        'subtitle': 'Профессионалы, объединённые общей целью',
        'icon': 'users',
        'flip_hint_front': 'Нажми для подробностей',
        'flip_hint_back': 'Кликни на карточку чтобы вернуться',
        'experience_label': 'Опыт работы',
        'responsibilities_label': 'Обязанности:'
    },
    'en': {
        'title': 'Our Team',
        'subtitle': 'Professionals united by a common goal',
        'icon': 'users',
        'flip_hint_front': 'Click for details',
        'flip_hint_back': 'Click card to return',
        'experience_label': 'Work Experience',
        'responsibilities_label': 'Responsibilities:'
    }
}

# Члены команды
team_members = [
    {
        'id': 'asadbek',
        'name': 'Асадбек Фазлиддинов',
        'role': {
            'ru': 'Team Lead & Developer',
            'en': 'Team Lead & Developer'
        },
        'experience': ['Yandex Taxi', 'Uzum Market'],
        'responsibilities': {
            'ru': 'Руководство командой, разработка backend на Flask, интеграция ML моделей, создание API',
            'en': 'Team leadership, Flask backend development, ML model integration, API creation'
        },
        'links': {
            'linkedin': 'https://www.linkedin.com/in/asadbek-fazliddinov',
            'github': '#',
            'portfolio': '#'
        }
    },
    {
        'id': 'saydullo',
        'name': 'Сайдулло Султонов',
        'role': {
            'ru': 'Business Researcher',
            'en': 'Business Researcher'
        },
        'experience': ['Ermak', 'abnmb group', 'Cau medical'],
        'responsibilities': {
            'ru': 'Анализ рынка и конкурентов, исследование потребностей пользователей, разработка бизнес-модели',
            'en': 'Market and competitor analysis, user needs research, business model development'
        },
        'links': {
            'linkedin': 'https://www.linkedin.com/in/saydullo-sultonov-837347255/',
            'github': '#',
            'portfolio': '#'
        }
    }
]

# Почему мы
why_us_data = {
    'ru': {
        'title': 'Почему именно мы',
        'subtitle': 'Что делает нашу команду особенной',
        'icon': 'star',
        'cards': [
            {
                'icon': 'graduation-cap',
                'title': 'Экспертиза',
                'text': 'Наша команда объединяет экспертов в области компьютерного зрения, машинного обучения и разработки мобильных приложений. Совокупный опыт команды - более 15 лет в IT.'
            },
            {
                'icon': 'heart',
                'title': 'Личная мотивация',
                'text': 'У каждого из нас есть близкие люди с хроническими заболеваниями. Мы не просто создаём продукт - мы решаем реальную проблему, с которой сталкиваемся сами.'
            },
            {
                'icon': 'rocket',
                'title': 'Инновационный подход',
                'text': 'Мы используем последние достижения в области AI и computer vision, адаптируя их для решения конкретной социально значимой задачи.'
            },
            {
                'icon': 'users-cog',
                'title': 'Команда полного цикла',
                'text': 'От исследования и разработки ML-моделей до создания user-friendly мобильного приложения - мы контролируем весь процесс разработки.'
            },
            {
                'icon': 'chart-line',
                'title': 'Опыт реализации',
                'text': 'Члены нашей команды успешно запустили несколько проектов, включая мобильные приложения с ML-компонентами и веб-сервисы с высокой нагрузкой.'
            },
            {
                'icon': 'handshake',
                'title': 'Партнёрства',
                'text': 'Мы активно взаимодействуем с медицинскими специалистами и организациями пациентов для создания действительно полезного решения.'
            }
        ],
        'achievements_title': 'Наши достижения',
        'achievements': [
            {'icon': '🏆', 'text': 'Победители региональных хакатонов'},
            {'icon': '💡', 'text': '3 успешно запущенных проекта'},
            {'icon': '👥', 'text': 'Сообщество 1000+ тестовых пользователей'},
            {'icon': '🤝', 'text': 'Партнёрства с медицинскими организациями'}
        ]
    },
    'en': {
        'title': 'Why Choose Us',
        'subtitle': 'What makes our team special',
        'icon': 'star',
        'cards': [
            {
                'icon': 'graduation-cap',
                'title': 'Expertise',
                'text': 'Our team brings together experts in computer vision, machine learning, and mobile app development. Combined team experience - over 15 years in IT.'
            },
            {
                'icon': 'heart',
                'title': 'Personal Motivation',
                'text': 'Each of us has loved ones with chronic diseases. We\'re not just creating a product - we\'re solving a real problem we face ourselves.'
            },
            {
                'icon': 'rocket',
                'title': 'Innovative Approach',
                'text': 'We use the latest achievements in AI and computer vision, adapting them to solve a specific socially significant task.'
            },
            {
                'icon': 'users-cog',
                'title': 'Full-Cycle Team',
                'text': 'From research and ML model development to creating a user-friendly mobile app - we control the entire development process.'
            },
            {
                'icon': 'chart-line',
                'title': 'Implementation Experience',
                'text': 'Our team members have successfully launched several projects, including mobile apps with ML components and high-load web services.'
            },
            {
                'icon': 'handshake',
                'title': 'Partnerships',
                'text': 'We actively collaborate with medical professionals and patient organizations to create a truly useful solution.'
            }
        ],
        'achievements_title': 'Our Achievements',
        'achievements': [
            {'icon': '🏆', 'text': 'Winners of regional hackathons'},
            {'icon': '💡', 'text': '3 successfully launched projects'},
            {'icon': '👥', 'text': 'Community of 1000+ beta testers'},
            {'icon': '🤝', 'text': 'Partnerships with medical organizations'}
        ]
    }
}

# Дорожная карта
roadmap_data = {
    'ru': {
        'title': 'Дорожная карта проекта',
        'subtitle': 'Наш путь от идеи до запуска',
        'icon': 'road',
        'current_stage': 'MVP Development',
        'stage_label': 'Текущий этап:',
        'next_steps_title': 'Следующие шаги'
    },
    'en': {
        'title': 'Project Roadmap',
        'subtitle': 'Our journey from idea to launch',
        'icon': 'road',
        'current_stage': 'MVP Development',
        'stage_label': 'Current Stage:',
        'next_steps_title': 'Next Steps'
    }
}

# Этапы roadmap
milestones = [
    {
        'id': 'milestone_1',
        'title': {
            'ru': 'Исследование и концепция',
            'en': 'Research and Concept'
        },
        'date': 'Ноябрь 2024',
        'status': 'completed',
        'description': {
            'ru': 'Анализ проблемы, исследование рынка, разработка концепции',
            'en': 'Problem analysis, market research, concept development'
        }
    },
    {
        'id': 'milestone_2',
        'title': {
            'ru': 'Прототип MVP',
            'en': 'MVP Prototype'
        },
        'date': 'Декабрь 2024',
        'status': 'in_progress',
        'description': {
            'ru': 'Разработка базового функционала, обучение ML модели',
            'en': 'Basic functionality development, ML model training'
        }
    },
    {
        'id': 'milestone_3',
        'title': {
            'ru': 'Тестирование',
            'en': 'Testing'
        },
        'date': 'Январь 2025',
        'status': 'upcoming',
        'description': {
            'ru': 'Альфа-тестирование с фокус-группой пользователей',
            'en': 'Alpha testing with focus group of users'
        }
    },
    {
        'id': 'milestone_4',
        'title': {
            'ru': 'Публичный релиз',
            'en': 'Public Release'
        },
        'date': 'Февраль 2025',
        'status': 'upcoming',
        'description': {
            'ru': 'Запуск приложения в App Store и Google Play',
            'en': 'Launch app in App Store and Google Play'
        }
    }
]

# Следующие шаги
next_steps = [
    {
        'number': 1,
        'title': {
            'ru': 'Завершение MVP',
            'en': 'Complete MVP'
        },
        'description': {
            'ru': 'Финализация основного функционала и интеграция всех компонентов',
            'en': 'Finalize core functionality and integrate all components'
        }
    },
    {
        'number': 2,
        'title': {
            'ru': 'Бета-тестирование',
            'en': 'Beta Testing'
        },
        'description': {
            'ru': 'Запуск закрытого тестирования с фокус-группой из 100 пользователей',
            'en': 'Launch closed testing with focus group of 100 users'
        }
    },
    {
        'number': 3,
        'title': {
            'ru': 'Оптимизация модели',
            'en': 'Model Optimization'
        },
        'description': {
            'ru': 'Улучшение точности и скорости распознавания на основе feedback',
            'en': 'Improve accuracy and recognition speed based on feedback'
        }
    },
    {
        'number': 4,
        'title': {
            'ru': 'Публичный релиз',
            'en': 'Public Release'
        },
        'description': {
            'ru': 'Запуск приложения в App Store и Google Play',
            'en': 'Launch app in App Store and Google Play'
        }
    }
]

# Метаданные
meta_data = {
    'ru': {
        'title': 'Smart Care - Умный помощник для здоровья',
        'description': 'Smart Care - Приложение для помощи людям с заболеваниями, использующее AI и компьютерное зрение',
        'keywords': 'smart care, здоровье, диабет, аллергии, computer vision, AI',
        'og_title': 'Smart Care - Умный помощник для здоровья',
        'og_description': 'Мгновенный анализ продуктов через камеру смартфона'
    },
    'en': {
        'title': 'Smart Care - Smart Health Assistant',
        'description': 'Smart Care - An app to help people with chronic diseases using AI and computer vision',
        'keywords': 'smart care, health, diabetes, allergies, computer vision, AI',
        'og_title': 'Smart Care - Smart Health Assistant',
        'og_description': 'Instant product analysis via smartphone camera'
    }
}

# Footer
footer_data = {
    'ru': {
        'copyright': '© 2024 Smart Care. Все права защищены.',
        'tagline': 'Создано с ❤️ для хакатона'
    },
    'en': {
        'copyright': '© 2024 Smart Care. All rights reserved.',
        'tagline': 'Created with ❤️ for hackathon'
    }
}

# Страницы ошибок
errors_data = {
    'ru': {
        '404': {
            'icon': 'search',
            'title': '404',
            'subtitle': 'Страница не найдена',
            'text': 'К сожалению, запрашиваемая страница не существует или была перемещена.',
            'button': 'Вернуться на главную'
        },
        '500': {
            'icon': 'exclamation-triangle',
            'title': '500',
            'subtitle': 'Внутренняя ошибка сервера',
            'text': 'Что-то пошло не так на нашей стороне. Мы уже работаем над исправлением проблемы.',
            'button': 'Вернуться на главную'
        }
    },
    'en': {
        '404': {
            'icon': 'search',
            'title': '404',
            'subtitle': 'Page Not Found',
            'text': 'Unfortunately, the requested page does not exist or has been moved.',
            'button': 'Return to Home'
        },
        '500': {
            'icon': 'exclamation-triangle',
            'title': '500',
            'subtitle': 'Internal Server Error',
            'text': 'Something went wrong on our end. We are already working on fixing the issue.',
            'button': 'Return to Home'
        }
    }
}

# ==========================================
# ФУНКЦИИ ЗАГРУЗКИ
# ==========================================

def upload_navigation():
    """Загрузка навигации"""
    print("📍 Загрузка навигации...")
    for lang in ['ru', 'en']:
        firestore_service.create_document(
            'translations',
            f'{lang}_navigation',
            navigation_data[lang]
        )
    print("✓ Навигация загружена\n")

def upload_home_content():
    """Загрузка контента главной страницы"""
    print("🏠 Загрузка контента главной страницы...")
    
    # Hero
    for lang in ['ru', 'en']:
        firestore_service.create_document(
            'translations',
            f'{lang}_hero',
            hero_data[lang]
        )
    
    # Problem
    for lang in ['ru', 'en']:
        firestore_service.create_document(
            'translations',
            f'{lang}_problem',
            problem_data[lang]
        )
    
    # Solution
    for lang in ['ru', 'en']:
        firestore_service.create_document(
            'translations',
            f'{lang}_solution',
            solution_data[lang]
        )
    
    # Sectors
    for lang in ['ru', 'en']:
        firestore_service.create_document(
            'translations',
            f'{lang}_sectors',
            sectors_data[lang]
        )
    
    print("✓ Контент главной страницы загружен\n")

def upload_team():
    """Загрузка данных команды"""
    print("👥 Загрузка команды...")
    
    # Заголовки секции
    for lang in ['ru', 'en']:
        firestore_service.create_document(
            'translations',
            f'{lang}_team_section',
            team_section_data[lang]
        )
    
    # Члены команды
    for member in team_members:
        firestore_service.create_document(
            'team_members',
            member['id'],
            member
        )
    
    print("✓ Команда загружена\n")

def upload_why_us():
    """Загрузка секции 'Почему мы'"""
    print("⭐ Загрузка секции 'Почему мы'...")
    for lang in ['ru', 'en']:
        firestore_service.create_document(
            'translations',
            f'{lang}_why_us',
            why_us_data[lang]
        )
    print("✓ Секция 'Почему мы' загружена\n")

def upload_roadmap():
    """Загрузка дорожной карты"""
    print("🛣️  Загрузка дорожной карты...")
    
    # Заголовки секции
    for lang in ['ru', 'en']:
        firestore_service.create_document(
            'translations',
            f'{lang}_roadmap',
            roadmap_data[lang]
        )
    
    # Milestones
    for milestone in milestones:
        firestore_service.create_document(
            'roadmap_milestones',
            milestone['id'],
            milestone
        )
    
    # Next steps
    for step in next_steps:
        firestore_service.create_document(
            'roadmap_next_steps',
            f'step_{step["number"]}',
            step
        )
    
    print("✓ Дорожная карта загружена\n")

def upload_meta_and_footer():
    """Загрузка метаданных и footer"""
    print("📄 Загрузка метаданных и footer...")
    
    for lang in ['ru', 'en']:
        firestore_service.create_document(
            'translations',
            f'{lang}_meta',
            meta_data[lang]
        )
        firestore_service.create_document(
            'translations',
            f'{lang}_footer',
            footer_data[lang]
        )
    
    print("✓ Метаданные и footer загружены\n")

def upload_errors():
    """Загрузка страниц ошибок"""
    print("❌ Загрузка страниц ошибок...")
    for lang in ['ru', 'en']:
        firestore_service.create_document(
            'translations',
            f'{lang}_errors',
            errors_data[lang]
        )
    print("✓ Страницы ошибок загружены\n")

# ==========================================
# ГЛАВНАЯ ФУНКЦИЯ
# ==========================================

def main():
    """Запуск миграции"""
    print("\n" + "="*60)
    print("  МИГРАЦИЯ ДАННЫХ SMART CARE В FIRESTORE")
    print("="*60 + "\n")
    
    try:
        # Загрузка всех данных
        upload_navigation()
        upload_home_content()
        upload_team()
        upload_why_us()
        upload_roadmap()
        upload_meta_and_footer()
        upload_errors()
        
        print("\n" + "="*60)
        print("  ✅ МИГРАЦИЯ ЗАВЕРШЕНА УСПЕШНО!")
        print("="*60 + "\n")
        
        print("📊 Загружено:")
        print("  • Навигация (2 языка)")
        print("  • Контент главной страницы (hero, problem, solution, sectors)")
        print(f"  • Команда ({len(team_members)} членов)")
        print("  • Почему мы (6 карточек + достижения)")
        print(f"  • Дорожная карта ({len(milestones)} milestones + {len(next_steps)} next steps)")
        print("  • Метаданные и footer")
        print("  • Страницы ошибок (404, 500)")
        print("\n✨ Все данные успешно загружены в Firebase Firestore!\n")
        
    except Exception as e:
        print(f"\n❌ Ошибка миграции: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()

