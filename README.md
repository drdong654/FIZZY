<h1 align="center">
  <a href="https://git.io/typing-svg">
    <img src="https://readme-typing-svg.demolab.com/?lines=FIZZY+%7C+SOCIAL+LISTENING&center=true&width=650&size=32&color=FFFFFF" alt="FIZZY | SOCIAL LISTENING">
  </a>
</h1>

<p align="center">
  Мониторинг упоминаний бренда и продуктов в одном месте.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white" alt="Python 3.13">
  <img src="https://img.shields.io/badge/aiogram-3-2CA5E0?logo=telegram&logoColor=white" alt="aiogram 3">
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white" alt="PostgreSQL">
</p>

---

## О проекте

**FIZZY** — проект для мониторинга упоминаний компании и её продуктов. Он помогает понять, что пишет аудитория, как меняется тональность сообщений и восприятие бренда.

Проект находится в разработке.

## Что есть сейчас

- Telegram-бот с командами `/start` и `/help`.
- Модели данных для событий, источников, сообщений, персон и упоминаний.
- Основа для дальнейшей обработки сообщений.

## Как будет работать система

```text
Источники → Сбор сообщений → raw_messages → Обработка → mentions → Результат
```

Текст сообщения хранится в `raw_messages`, а его связь с событием — в `mentions`. Персоны используются для создания синтетических публикаций.

## Быстрый старт

Понадобятся **Python 3.13**, **uv** и **PostgreSQL**.

```bash
uv venv
source .venv/bin/activate
uv sync
```

Создай файл окружения:

```bash
cp .env.example .env
```

Укажи в `.env` свои значения `BOT_TOKEN` и `DATABASE_URL`, затем запусти бота:

```bash
python -m bot.main
```

> Подключение и настройка базы данных ещё находятся в разработке.

## Стек

`Python 3.13` · `asyncio` · `aiogram` · `SQLAlchemy` · `PostgreSQL`

## Структура проекта

```text
.
├── bot/             Telegram-бот
├── db/              модели и схема базы данных
├── docs/            планы и заметки
├── media/           изображения проекта
├── src/fizzy/       Python-пакет
├── pyproject.toml   зависимости и настройки проекта
└── uv.lock          зафиксированные версии зависимостей
```

## Планы

- Собирать сообщения из источников.
- Находить упоминания заданных событий и ключевых слов.
- Анализировать тональность и динамику упоминаний.
- Показывать результаты через бота.
