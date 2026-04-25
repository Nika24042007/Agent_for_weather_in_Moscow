# Agent_for_weather_in_Moscow. Track A

**Цель:** создать ИИ-агента, который может работать с API
**Библиотеки:** openai (для самого агента), requests (для работы с API), os, dotenv

**ТЗ:**
- агент принимает запрос пользователя  
- при необходимости вызывает API  
- обрабатывает результат  
- формирует ответ

**LLM:** Qwen
**API:** Яндекс.Погода

## Структура

<pre>
    .
    ├── Agent                                  
    │   ├── main.py                            # файл запуска
    │   ├── agent.py                           # Сам агент и функция инструмета
    │   ├── tools.py                           # Описание инструмента для агента
    │   ├── .gitignore                         # git ignore файл
    │   ├── README.md                          # Описание содержания проекта
    │   ├── REFLECTION.md                      # Эссе
    │   ├── README.md - Agent_for_weather_in_Moscow - Visual Studio Code 2026-04-25 09-31-48.mp4 # Запись работы агента
</pre>

## Запуск
python -m main

