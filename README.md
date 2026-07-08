# Шаурмания — Flask-версия

Flask-приложение на основе статичного лендинга [mshqq/shaurmania](https://github.com/mshqq/shaurmania) — учебного проекта второго семестра. Оригинал — чистый HTML/CSS/JS без фреймворков; здесь к нему добавлен Python-бэкенд на базе SQLite с веб-формами, API каталога/заказов и механизмом подписок.

![Превью сайта](app/static/img/preview.png)

## Что добавлено поверх шаблона

| Оригинал ([mshqq/shaurmania](https://github.com/mshqq/shaurmania)) | Эта версия |
|------|------|
| Статичный HTML-лендинг | Flask-приложение (модульная структура Flask Package) |
| Вёрстка формы подписки | Сохранение подписчиков в БД + генерация токенов для отписки |
| Только вёрстка товаров/заказов | Архитектура БД (модели продуктов, категорий, точек выдачи и заказов) + API-эндпоинты |
| Деплой через GitHub Pages | Запуск через Python Flask сервер |

## Стек

- **Python / Flask / Flask-SQLAlchemy** — бэкенд, роутинг, ORM-модели
- **Flask-WTF / WTForms** — валидация формы подписки + CSRF-защита
- **SQLite** — локальная СУБД для хранения данных
- **smtplib (опционально)** — отправка HTML-писем через Gmail SMTP (код находится в `mail.py`, в маршрутах по умолчанию закомментирован)
- **python-dotenv** — секреты и настройки через `.env`
- **HTML / CSS / JS** — адаптированный фронтенд из оригинального шаблона

## Быстрый старт

1. Склонируйте репозиторий:
```bash
git clone <url-репозитория>
cd ShaurmaniaApp
```

2. Настройте виртуальное окружение и установите зависимости:
```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

pip install -r requirements.txt
```

3. Создайте файл `.env` в корне проекта:
```env
SECRET_KEY=any-random-string
app_password=your-gmail-app-password
```

> **Примечание:** `app_password` необходим только для отправки писем. Это [пароль приложения Gmail](https://myaccount.google.com/apppasswords) (требует включённой двухфакторной аутентификации в аккаунте Google).

4. Запустите Flask-сервер:
```bash
python app.py
# → http://127.0.0.1:5000
```
При первом запуске база данных SQLite (`instance/shaurmania.db`) и все таблицы будут созданы автоматически.

---

## Структура проекта

```
ShaurmaniaApp/
├── app.py                       # Точка запуска (вызывает create_app())
├── mail.py                      # Отправка писем через Gmail SMTP (отдельный скрипт)
├── requirements.txt             # Зависимости проекта
├── .env                         # Переменные окружения (не коммитится в Git)
├── app/                         # Основной пакет приложения
│   ├── __init__.py              # Инициализация Flask, БД и CSRF
│   ├── extensions.py            # Объявление расширений SQLAlchemy и CSRFProtect
│   ├── forms.py                 # Классы форм (SubscriptionForm)
│   ├── models.py                # Модели базы данных (Location, Category, Product, Order, OrderItems, Subscriber)
│   ├── routes.py                # Обработчики страниц и API-эндпоинтов
│   ├── templates/               # HTML-шаблоны веб-страниц и писем
│   │   ├── index.html           # Главный шаблон лендинга
│   │   └── email_subscription.html # Шаблон отправляемого письма
│   └── static/                  # Стили CSS, скрипты JS, шрифты и изображения
└── instance/                    # Папка с локальной базой данных SQLite (создаётся при запуске)
    └── shaurmania.db
```

---

## База данных и API-эндпоинты

В приложении спроектирована база данных с моделями SQLAlchemy:
* `Subscriber` — подписчики рассылки с уникальным UUID-токеном безопасности.
* `Category` и `Product` — список товаров и категорий.
* `Order` и `OrderItems` — заказы и состав (товары, количества).
* `Location` — адреса ресторанов.

### API Эндпоинты

* **Каталог и заказы:**
  * `GET /api/products` — возвращает список всех товаров в формате JSON.
  * `POST /api/order` — принимает JSON с корзиной покупателя и его контактными данными, рассчитывает сумму заказа и логирует информацию в консоли.
  * `GET /api/orders` — тестовый метод для получения списка всех ID заказов и их позиций.
* **Подписки и рассылки:**
  * `POST /api/subscribe` — принимает форму подписки, валидирует адрес почты и сохраняет запись в БД `Subscriber`.
  * `GET /unsubscribe/<token>` — отписывает пользователя от рассылки по его уникальному UUID-токену (меняет `is_active` класса `Subscriber` в `False`).
  * `GET /admin/subscribers` — JSON-список всех активных подписчиков системы.

> **Как включить реальную отправку писем на почту:** раскомментируйте импорт `sendEmail` и строки вызова `sendEmail(app_password, name, email)` в файле `app/routes.py`, указав корректные параметры доступа в файле `.env` и отправителя в `mail.py`.

