# pyUFO-db: Python Unified Flexible Object Database

[![Documentation](https://img.shields.io/badge/Docs-green?style=flat&logo=github&labelColor=gray&link=https://github.com/SL1dee36/pyufo-db/blob/main/DOCS.md)](https://github.com/SL1dee36/pyufo-db/blob/main/DOCS.md)


pyUFO-db (Python Unified Flexible Object Database) - это легковесная объектно-ориентированная база данных, написанная на Python.  Она предоставляет простой интерфейс для создания, управления и хранения структурированных данных в памяти и на диске. pyUFO-db вдохновлена проектом [UFO-DB](https://github.com/atxxxm/UFO-DB), написанным на C++, но переосмыслена и реализована на Python для большей гибкости и простоты использования.  **Важно:** pyUFO-db не предназначена для хранения информации об НЛО, а является универсальной базой данных для любых данных.

## Установка

Вы можете установить pyUFO-db с помощью pip:

```bash
pip install py-ufo-db
```

Или клонировать репозиторий с GitHub:

```bash
git clone https://github.com/SL1dee36/pyufo-db.git
```

## Документация

Полная документация доступна по ссылке: [DOCS.md](https://github.com/SL1dee36/pyufo-db/blob/main/DOCS.md)

## Основные возможности

* **Простота использования:** pyUFO-db предоставляет интуитивно понятный API для работы с данными.
* **Гибкость:**  Поддерживает динамическую структуру таблиц - вы можете добавлять и изменять столбцы по мере необходимости.
* **Сохранение на диск:**  Возможность сохранять и загружать данные из файла для персистентного хранения.
* **Обработка ошибок:** Встроенная обработка распространенных ошибок, таких как дублирование имен таблиц и доступ к несуществующим данным.
* **Кодировка UTF-8:** Поддержка Unicode для хранения данных на различных языках.

## Пример использования

```python
from py_ufo_db import Relative_DB

db = Relative_DB()
db.create_table("users", ["name", "email", "age"])
db.insert("users", {"name": "John Doe", "email": "john.doe@example.com", "age": "30"})
db.insert("users", {"name": "Jane Smith", "email": "jane.smith@example.com", "age": "25"})
db.select("users")
db.update("users", 1, {"age": "31"})
db.select("users")
db.delete_record("users", 2)
db.select("users")
db.save_to_file("users.db")

db2 = Relative_DB()
db2.load_from_file("users.db")
db2.select("users")

```

## Контрибуции

Вклады приветствуются! Пожалуйста, создавайте запросы на включение (pull requests) или открывайте issues в репозитории GitHub.

## Лицензия

MIT License

## Контакты

[Мой GitHub](https://github.com/sl1dee36)

## Благодарности

* [atxxxm](https://github.com/atxxxm) за оригинальный проект [UFO-DB](https://github.com/atxxxm/UFO-DB) на C++.
