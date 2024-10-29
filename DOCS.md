# Документация по базе данных pyUFO-db

Оригинальная c++ версия проекта: [UFO-DB](https://github.com/atxxxm/UFO-DB)

Эта документация описывает структуру и использование базы данных pyUFO-db, реализованной на Python. База данных позволяет хранить и управлять записями о наблюдениях pyUFO-db, организованными в таблицы.

## Классы

### `UFORecords`

Этот класс представляет собой отдельную запись о pyUFO-db.

**Атрибуты:**

* `fields`: Словарь, хранящий данные записи. Ключи словаря - названия полей, значения - значения полей.

**Методы:**

* `get_field(self, field_name: str) -> str`: Возвращает значение поля с заданным именем. Если поле не существует, возвращает пустую строку.
* `add(self, field_name: str, value: str) -> None`: Добавляет или обновляет поле с заданным именем и значением.
* `__repr__(self) -> str`: Возвращает строковое представление записи (словарь `fields`).


### `UFOTable`

Этот класс представляет таблицу записей о pyUFO-db.

**Атрибуты:**

* `name`: Название таблицы.
* `columns`: Список названий столбцов таблицы.
* `records`: Список записей (`UFORecords`) в таблице.
* `next_id`: Следующий доступный идентификатор записи.

**Методы:**

* `insert_record(self, record_data: Dict[str, str]) -> None`: Вставляет новую запись в таблицу.  `record_data` - словарь, где ключи - названия столбцов, а значения - значения для новой записи. Автоматически добавляет уникальный `id` к записи.
* `select_all(self) -> None`: Выводит все записи таблицы в консоль в формате таблицы.
* `select_where(self, field_name: str, value: str) -> List[UFORecords]`: Возвращает список записей, удовлетворяющих условию `field_name == value`.
* `update_record(self, record_id: int, updates: Dict[str, str]) -> None`: Обновляет запись с заданным `record_id`. `updates` - словарь, где ключи - названия полей для обновления, а значения - новые значения.  Вызывает `RuntimeError`, если запись с данным `id` не найдена.
* `delete_record(self, record_id: int) -> bool`: Удаляет запись с заданным `record_id`. Возвращает `True`, если запись была удалена, и `False` в противном случае.
* `_print_header(self) -> None`:  (Внутренний метод) Выводит заголовок таблицы в консоль.
* `_print_record(self, record: UFORecords) -> None`: (Внутренний метод) Выводит одну запись в консоль в формате строки таблицы.

### `Relative_DB`

Этот класс представляет собой базу данных, содержащую таблицы `UFOTable`.

**Атрибуты:**

* `tables`: Словарь, где ключи - названия таблиц, а значения - объекты `UFOTable`.

**Методы:**

* `create_table(self, name: str, columns: List[str]) -> None`: Создает новую таблицу с заданным именем и столбцами.  Вызывает `RuntimeError`, если таблица с таким именем уже существует.
* `insert(self, table_name: str, record_data: Dict[str, str]) -> None`: Вставляет новую запись в указанную таблицу. Вызывает `RuntimeError`, если таблицы с таким именем не существует.
* `select(self, table_name: str) -> None`: Выводит все записи указанной таблицы в консоль. Вызывает `RuntimeError`, если таблицы с таким именем не существует.
* `update(self, table_name: str, record_id: int, updates: Dict[str, str]) -> None`: Обновляет запись в указанной таблице. Вызывает `RuntimeError`, если таблицы с таким именем не существует.
* `delete_record(self, table_name: str, record_id: int) -> bool`: Удаляет запись из указанной таблицы. Возвращает `True`, если запись была удалена, и `False`, если таблица или запись не найдены.
* `save_to_file(self, filename: str) -> bool`: Сохраняет базу данных в файл.  Возвращает `True` при успешном сохранении, `False` при ошибке.
* `load_from_file(self, filename: str) -> bool`: Загружает базу данных из файла.  Возвращает `True` при успешной загрузке, `False` при ошибке.


## Пример использования

```python
db = Relative_DB()
db.create_table("sightings", ["date", "location", "description"])
db.insert("sightings", {"date": "2024-01-01", "location": "Moscow", "description": "Bright light"})
db.insert("sightings", {"date": "2024-01-05", "location": "London", "description": "Disc-shaped object"})
db.select("sightings")
db.update("sightings", 1, {"location": "St. Petersburg"})
db.select("sightings")
db.delete_record("sightings", 2)
db.select("sightings")
db.save_to_file("ufo_data.txt")

db2 = Relative_DB()
db2.load_from_file("ufo_data.txt")
db2.select("sightings")

```


## Обработка ошибок

База данных обрабатывает следующие ошибки:

* Дублирование имен таблиц при создании.
* Попытка доступа к несуществующей таблице.
* Попытка обновления или удаления несуществующей записи.
* Ошибки при сохранении и загрузке из файла (IOError, OSError, ValueError, IndexError).


## Кодировка

База данных использует кодировку UTF-8 для сохранения и загрузки данных из файла.
