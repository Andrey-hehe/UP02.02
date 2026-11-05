# Python Diff — модуль сравнения файлов

## Описание проекта

Python Diff — модуль для сравнения двух версий файлов. Позволяет находить добавленные, удалённые и изменённые строки, сравнивать JSON-файлы по отдельным полям и создавать HTML-отчёты.

## Возможности

- Чтение текстовых файлов.
- Чтение и форматирование JSON.
- Поиск добавленных, удалённых и изменённых строк.
- Сравнение JSON по отдельным полям.
- Создание HTML-отчётов с различиями между файлами.

## Технологии

- Python 3.12
- difflib
- json
- pathlib
- argparse
- unittest

Используются стандартные библиотеки Python.

## Структура проекта

```text
UP02.02/
├── .github/
├── src/
│   ├── __init__.py
│   └── main.py
├── tests/
│   └── test_diff.py
├── examples/
│   ├── first.txt
│   ├── second.txt
│   ├── first.json
│   ├── second.json
│   └── test_json.py
├── docs/
├── README.md
└── .gitignore
```

## Установка и запуск

1. Клонировать репозиторий:

```bash
git clone https://github.com/Andrey-hehe/UP02.02.git
```

2. Перейти в папку проекта:

```bash
cd UP02.02
```

3. Запустить сравнение файлов:

```bash
python src/main.py first.txt second.txt -o report.html
```

После выполнения будет создан HTML-отчёт `report.html`.

## Использование JSON-сравнения

Функция `compare_json()` позволяет сравнивать JSON-файлы по отдельным полям.

Пример:

```python
from src.main import compare_json

result = compare_json("first.json", "second.json")
print(result)
```

Результат содержит три категории:

- `added` — добавленные поля.
- `deleted` — удалённые поля.
- `modified` — изменённые поля с предыдущим и новым значением.

## Основные функции

| Функция | Назначение |
|---|---|
| `read_file()` | Чтение файла |
| `get_changes()` | Поиск различий между строками |
| `compare_json()` | Сравнение JSON по полям |
| `compare_files()` | Создание HTML-отчёта |
| `save_report()` | Сохранение HTML-отчёта |

## Запуск тестов

```bash
python -m unittest discover -s tests -v
```

## Проверка качества кода

Проверка Ruff:

```bash
ruff check src tests
```

Проверка форматирования:

```bash
ruff format --check src tests
```