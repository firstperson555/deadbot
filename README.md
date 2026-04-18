# DeadBoot - Telegram Bot

Приватный сервис продвижения в TikTok, Telegram и YouTube на aiogram 3.x.

## Установка локально

1. Клонируйте репозиторий:
```bash
git clone https://github.com/ВАШ_USERNAME/deadbot.git
cd deadbot
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Установите переменную окружения:
```bash
export BOT_TOKEN="7588478024:AAHUd6_2ntEUmVOvl5UGtnAe8wnB8WDdjD0"
```

4. Запустите бота:
```bash
python main.py
```

## Развертывание на Railway

1. Зайдите на [railway.app](https://railway.app) и авторизуйтесь через GitHub

2. Создайте новый проект:
   - Нажмите "New Project"
   - Выберите "Deploy from GitHub repo"
   - Выберите ваш репозиторий `deadbot`

3. Добавьте переменные окружения:
   - В настройках проекта перейдите в "Variables"
   - Добавьте переменную `BOT_TOKEN` со значением вашего токена бота
   - `BOT_TOKEN=7588478024:AAHUd6_2ntEUmVOvl5UGtnAe8wnB8WDdjD0`

4. Разверните проект:
   - Railway автоматически определит Python проект
   - Нажмите "Deploy"

5. Бот будет доступен 24/7

## Структура проекта

```
deadbot/
├── main.py              # Главный файл запуска
├── requirements.txt     # Зависимости
├── Procfile            # Конфигурация для Railway
├── railway.json        # Конфигурация Railway
├── handlers/           # Обработчики
│   ├── __init__.py
│   └── router.py
├── states/             # FSM состояния
│   ├── __init__.py
│   └── states.py
└── keyboards/          # Клавиатуры
    ├── __init__.py
    └── keyboards.py
```

## Функции

- Выбор платформы (TikTok, Telegram, YouTube)
- Выбор услуги (Просмотры, Лайки, Подписчики)
- Валидация ссылок для каждой платформы
- Фиксированные количества (1000, 5000, 10000)
- Фиксированные цены (100, 500, 1000 Stars)
- Система отмены заказа
- Админ-панель для одобрения/отклонения заказов
- Логирование всех действий

## Админ

- **ID:** 7846160465
- **Username:** @nev3rdead
