# Шаурмания — Flask-версия

Flask-приложение на основе статичного лендинга [mshqq/shaurmania](https://github.com/mshqq/shaurmania) — учебного проекта второго семестра. Оригинал — чистый HTML/CSS/JS без фреймворков; здесь к нему добавлен Python-бэкенд с рабочей формой подписки.

![Превью сайта](static/img/preview.png)

## Что добавлено поверх шаблона

| Оригинал ([mshqq/shaurmania](https://github.com/mshqq/shaurmania)) | Эта версия |
|------|------|
| Статичный HTML-лендинг | Flask-приложение |
| Форма подписки — только вёрстка | Форма реально отправляет письмо на e-mail пользователя |
| Деплой через GitHub Pages | Запуск через Python |

## Стек

- **Python / Flask** — бэкенд, роутинг
- **Flask-WTF** — валидация формы + CSRF-защита
- **smtplib** — отправка HTML-писем через Gmail SMTP
- **python-dotenv** — секреты через `.env`
- **HTML / CSS / JS** — фронтенд из оригинального шаблона (без изменений)

## Быстрый старт

```bash
git clone <url-репозитория>
cd ShaurmaniaApp

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

pip install -r requirements.txt
```

Создайте `.env`:

```env
SECRET_KEY=any-random-string
app_password=your-gmail-app-password
```

> `app_password` — [пароль приложения Gmail](https://myaccount.google.com/apppasswords), не основной пароль. Требует включённой 2FA.

```bash
python app.py
# → http://127.0.0.1:5000
```

## Структура проекта

```
ShaurmaniaApp/
├── app.py                       # Flask, маршруты, форма
├── mail.py                      # Отправка письма через Gmail SMTP
├── templates/
│   ├── index.html               # Лендинг (адаптирован из шаблона)
│   └── email_subscription.html  # HTML-письмо подписки
└── static/                      # CSS, JS, изображения из шаблона
```
