# Документация:

RelativeDB - это простая реляционная база данных, работающая в оперативной памяти. Она поддерживает базовые CRUD операции (создание, чтение, обновление, удаление), а также сохранение и загрузку данных в различных форматах.

## Классы

### `UFORecords`

Представляет собой отдельную запись в таблице НЛО.

**Атрибуты:**

* `fields (Dict[str, Any])`: Словарь, содержащий данные записи. Ключи - имена полей, значения - значения полей.

**Методы:**

* `get_field(field_name: str) -> Any`: Возвращает значение указанного поля. Если поле не существует, возвращает `None`.
* `set_field(field_name: str, value: Any) -> None`: Устанавливает значение указанного поля.
* `__repr__(self) -> str`: Возвращает строковое представление записи (словарь полей).


### `UFOTable`

Представляет собой таблицу в базе данных НЛО.

**Атрибуты:**

* `name (str)`: Имя таблицы.
* `columns (List[Dict[str, str]])`: Список словарей, определяющих столбцы таблицы. Каждый словарь должен содержать ключи "name" (имя столбца) и "type" (тип данных столбца - 'int', 'float' или 'str').
* `records (List[UFORecords])`: Список объектов `UFORecords`, представляющих данные таблицы.
* `next_id (int)`: Следующий доступный ID для новой записи.
* `indices (Dict[str, Dict[Any, List[int]]])`: Словарь индексов для ускорения поиска. Ключи - имена столбцов, значения - словари, сопоставляющие значения полей со списками ID записей.

**Методы:**

* `insert_record(record_data: Dict[str, Any]) -> None`: Вставляет новую запись в таблицу. Автоматически присваивает ID записи.
* `_add_to_indices(record: UFORecords)`:  Добавляет запись в соответствующие индексы. (Внутренний метод)
* `_remove_from_indices(record: UFORecords)`: Удаляет запись из соответствующих индексов. (Внутренний метод)
* `select_all() -> List[UFORecords]`: Выбирает все записи из таблицы.
* `select_where(field_name: str, value: Any, use_index=True) -> List[UFORecords]`: Выбирает записи, соответствующие заданному критерию.  `use_index` указывает, использовать ли индекс для ускорения поиска.
* `update_record(record_id: int, updates: Dict[str, Any]) -> None`: Обновляет указанную запись. Генерирует `ValueError`, если запись с заданным ID не найдена.
* `delete_record(record_id: int) -> bool`: Удаляет указанную запись. Возвращает `True`, если запись была удалена, `False` в противном случае.
* `create_index(column_name: str)`: Создает индекс для указанного столбца.
* `_print_header() -> None`:  Выводит заголовок таблицы. (Внутренний метод)
* `_print_record(record: UFORecords) -> None`: Выводит одну запись. (Внутренний метод)
* `print_table()`: Выводит всю таблицу в форматированном виде.


### `RelativeDB`

Основной класс базы данных.

**Атрибуты:**

* `tables (Dict[str, UFOTable])`: Словарь таблиц в базе данных. Ключи - имена таблиц, значения - объекты `UFOTable`.

**Методы:**

* `create_table(table_name: str, columns: List[Dict[str, str]]) -> None`: Создает новую таблицу. Генерирует `ValueError`, если таблица с таким именем уже существует.  Проверяет типы данных столбцов.
* `insert(table_name: str, record_data: Dict[str, Any]) -> None`: Вставляет новую запись в таблицу. Проверяет соответствие типов данных.
* `select(table_name: str, where_clause: Optional[Dict[str, Any]] = None) -> List[UFORecords]`: Выбирает записи из таблицы. Опционально принимает условие `where_clause` для фильтрации.
* `update(table_name: str, record_id: int, updates: Dict[str, Any]) -> None`: Обновляет указанную запись в таблице.
* `delete(table_name: str, record_id: int) -> bool`: Удаляет указанную запись из таблицы.
* `create_index(table_name: str, column_name: str)`: Создает индекс для указанного столбца в указанной таблице.
* `_get_table(table_name: str) -> UFOTable`: Возвращает объект таблицы по имени. Генерирует `ValueError`, если таблица не существует. (Внутренний метод)
* `save_to_file(filename: str, format: str = "ufo") -> bool`: Сохраняет базу данных в файл в указанном формате. Поддерживаемые форматы: "ufo", "json", "csv", "sqlite".
* `_save_ufo(filename: str) -> bool`: Сохраняет в формате UFO.  (Внутренний метод)
* `_save_json(filename: str) -> bool`: Сохраняет в формате JSON. (Внутренний метод)
* `_save_csv(filename: str) -> bool`: Сохраняет в формате CSV. (Внутренний метод)
* `_save_sqlite(filename: str) -> bool`: Сохраняет в формате SQLite. (Внутренний метод)
* `load_from_file(filename: str, format: str = "ufo") -> bool`: Загружает базу данных из файла в указанном формате.
* `_load_ufo(filename: str) -> bool`: Загружает из формата UFO. (Внутренний метод)
* `_load_json(filename: str) -> bool`: Загружает из формата JSON. (Внутренний метод)
* `_load_csv(filename: str) -> bool`: Загружает из формата CSV. (Внутренний метод)
* `_load_sqlite(filename: str) -> bool`: Загружает из формата SQLite. (Внутренний метод - **не реализован**)
* `_convert_type(value: str, type_str: str) -> Any`: Преобразует строковое значение к указанному типу данных ('int', 'float', 'str'). (Внутренний метод)


## Поддерживаемые форматы

* **ufo:** Наш формат UFO.     
* **json:** Формат JSON.                 
* **csv:** Формат CSV.                   
* **sqlite:** Формат базы данных SQLite. 23%


## Пример использования

```python
from py_ufo_db import RelativeDB

db = RelativeDB()

# Создание таблицы
db.create_table("users", [{"name": "name", "type": "str"}, {"name": "age", "type": "int"}])

# Вставка записей
db.insert("users", {"name": "John Doe", "age": 30})
db.insert("users", {"name": "Jane Doe", "age": 25})

# Выборка записей
users = db.select("users")
for user in users:
    print(user)

# Выборка с условием
young_users = db.select("users", where_clause={"age": 25})
for user in young_users:
    print(user)

# Обновление записи
db.update("users", 0, {"age": 31})

# Удаление записи
db.delete("users", 1)

# Сохранение в файл
db.save_to_file("users.json", format="json")

# Загрузка из файла
db.load_from_file("users.json", format="json")
```
