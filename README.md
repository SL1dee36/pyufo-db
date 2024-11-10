# Python Unified Flexible Object Database

[![Documentation](https://img.shields.io/badge/Documentation-green?style=flat&logo=github&labelColor=gray&link=https://github.com/SL1dee36/pyufo-db/blob/main/Documentation/DOCS.md)](https://github.com/SL1dee36/pyufo-db/blob/main/Documentation/DOCS.md)


PY-UFO-DB (Python Unified Flexible Object Database) - это легковесная объектно-ориентированная база данных, написанная на Python.  Она предоставляет простой интерфейс для создания, управления и хранения структурированных данных в памяти и на диске. py-ufo-db вдохновлена проектом [UFO-DB](https://github.com/atxxxm/UFO-DB), написанным на C++, но переосмыслена и реализована на Python для большей гибкости и простоты использования.  

_**Важно:** PY-UFO-DB не предназначена для хранения информации об НЛО, а является универсальной базой данных для любых данных._

## Основные возможности

* **Простота использования:** py-ufo-db предоставляет интуитивно понятный API для работы с данными.
* **Гибкость:**  Поддерживает динамическую структуру таблиц - вы можете добавлять и изменять столбцы по мере необходимости.
* **Сохранение на диск:**  Возможность сохранять и загружать данные из файла для персистентного хранения.
* **Обработка ошибок:** Встроенная обработка распространенных ошибок, таких как дублирование имен таблиц и доступ к несуществующим данным.
* **Кодировка UTF-8:** Поддержка Unicode для хранения данных на различных языках.

## Установка

Вы можете установить pyufo-db с помощью pip:

```bash
pip install py-ufo-db
```

Или клонировать репозиторий с GitHub:

```bash
git clone https://github.com/SL1dee36/pyufo-db.git
```

## Документация

Полная документация доступна по ссылке: [DOCS.md](https://github.com/SL1dee36/pyufo-db/blob/main/Documentation/DOCS.md)

## Пример использования

```python
from pyufodb import *

db = RelativeDB()

columns = [
    {"name": "name", "type": "str"},
    {"name": "city", "type": "str"},
    {"name": "sightings", "type": "int"},
    {"name": "latitude", "type": "float"},
    {"name": "longitude", "type": "float"},
]
db.create_table("ufo_sightings", columns)


db.insert("ufo_sightings", {"name": "John Doe", "city": "New York", "sightings": 2, "latitude": 40.7128, "longitude": -74.0060})
db.insert("ufo_sightings", {"name": "Jane Smith", "city": "Los Angeles", "sightings": 5, "latitude": 34.0522, "longitude": -118.2437})
db.insert("ufo_sightings", {"name": "Peter Jones", "city": "London", "sightings": 1, "latitude": 51.5074, "longitude": 0.1278})

db.create_index("ufo_sightings", "city")


all_records = db.select("ufo_sightings")
print("All Records:")
for record in all_records:
    print(record)

la_records = db.select("ufo_sightings", where_clause={"city": "Los Angeles"})
print("\nRecords from Los Angeles:")
for record in la_records:
    print(record)


# Corrected select_where usage:
table = db.tables["ufo_sightings"]
la_records_indexed = table.select_where("city", "Los Angeles")
print("\nRecords from Los Angeles (using index):")
for record in la_records_indexed:
    print(record)

db.update("ufo_sightings", 1, {"sightings": 10, "city": "San Francisco"})
db.delete("ufo_sightings", 0)


print("\nUpdated Table:")
db.tables["ufo_sightings"].print_table()


db.save_to_file("ufo_data.ufo")
db.save_to_file("ufo_data.json", format="json")
db.save_to_file("ufo_data.csv", format="csv")
db.save_to_file("ufo_data.sqlite", format="sqlite")


new_db = RelativeDB()
new_db.load_from_file("ufo_data.ufo")

json_db = RelativeDB()
json_db.load_from_file("ufo_data.json", format="json")

csv_db = RelativeDB()
csv_db.load_from_file("ufo_data.csv", format="csv")

print("\nLoaded from UFO file:")
new_db.tables["ufo_sightings"].print_table()



record_to_modify = new_db.select("ufo_sightings", where_clause={"city": "San Francisco"})[0]
print(f"Original name:{record_to_modify.get_field('name')}")
record_to_modify.set_field('name',"Alice")
print(f"Modified name:{record_to_modify.get_field('name')}")




# Clean up (optional - comment out if you want to keep the files)
# os.remove("ufo_data.ufo")
# os.remove("ufo_data.json")
# os.remove("ufo_data.csv")
# os.remove("ufo_data.sqlite")
```

## Контрибуции

Вклады приветствуются! Пожалуйста, создавайте запросы на включение (pull requests) или открывайте issues в репозитории GitHub.

#### Лицензия: 
[MIT License](https://github.com/SL1dee36/pyufo-db/blob/main/LICENSE)

## Благодарности

* [atxxxm](https://github.com/atxxxm) за оригинальный проект [UFO-DB](https://github.com/atxxxm/UFO-DB) на C++.
