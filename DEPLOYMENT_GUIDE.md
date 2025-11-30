# 🚀 Руководство по деплою Smart Care

## Бесплатные платформы для деплоя

### ✅ Рекомендуется: Render.com

**Почему Render?**
- ✅ Бесплатный tier навсегда
- ✅ Автоматический деплой из GitHub
- ✅ Поддержка Python/Flask из коробки
- ✅ Environment variables
- ✅ SSL сертификаты (HTTPS)
- ✅ Логи в реальном времени

**Ограничения бесплатного tier:**
- 🕒 Спящий режим после 15 минут неактивности
- ⚡ Первый запуск может быть медленным (~30 секунд)
- 💾 512 MB RAM
- 🌍 1 регион (можно выбрать ближайший)

---

## 📋 Шаг 1: Подготовка проекта

### 1.1 Создайте Git репозиторий

```bash
cd /Users/asadfaza/Documents/Grad\ Project/application/safe_care

# Инициализация git (если еще не сделано)
git init

# Добавьте все файлы
git add .

# Коммит
git commit -m "Initial commit: Smart Care application"
```

### 1.2 Создайте GitHub репозиторий

1. Зайдите на [GitHub.com](https://github.com)
2. Нажмите **New repository**
3. Название: `smart-care-app`
4. Visibility: **Public** или **Private**
5. Нажмите **Create repository**

### 1.3 Push в GitHub

```bash
# Добавьте remote
git remote add origin https://github.com/ВАШ_USERNAME/smart-care-app.git

# Push
git branch -M main
git push -u origin main
```

---

## 🌐 Шаг 2: Деплой на Render.com

### 2.1 Регистрация

1. Зайдите на [render.com](https://render.com)
2. Нажмите **Get Started for Free**
3. Войдите через **GitHub** (рекомендуется)

### 2.2 Создание Web Service

1. На dashboard нажмите **New +**
2. Выберите **Web Service**
3. Подключите ваш GitHub репозиторий `smart-care-app`
4. Нажмите **Connect**

### 2.3 Настройка сервиса

**Основные настройки:**
```
Name: smart-care
Region: Frankfurt (для Европы) или Oregon (для США)
Branch: main
Root Directory: (оставьте пустым)
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
Instance Type: Free
```

### 2.4 Environment Variables

Нажмите **Advanced** и добавьте переменные:

| Key | Value |
|-----|-------|
| `FLASK_ENV` | `production` |
| `SECRET_KEY` | `ваш-секретный-ключ-минимум-32-символа` |
| `FIREBASE_CREDENTIALS_PATH` | `firebase-credentials.json` |

**Для генерации SECRET_KEY:**
```python
python -c "import secrets; print(secrets.token_hex(32))"
```

### 2.5 Firebase Credentials

**ВАЖНО!** Firebase credentials нужно добавить как **Secret File**:

1. В разделе **Environment**
2. Нажмите **Add Secret File**
3. Filename: `firebase-credentials.json`
4. Contents: вставьте содержимое вашего `firebase-credentials.json`
5. Нажмите **Save**

### 2.6 Deploy!

Нажмите **Create Web Service** внизу страницы.

Render начнет:
1. ✅ Клонировать репозиторий
2. ✅ Устанавливать зависимости
3. ✅ Запускать приложение

Процесс займет 3-5 минут.

---

## ✅ Шаг 3: Проверка

### 3.1 Получите URL

После успешного деплоя вы получите URL вида:
```
https://smart-care.onrender.com
```

### 3.2 Протестируйте

Откройте в браузере:
```
https://smart-care.onrender.com/
https://smart-care.onrender.com/en
https://smart-care.onrender.com/api/health
```

### 3.3 Проверьте логи

В dashboard Render:
- Перейдите в **Logs**
- Убедитесь, что приложение запустилось без ошибок
- Должна быть строка: `✓ Firestore: ✓ Подключен`

---

## 🔧 Шаг 4: Настройка автодеплоя

Render автоматически деплоит при каждом push в GitHub!

```bash
# Внесите изменения
git add .
git commit -m "Update content"
git push

# Render автоматически задеплоит за 2-3 минуты
```

---

## 🎨 Альтернативные платформы

### Вариант 2: Railway.app

**Плюсы:**
- 💵 $5 бесплатных кредитов каждый месяц
- ⚡ Быстрее чем Render
- 🔄 Не засыпает
- 💾 1GB RAM на free tier

**Шаги:**
1. [railway.app](https://railway.app) → Sign up
2. New Project → Deploy from GitHub
3. Выберите репозиторий
4. Add variables (как в Render)
5. Deploy

**URL:** `https://smart-care.railway.app`

---

### Вариант 3: Fly.io

**Плюсы:**
- 🌍 Много регионов
- 💾 256MB RAM бесплатно
- ⚡ Не засыпает

**Шаги:**
```bash
# Установка CLI
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Создание app
fly launch
# Следуйте инструкциям

# Добавьте secrets
fly secrets set FLASK_ENV=production
fly secrets set SECRET_KEY=your-secret-key

# Deploy
fly deploy
```

**URL:** `https://smart-care.fly.dev`

---

### Вариант 4: PythonAnywhere

**Плюсы:**
- 🎓 Бесплатный для студентов
- 📚 Хорошая документация
- 🕐 Без ограничений по времени

**Минусы:**
- ⚠️ Нет автодеплоя
- 🔗 URL вида: `username.pythonanywhere.com`
- 🌐 Нет custom domains на free tier

**Шаги:**
1. Зарегистрируйтесь на [pythonanywhere.com](https://www.pythonanywhere.com)
2. Dashboard → Web → Add a new web app
3. Выберите Flask
4. Upload код через Files или Git
5. Configure WSGI
6. Reload

---

## 🎯 Рекомендации для Production

### Безопасность

1. **SECRET_KEY**: используйте длинный случайный ключ
   ```python
   import secrets
   secrets.token_hex(32)
   ```

2. **Firebase Rules**: настройте правила безопасности
   ```javascript
   rules_version = '2';
   service cloud.firestore {
     match /databases/{database}/documents {
       match /{document=**} {
         allow read: if true;
         allow write: if false;  // Только чтение
       }
     }
   }
   ```

3. **CORS**: добавьте если нужно
   ```python
   from flask_cors import CORS
   CORS(app, origins=['https://smart-care.onrender.com'])
   ```

### Производительность

1. **Redis Cache** (если нужно):
   ```yaml
   # render.yaml - добавьте Redis
   - type: redis
     name: smart-care-cache
     plan: free
   ```

2. **CDN для статики**: используйте Cloudflare (бесплатно)

3. **Мониторинг**: 
   - Render Dashboard → Metrics
   - Или добавьте [Sentry.io](https://sentry.io) (бесплатный tier)

### Custom Domain

**На Render (платный план):**
```
Settings → Custom Domains → Add Domain
```

**Бесплатная альтернатива - Cloudflare:**
1. Зарегистрируйте домен на [Freenom](https://www.freenom.com) (бесплатно)
2. Добавьте в Cloudflare
3. Настройте CNAME на Render URL

---

## 📊 Мониторинг и обслуживание

### Проверка здоровья

```bash
# Health check
curl https://smart-care.onrender.com/api/health

# Ожидаемый ответ:
{
  "status": "healthy",
  "service": "smart_care",
  "version": "1.0.0",
  "firestore_available": true
}
```

### Логи

**Render:**
- Dashboard → Logs → Real-time logs

**Railway:**
- Project → Deployments → View Logs

**Fly.io:**
```bash
fly logs
```

### Обновление

```bash
# Локальные изменения
git add .
git commit -m "Update: ваше описание"
git push

# Render автоматически задеплоит
# Процесс займет 2-3 минуты
```

---

## ⚠️ Troubleshooting

### Проблема: Приложение не запускается

**Проверьте логи:**
```
Render → Logs
```

**Частые ошибки:**
1. **ModuleNotFoundError**: добавьте модуль в `requirements.txt`
2. **Firebase error**: проверьте `firebase-credentials.json`
3. **PORT error**: Render автоматически устанавливает `$PORT`

### Проблема: 503 Service Unavailable

**Причина**: Приложение "спит" (free tier)

**Решение**: подождите 30-60 секунд, пока оно "проснется"

**Альтернатива**: используйте uptime monitor (бесплатно):
- [UptimeRobot](https://uptimerobot.com)
- Ping каждые 5 минут → приложение не засыпает

### Проблема: Firestore недоступен

**Проверьте:**
1. Secret File `firebase-credentials.json` добавлен
2. Firebase project активен
3. Firestore database создана (Native mode)
4. Billing включен в Firebase (даже для free tier)

---

## 💰 Стоимость

### Полностью бесплатно:
- ✅ Render free tier (спит после 15 мин)
- ✅ Firebase Firestore (до 50K reads/day)
- ✅ GitHub (unlimited public repos)

### Если нужно больше:
- 💵 Render Starter: $7/месяц (не спит, 512MB RAM)
- 💵 Railway: $5/месяц (1GB RAM, не спит)
- 💵 Firebase Blaze: pay-as-you-go (от $0)

---

## 🎉 Итоговый чеклист

- [ ] Git репозиторий создан
- [ ] Код загружен на GitHub
- [ ] Render.com аккаунт создан
- [ ] Web Service настроен
- [ ] Environment variables добавлены
- [ ] Firebase credentials загружены
- [ ] Первый деплой успешен
- [ ] URL работает
- [ ] API endpoints отвечают
- [ ] Firestore подключен
- [ ] Переключение языков работает
- [ ] Автодеплой настроен

---

## 📞 Полезные ссылки

- [Render Docs](https://render.com/docs)
- [Railway Docs](https://docs.railway.app)
- [Fly.io Docs](https://fly.io/docs)
- [Firebase Console](https://console.firebase.google.com)
- [GitHub](https://github.com)

---

**Ваше приложение в production!** 🚀

*Smart Care Team*

