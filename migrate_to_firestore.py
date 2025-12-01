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
        # Desktop header
        'home': 'Главная',
        'team': 'Команда',
        'why_us': 'Почему мы',
        'roadmap': 'Дорожная карта',
        'implementation': 'Реализация',
        # Mobile tabs (короткие версии)
        'home_short': 'Главная',
        'team_short': 'Команда',
        'why_us_short': 'О нас',
        'roadmap_short': 'Карта',
        'implementation_short': 'План'
    },
    'en': {
        # Desktop header
        'home': 'Home',
        'team': 'Team',
        'why_us': 'Why Us',
        'roadmap': 'Roadmap',
        'implementation': 'Implementation',
        # Mobile tabs (короткие версии)
        'home_short': 'Home',
        'team_short': 'Team',
        'why_us_short': 'About',
        'roadmap_short': 'Map',
        'implementation_short': 'Plan'
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
        'description': 'Люди с хроническими заболеваниями (диабет, целиакия, пищевые аллергии) сталкиваются с серьёзными трудностями:',
        'challenges': [
            {'icon': 'clock', 'text': 'Тратят много времени на изучение состава продуктов'},
            {'icon': 'search', 'text': 'Сложно найти мелкий шрифт на упаковках'},
            {'icon': 'exclamation-circle', 'text': 'Ошибки могут привести к серьёзным последствиям для здоровья'},
            {'icon': 'question-circle', 'text': 'Непонятные химические названия ингредиентов'},
            {'icon': 'tired', 'text': 'Постоянный стресс при покупке продуктов'}
        ],
        'stat_number': '~60 млн',
        'stat_label': 'человек в мире живут с диабетом и аллергиями'
    },
    'en': {
        'icon': 'exclamation-triangle',
        'title': 'Problem',
        'description': 'People with chronic diseases (diabetes, celiac disease, food allergies) face serious difficulties:',
        'challenges': [
            {'icon': 'clock', 'text': 'Spend a lot of time studying product composition'},
            {'icon': 'search', 'text': 'Difficult to find small print on packages'},
            {'icon': 'exclamation-circle', 'text': 'Mistakes can lead to serious health consequences'},
            {'icon': 'question-circle', 'text': 'Incomprehensible chemical names of ingredients'},
            {'icon': 'tired', 'text': 'Constant stress when buying products'}
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
        'description': 'Smart Care использует компьютерное зрение и AI для мгновенного анализа продуктов через камеру смартфона.',
        'steps': [
            {'icon': 'camera', 'title': 'Сканируй', 'description': 'Наведи камеру на продукт'},
            {'icon': 'brain', 'title': 'Анализируй', 'description': 'AI обрабатывает состав'},
            {'icon': 'check-circle', 'title': 'Получай ответ', 'description': 'Безопасно или нет'}
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
        'description': 'Smart Care uses computer vision and AI for instant product analysis via smartphone camera.',
        'steps': [
            {'icon': 'camera', 'title': 'Scan', 'description': 'Point camera at product'},
            {'icon': 'brain', 'title': 'Analyze', 'description': 'AI processes composition'},
            {'icon': 'check-circle', 'title': 'Get Answer', 'description': 'Safe or not'}
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
        'items': [
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
        'items': [
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

# Члены команды (ПРАВИЛЬНАЯ СТРУКТУРА: ru/en разделены)
team_members = [
    {
        'id': 'asadbek',
        'ru': {
            'name': 'Асадбек Фазлиддинов',
            'role': 'Team Lead & Developer',
            'experience': ['Yandex Taxi', 'Uzum Market'],
            'responsibilities': 'Руководство командой, разработка backend на Flask, интеграция ML моделей, создание API',
            'links': {
                'linkedin': 'https://www.linkedin.com/in/asadbek-fazliddinov',
                'github': '#',
                'portfolio': '#'
            }
        },
        'en': {
            'name': 'Asadbek Fazliddinov',
            'role': 'Team Lead & Developer',
            'experience': ['Yandex Taxi', 'Uzum Market'],
            'responsibilities': 'Team leadership, Flask backend development, ML model integration, API creation',
            'links': {
                'linkedin': 'https://www.linkedin.com/in/asadbek-fazliddinov',
                'github': '#',
                'portfolio': '#'
            }
        }
    },
    {
        'id': 'saydullo',
        'ru': {
            'name': 'Сайдулло Султонов',
            'role': 'Business Researcher',
            'experience': ['Ermak', 'abnmb group', 'Cau medical'],
            'responsibilities': 'Анализ рынка и конкурентов, исследование потребностей пользователей, разработка бизнес-модели',
            'links': {
                'linkedin': 'https://www.linkedin.com/in/saydullo-sultonov-837347255/',
                'github': '#',
                'portfolio': '#'
            }
        },
        'en': {
            'name': 'Saydullo Sultonov',
            'role': 'Business Researcher',
            'experience': ['Ermak', 'abnmb group', 'Cau medical'],
            'responsibilities': 'Market and competitor analysis, user needs research, business model development',
            'links': {
                'linkedin': 'https://www.linkedin.com/in/saydullo-sultonov-837347255/',
                'github': '#',
                'portfolio': '#'
            }
        }
    }
]

# Почему мы
why_us_data = {
    'ru': {
        'title': 'Почему именно мы',
        'subtitle': 'Что делает нашу команду особенной',
        'icon': 'star',
        'reasons': [
            {
                'icon': 'graduation-cap',
                'title': 'Экспертиза',
                'description': 'Наша команда объединяет экспертов в области компьютерного зрения, машинного обучения и разработки мобильных приложений. Совокупный опыт команды - более 15 лет в IT.'
            },
            {
                'icon': 'heart',
                'title': 'Личная мотивация',
                'description': 'У каждого из нас есть близкие люди с хроническими заболеваниями. Мы не просто создаём продукт - мы решаем реальную проблему, с которой сталкиваемся сами.'
            },
            {
                'icon': 'rocket',
                'title': 'Инновационный подход',
                'description': 'Мы используем последние достижения в области AI и computer vision, адаптируя их для решения конкретной социально значимой задачи.'
            },
            {
                'icon': 'users-cog',
                'title': 'Команда полного цикла',
                'description': 'От исследования и разработки ML-моделей до создания user-friendly мобильного приложения - мы контролируем весь процесс разработки.'
            },
            {
                'icon': 'chart-line',
                'title': 'Опыт реализации',
                'description': 'Члены нашей команды успешно запустили несколько проектов, включая мобильные приложения с ML-компонентами и веб-сервисы с высокой нагрузкой.'
            },
            {
                'icon': 'handshake',
                'title': 'Партнёрства',
                'description': 'Мы активно взаимодействуем с медицинскими специалистами и организациями пациентов для создания действительно полезного решения.'
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
        'reasons': [
            {
                'icon': 'graduation-cap',
                'title': 'Expertise',
                'description': 'Our team brings together experts in computer vision, machine learning, and mobile app development. Combined team experience - over 15 years in IT.'
            },
            {
                'icon': 'heart',
                'title': 'Personal Motivation',
                'description': 'Each of us has loved ones with chronic diseases. We\'re not just creating a product - we\'re solving a real problem we face ourselves.'
            },
            {
                'icon': 'rocket',
                'title': 'Innovative Approach',
                'description': 'We use the latest achievements in AI and computer vision, adapting them to solve a specific socially significant task.'
            },
            {
                'icon': 'users-cog',
                'title': 'Full-Cycle Team',
                'description': 'From research and ML model development to creating a user-friendly mobile app - we control the entire development process.'
            },
            {
                'icon': 'chart-line',
                'title': 'Implementation Experience',
                'description': 'Our team members have successfully launched several projects, including mobile apps with ML components and high-load web services.'
            },
            {
                'icon': 'handshake',
                'title': 'Partnerships',
                'description': 'We actively collaborate with medical professionals and patient organizations to create a truly useful solution.'
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
        'current_stage': 'Разработка MVP',
        'stage_label': 'Текущий этап:',
        'next_steps_title': 'Следующие шаги',
        'status_completed': 'Завершено',
        'status_in_progress': 'В процессе',
        'status_upcoming': 'Планируется'
    },
    'en': {
        'title': 'Project Roadmap',
        'subtitle': 'Our journey from idea to launch',
        'icon': 'road',
        'current_stage': 'MVP Development',
        'stage_label': 'Current Stage:',
        'next_steps_title': 'Next Steps',
        'status_completed': 'Completed',
        'status_in_progress': 'In Progress',
        'status_upcoming': 'Upcoming'
    }
}

# Реализация (НОВАЯ СЕКЦИЯ - ранее отсутствовала!)
implementation_data = {
    'ru': {
        'title': 'Как мы планируем реализовать решение',
        'subtitle': 'Технический подход и архитектура',
        'icon': 'rocket',
        'components_title': 'Ключевые компоненты решения',
        'tech_stack_title': 'Технологический стек',
        'implementation_steps_title': 'Этапы реализации',
        'unique_features_title': 'Уникальные особенности',
        
        # Категории технологий
        'tech_categories': [
            {
                'icon': 'mobile-alt',
                'title': 'Мобильная разработка',
                'technologies': [
                    {'name': 'React Native', 'description': 'Кроссплатформенная разработка для iOS и Android'},
                    {'name': 'Expo', 'description': 'Ускоренная разработка и тестирование'}
                ]
            },
            {
                'icon': 'brain',
                'title': 'Машинное обучение',
                'technologies': [
                    {'name': 'TensorFlow / PyTorch', 'description': 'Обучение и деплой ML-моделей'},
                    {'name': 'OpenCV', 'description': 'Обработка изображений и распознавание объектов'},
                    {'name': 'Tesseract OCR', 'description': 'Распознавание текста с упаковок'}
                ]
            },
            {
                'icon': 'server',
                'title': 'Backend',
                'technologies': [
                    {'name': 'Python + Flask/FastAPI', 'description': 'Быстрая разработка REST API'},
                    {'name': 'PostgreSQL', 'description': 'Хранение данных пользователей и продуктов'},
                    {'name': 'Redis', 'description': 'Кэширование частых запросов'}
                ]
            },
            {
                'icon': 'cloud',
                'title': 'Инфраструктура',
                'technologies': [
                    {'name': 'Docker', 'description': 'Контейнеризация сервисов'},
                    {'name': 'AWS / GCP', 'description': 'Облачная инфраструктура'},
                    {'name': 'CI/CD', 'description': 'Автоматизация деплоя'}
                ]
            }
        ],
        
        # Этапы реализации
        'implementation_steps': [
            {
                'badge': 'Этап 1',
                'title': 'Сбор и подготовка данных',
                'tasks': [
                    'Создание датасета изображений продуктов',
                    'Аннотация и разметка данных',
                    'Построение базы данных ингредиентов'
                ]
            },
            {
                'badge': 'Этап 2',
                'title': 'Обучение ML-моделей',
                'tasks': [
                    'Обучение модели распознавания объектов',
                    'Тренировка OCR для чтения состава',
                    'NLP для понимания названий ингредиентов'
                ]
            },
            {
                'badge': 'Этап 3',
                'title': 'Разработка backend',
                'tasks': [
                    'Создание REST API',
                    'Интеграция ML-моделей',
                    'Настройка базы данных'
                ]
            },
            {
                'badge': 'Этап 4',
                'title': 'Разработка мобильного приложения',
                'tasks': [
                    'Дизайн UI/UX',
                    'Реализация функционала камеры',
                    'Интеграция с backend API'
                ]
            },
            {
                'badge': 'Этап 5',
                'title': 'Тестирование и оптимизация',
                'tasks': [
                    'Unit и интеграционные тесты',
                    'Тестирование с пользователями',
                    'Оптимизация производительности'
                ]
            },
            {
                'badge': 'Этап 6',
                'title': 'Деплой и масштабирование',
                'tasks': [
                    'Настройка облачной инфраструктуры',
                    'Мониторинг и логирование',
                    'Публикация в App Store / Google Play'
                ]
            }
        ],
        
        # Уникальные особенности
        'unique_features': [
            {'icon': 'bolt', 'title': 'Мгновенный анализ', 'description': 'Результат за 2-3 секунды'},
            {'icon': 'wifi', 'title': 'Offline режим', 'description': 'Работа без интернета'},
            {'icon': 'user-cog', 'title': 'Персонализация', 'description': 'Учёт личных ограничений'},
            {'icon': 'database', 'title': 'База данных', 'description': '50,000+ продуктов'}
        ]
    },
    'en': {
        'title': 'How We Plan to Implement the Solution',
        'subtitle': 'Technical approach and architecture',
        'icon': 'rocket',
        'components_title': 'Key Solution Components',
        'tech_stack_title': 'Technology Stack',
        'implementation_steps_title': 'Implementation Stages',
        'unique_features_title': 'Unique Features',
        
        # Technology categories
        'tech_categories': [
            {
                'icon': 'mobile-alt',
                'title': 'Mobile Development',
                'technologies': [
                    {'name': 'React Native', 'description': 'Cross-platform development for iOS and Android'},
                    {'name': 'Expo', 'description': 'Accelerated development and testing'}
                ]
            },
            {
                'icon': 'brain',
                'title': 'Machine Learning',
                'technologies': [
                    {'name': 'TensorFlow / PyTorch', 'description': 'ML model training and deployment'},
                    {'name': 'OpenCV', 'description': 'Image processing and object recognition'},
                    {'name': 'Tesseract OCR', 'description': 'Text recognition from packages'}
                ]
            },
            {
                'icon': 'server',
                'title': 'Backend',
                'technologies': [
                    {'name': 'Python + Flask/FastAPI', 'description': 'Fast REST API development'},
                    {'name': 'PostgreSQL', 'description': 'User and product data storage'},
                    {'name': 'Redis', 'description': 'Frequent query caching'}
                ]
            },
            {
                'icon': 'cloud',
                'title': 'Infrastructure',
                'technologies': [
                    {'name': 'Docker', 'description': 'Service containerization'},
                    {'name': 'AWS / GCP', 'description': 'Cloud infrastructure'},
                    {'name': 'CI/CD', 'description': 'Deploy automation'}
                ]
            }
        ],
        
        # Implementation stages
        'implementation_steps': [
            {
                'badge': 'Stage 1',
                'title': 'Data Collection and Preparation',
                'tasks': [
                    'Creating product image dataset',
                    'Data annotation and labeling',
                    'Building ingredient database'
                ]
            },
            {
                'badge': 'Stage 2',
                'title': 'ML Model Training',
                'tasks': [
                    'Training object detection model',
                    'OCR training for composition reading',
                    'NLP for ingredient name understanding'
                ]
            },
            {
                'badge': 'Stage 3',
                'title': 'Backend Development',
                'tasks': [
                    'Creating REST API',
                    'ML model integration',
                    'Database setup'
                ]
            },
            {
                'badge': 'Stage 4',
                'title': 'Mobile App Development',
                'tasks': [
                    'UI/UX Design',
                    'Camera functionality implementation',
                    'Backend API integration'
                ]
            },
            {
                'badge': 'Stage 5',
                'title': 'Testing and Optimization',
                'tasks': [
                    'Unit and integration tests',
                    'User testing',
                    'Performance optimization'
                ]
            },
            {
                'badge': 'Stage 6',
                'title': 'Deployment and Scaling',
                'tasks': [
                    'Cloud infrastructure setup',
                    'Monitoring and logging',
                    'App Store / Google Play publishing'
                ]
            }
        ],
        
        # Unique features
        'unique_features': [
            {'icon': 'bolt', 'title': 'Instant Analysis', 'description': 'Results in 2-3 seconds'},
            {'icon': 'wifi', 'title': 'Offline Mode', 'description': 'Works without internet'},
            {'icon': 'user-cog', 'title': 'Personalization', 'description': 'Personal restriction tracking'},
            {'icon': 'database', 'title': 'Database', 'description': '50,000+ products'}
        ]
    }
}

# Этапы roadmap (ПРАВИЛЬНАЯ СТРУКТУРА: ru/en разделены)
milestones = [
    {
        'id': 'milestone_1',
        'ru': {
            'title': 'Исследование и концепция',
            'date': 'Ноябрь 2024',
            'status': 'completed',
            'description': 'Анализ проблемы, исследование рынка, разработка концепции'
        },
        'en': {
            'title': 'Research and Concept',
            'date': 'November 2024',
            'status': 'completed',
            'description': 'Problem analysis, market research, concept development'
        }
    },
    {
        'id': 'milestone_2',
        'ru': {
            'title': 'Прототип MVP',
            'date': 'Декабрь 2024',
            'status': 'in_progress',
            'description': 'Разработка базового функционала, обучение ML модели'
        },
        'en': {
            'title': 'MVP Prototype',
            'date': 'December 2024',
            'status': 'in_progress',
            'description': 'Basic functionality development, ML model training'
        }
    },
    {
        'id': 'milestone_3',
        'ru': {
            'title': 'Тестирование',
            'date': 'Январь 2025',
            'status': 'upcoming',
            'description': 'Альфа-тестирование с фокус-группой пользователей'
        },
        'en': {
            'title': 'Testing',
            'date': 'January 2025',
            'status': 'upcoming',
            'description': 'Alpha testing with focus group of users'
        }
    },
    {
        'id': 'milestone_4',
        'ru': {
            'title': 'Публичный релиз',
            'date': 'Февраль 2025',
            'status': 'upcoming',
            'description': 'Запуск приложения в App Store и Google Play'
        },
        'en': {
            'title': 'Public Release',
            'date': 'February 2025',
            'status': 'upcoming',
            'description': 'Launch app in App Store and Google Play'
        }
    }
]

# Следующие шаги (ПРАВИЛЬНАЯ СТРУКТУРА: ru/en разделены)
next_steps = [
    {
        'id': 'step_1',
        'ru': {
            'title': 'Завершение MVP',
            'description': 'Финализация основного функционала и интеграция всех компонентов',
            'number': 1
        },
        'en': {
            'title': 'Complete MVP',
            'description': 'Finalize core functionality and integrate all components',
            'number': 1
        }
    },
    {
        'id': 'step_2',
        'ru': {
            'title': 'Бета-тестирование',
            'description': 'Запуск закрытого тестирования с фокус-группой из 100 пользователей',
            'number': 2
        },
        'en': {
            'title': 'Beta Testing',
            'description': 'Launch closed testing with focus group of 100 users',
            'number': 2
        }
    },
    {
        'id': 'step_3',
        'ru': {
            'title': 'Оптимизация модели',
            'description': 'Улучшение точности и скорости распознавания на основе feedback',
            'number': 3
        },
        'en': {
            'title': 'Model Optimization',
            'description': 'Improve accuracy and recognition speed based on feedback',
            'number': 3
        }
    },
    {
        'id': 'step_4',
        'ru': {
            'title': 'Публичный релиз',
            'description': 'Запуск приложения в App Store и Google Play',
            'number': 4
        },
        'en': {
            'title': 'Public Release',
            'description': 'Launch app in App Store and Google Play',
            'number': 4
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
        'copyright': '© 2025 Smart Care. Все права защищены.',
        'tagline': 'Создано с ❤️ для хакатона'
    },
    'en': {
        'copyright': '© 2025 Smart Care. All rights reserved.',
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
    
    # Члены команды (ОБНОВЛЕННАЯ СТРУКТУРА)
    for member in team_members:
        firestore_service.create_document(
            'team_members',
            member['id'],
            {
                'ru': member['ru'],
                'en': member['en']
            }
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
    
    # Milestones (ОБНОВЛЕННАЯ СТРУКТУРА)
    for milestone in milestones:
        firestore_service.create_document(
            'roadmap_milestones',
            milestone['id'],
            {
                'ru': milestone['ru'],
                'en': milestone['en']
            }
        )
    
    # Next steps (ОБНОВЛЕННАЯ СТРУКТУРА)
    for step in next_steps:
        firestore_service.create_document(
            'roadmap_next_steps',
            step['id'],
            {
                'ru': step['ru'],
                'en': step['en']
            }
        )
    
    print("✓ Дорожная карта загружена\n")

def upload_implementation():
    """Загрузка секции реализации (НОВАЯ ФУНКЦИЯ)"""
    print("🚀 Загрузка секции реализации...")
    for lang in ['ru', 'en']:
        firestore_service.create_document(
            'translations',
            f'{lang}_implementation',
            implementation_data[lang]
        )
    print("✓ Секция реализации загружена\n")

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
        upload_implementation()  # НОВАЯ ФУНКЦИЯ!
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
        print("  • Реализация (новая секция)")
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

