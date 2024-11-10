# Developer: @sl1dee36, @atxxxm
# Current lib version: 1.7.3.0
# Date: 10.11.2024 18:37

from typing import Dict, List, Any, Optional
import os
import json
import csv
import sqlite3

class UFORecords:
    """
    Represents a single record in a UFO table.

    Attributes:
        fields (Dict[str, Any]): A dictionary containing the record's data.
                                 Keys are field names, values are field values.
    """

    def __init__(self, data: Dict[str, Any] = None):
        self.fields = data or {}

    def get_field(self, field_name: str) -> Any:
        """
        Retrieves the value of a specific field.

        Args:
            field_name: The name of the field to retrieve.

        Returns:
            The value of the field, or None if the field does not exist.
        """

        return self.fields.get(field_name)

    def set_field(self, field_name: str, value: Any) -> None:
        """
        Sets the value of a specific field.

        Args:
            field_name: The name of the field to set.
            value: The new value for the field.
        """

        self.fields[field_name] = value

    def __repr__(self) -> str:
        return str(self.fields)


class UFOTable:
    """
    Represents a table within the UFO database.

    Attributes:
        name (str): The name of the table.
        columns (List[Dict[str, str]]): A list of dictionaries defining the table's columns.
                                        Each dictionary should have "name" and "type" keys.
        records (List[UFORecords]): A list of UFORecords objects representing the table's data.
        next_id (int): The next available ID for a new record.
        indices (Dict[str, Dict[Any, List[int]]]): A dictionary of indices for faster lookups.
                                                   Keys are column names, values are dictionaries
                                                   mapping field values to lists of record IDs.
    """

    def __init__(self, table_name: str, columns: List[Dict[str, str]]):
        self.name = table_name
        self.columns = columns
        self.records = []
        self.next_id = 0
        self.indices = {}

    def insert_record(self, record_data: Dict[str, Any]) -> None:
        """
        Inserts a new record into the table.

        Args:
            record_data: A dictionary containing the data for the new record.
        """

        new_record = UFORecords(record_data)
        new_record.set_field("id", self.next_id)
        self._add_to_indices(new_record)
        self.records.append(new_record)
        self.next_id += 1

    def _add_to_indices(self, record: UFORecords):
        """
        Adds a record to the relevant indices.

        Args:
            record: The UFORecords object to add to the indices.
        """

        for column_name, index in self.indices.items():
            value = record.get_field(column_name)
            if value not in index:
                index[value] = []
            index[value].append(record.get_field('id'))

    def _remove_from_indices(self, record: UFORecords):
        """
        Removes a record from the relevant indices.

        Args:
            record: The UFORecords object to remove from the indices.
        """

        for column_name, index in self.indices.items():
            value = record.get_field(column_name)
            if value in index:
                index[value].remove(record.get_field('id'))

    def select_all(self) -> List[UFORecords]:
        """
        Selects all records from the table.

        Returns:
            A list of all UFORecords objects in the table.
        """

        return self.records

    def select_where(self, field_name: str, value: Any, use_index=True) -> List[UFORecords]:
        """
        Selects records that match a specific criteria.

        Args:
            field_name: The name of the field to filter on.
            value: The value to match.
            use_index: Whether to use an index for faster lookup (if available).

        Returns:
            A list of UFORecords objects that match the criteria.
        """

        if use_index and field_name in self.indices:
            record_ids = self.indices[field_name].get(value, [])
            return [record for record in self.records if record.get_field('id') in record_ids]
        return [record for record in self.records if record.get_field(field_name) == value]

    def update_record(self, record_id: int, updates: Dict[str, Any]) -> None:
        """
        Updates a specific record.

        Args:
            record_id: The ID of the record to update.
            updates: A dictionary containing the updated field values.

        Raises:
            ValueError: If no record with the given ID is found.
        """

        try:
            record_index = next((i for i, record in enumerate(self.records) if record.get_field("id") == record_id))
            self._remove_from_indices(self.records[record_index])
            for field, value in updates.items():
                self.records[record_index].set_field(field, value)
            self._add_to_indices(self.records[record_index])
        except StopIteration:
            raise ValueError(f"Record with id {record_id} not found.")

    def delete_record(self, record_id: int) -> bool:
        """
        Deletes a specific record.

        Args:
            record_id: The ID of the record to delete.

        Returns:
            True if the record was deleted, False otherwise.
        """

        try:
            record_index = next((i for i, record in enumerate(self.records) if record.get_field("id") == record_id))
            self._remove_from_indices(self.records[record_index])
            del self.records[record_index]
            return True
        except StopIteration:
            return False

    def create_index(self, column_name: str):
        """
        Creates an index on a specific column for faster lookups.

        Args:
            column_name: The name of the column to index.
        """

        if column_name in self.indices:
            return

        self.indices[column_name] = {}
        for record in self.records:
            value = record.get_field(column_name)
            if value is not None:
                if value not in self.indices[column_name]:
                    self.indices[column_name][value] = []
                self.indices[column_name][value].append(record.get_field('id'))

    def _print_header(self) -> None:
        """Prints the table header."""

        print("|" + "|".join(f" {col['name']:<10} " for col in self.columns) + "|")
        print("-" * (13 * (len(self.columns) + 1) - 1))

    def _print_record(self, record: UFORecords) -> None:
        """Prints a single record."""

        print("|" + "|".join(f" {str(record.get_field(col['name'])):<10} " for col in self.columns) + "|")

    def print_table(self):
        """Prints the entire table in a formatted way."""

        self._print_header()
        for record in self.records:
            self._print_record(record)


class RelativeDB:
    """
    A simple in-memory relational database.

    Supports basic CRUD operations and saving/loading to various file formats.

    Available Commands (through method calls):
        create_table(table_name, columns): Creates a new table.
        insert(table_name, record_data): Inserts a new record into a table.
        select(table_name, where_clause): Selects records from a table (optionally with a where clause).
        update(table_name, record_id, updates): Updates a specific record in a table.
        delete(table_name, record_id): Deletes a specific record from a table.
        create_index(table_name, column_name): Creates an index on a column for faster lookups.
        save_to_file(filename, format): Saves the database to a file in a specific format.
        load_from_file(filename, format): Loads the database from a file in a specific format.


    Supported Formats:
        ufo: Custom UFO format.
        json: JSON format.
        csv: CSV format.
        sqlite: SQLite database format.


    Attributes:
        tables (Dict[str, UFOTable]): A dictionary of tables in the database.
                                     Keys are table names, values are UFOTable objects.
    """

    def __init__(self):
        self.tables = {}

    def create_table(self, table_name: str, columns: List[Dict[str, str]]) -> None:
        if table_name in self.tables:
            raise ValueError(f"Table with name '{table_name}' already exists.")
        for col in columns:
            if 'type' not in col or col['type'] not in ['int', 'float', 'str']:
                raise TypeError(f"Invalid type specified for column {col.get('name', 'unnamed')}")
        self.tables[table_name] = UFOTable(table_name, columns)

    def insert(self, table_name: str, record_data: Dict[str, Any]) -> None:
        table = self._get_table(table_name)
        for col in table.columns:
            value = record_data.get(col['name'])
            expected_type = col['type']
            if value is not None and not isinstance(value, eval(expected_type)):
                raise TypeError(f"Invalid data type for column '{col['name']}'. Expected {expected_type}, got {type(value).__name__}.")
        table.insert_record(record_data)

    def select(self, table_name: str, where_clause: Optional[Dict[str, Any]] = None) -> List[UFORecords]:
        table = self._get_table(table_name)
        if where_clause:
            result = table.records[:]
            for field, value in where_clause.items():
                result = [record for record in result if record.get_field(field) == value]
            return result
        return table.select_all()

    def update(self, table_name: str, record_id: int, updates: Dict[str, Any]) -> None:
        table = self._get_table(table_name)
        table.update_record(record_id, updates)

    def delete(self, table_name: str, record_id: int) -> bool:
        table = self._get_table(table_name)
        return table.delete_record(record_id)

    def create_index(self, table_name: str, column_name: str):
        table = self._get_table(table_name)
        table.create_index(column_name)

    def _get_table(self, table_name: str) -> UFOTable:
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' does not exist.")
        return self.tables[table_name]

    def save_to_file(self, filename: str, format: str = "ufo") -> bool:
        if format == "ufo":
            return self._save_ufo(filename)
        if format == "json":
            return self._save_json(filename)
        elif format == "csv":
            return self._save_csv(filename)
        elif format == "sqlite":
            return self._save_sqlite(filename)
        raise ValueError(f"Unsupported format: {format}")


    def _save_ufo(self, filename: str) -> bool:
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(str(len(self.tables)) + "\n")
                for table_name, table in self.tables.items():
                    f.write(table_name + "\n")
                    f.write(str(len(table.columns)) + "\n")
                    for col in table.columns:
                        f.write(f"{col['name']}:{col['type']}\n")

                    f.write(str(table.next_id) + "\n")
                    f.write(str(len(table.records)) + "\n")
                    for record in table.records:
                        record_data = [str(record.get_field(col['name'])) for col in table.columns]
                        f.write("|".join(record_data) + "|" + str(record.get_field("id")) + "\n")
            return True
        except (IOError, OSError) as e:
            print(f"Error saving to UFO file: {e}")
            return False

    def _save_json(self, filename: str) -> bool:
        try:
            data = {
                table_name: {
                    "columns": table.columns,
                    "records": [record.fields for record in table.records]
                }
                for table_name, table in self.tables.items()
            }
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            return True
        except (IOError, OSError, json.JSONDecodeError) as e:
            print(f"Error saving to JSON: {e}")
            return False

    def _save_csv(self, filename: str) -> bool:
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                for table_name, table in self.tables.items():
                    writer = csv.DictWriter(csvfile, fieldnames=[col['name'] for col in table.columns] + ['id'])
                    writer.writeheader()
                    for record in table.records:
                        writer.writerow(record.fields)
            return True
        except (IOError, OSError, csv.Error) as e:
            print(f"Error saving to CSV: {e}")
            return False

    def _save_sqlite(self, filename: str) -> bool:  # Slightly modified
        try:
            conn = sqlite3.connect(filename)
            cursor = conn.cursor()
            for table_name, table in self.tables.items():
                column_definitions = ", ".join([f"{col['name']} {col['type']}" for col in table.columns])
                cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, {column_definitions});")  # Modified
                for record in table.records:
                    column_names = ", ".join([col['name'] for col in table.columns])
                    placeholders = ", ".join(["?"] * len(table.columns))
                    values = [record.get_field(col['name']) for col in table.columns]

                    # Include the id in the insert statement
                    cursor.execute(f"INSERT INTO {table_name} (id, {column_names}) VALUES ({record.get_field('id')}, {placeholders});", values)

            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error saving to SQLite: {e}")
            return False

    def load_from_file(self, filename: str, format: str = "ufo") -> bool:
        if not os.path.exists(filename):
            print(f"Error: File '{filename}' not found.")
            return False

        if format == "ufo":
            return self._load_ufo(filename)
        if format == "json":
            return self._load_json(filename)
        elif format == "csv":
            return self._load_csv(filename)
        elif format == "sqlite":
            return self._load_sqlite(filename)
        raise ValueError(f"Unsupported format: {format}")

    def _load_ufo(self, filename: str) -> bool:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                num_tables = int(f.readline().strip())
                for _ in range(num_tables):
                    table_name = f.readline().strip()
                    num_columns = int(f.readline().strip())
                    columns = []
                    for _ in range(num_columns):
                        col_name, col_type = f.readline().strip().split(":", 1)
                        columns.append({"name": col_name, "type": col_type})

                    table = UFOTable(table_name, columns)
                    table.next_id = int(f.readline().strip())
                    num_records = int(f.readline().strip())

                    for _ in range(num_records):
                        line = f.readline().strip()
                        record_data_str = line.split("|")
                        record_data = {col['name']: self._convert_type(record_data_str[i], col['type']) for i, col in enumerate(columns)}
                        record_id = int(record_data_str[-1])
                        record_data['id'] = record_id
                        record = UFORecords(record_data)
                        table.records.append(record)
                    self.tables[table_name] = table
            return True
        except (IOError, OSError, ValueError, IndexError) as e:
            print(f"Error loading from UFO file: {e}")
            return False



    def _load_json(self, filename: str) -> bool:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for table_name, table_data in data.items():
                    columns = table_data['columns']
                    table = UFOTable(table_name, columns)
                    for record_data in table_data['records']:
                        record = UFORecords(record_data)
                        if 'id' in record_data:
                            table.next_id = max(table.next_id, record_data['id'] + 1)
                        table.records.append(record)
                    self.tables[table_name] = table
            return True
        except (IOError, OSError, json.JSONDecodeError, TypeError) as e:
            print(f"Error loading from JSON: {e}")
            return False

    def _load_csv(self, filename: str) -> bool:
        try:
            with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    table_name = row.get('table_name', 'default')
                    if table_name not in self.tables:
                        columns = [{'name': field, 'type': 'str'} for field in reader.fieldnames if field != 'table_name']
                        self.tables[table_name] = UFOTable(table_name, columns)
                    table = self.tables[table_name]
                    record_data = {k: v for k, v in row.items() if k != 'table_name'}
                    for col in table.columns:
                        if col['type'] == 'int':
                            try:
                                record_data[col['name']] = int(record_data[col['name']])
                            except ValueError:
                                pass
                        elif col['type'] == 'float':
                            try:
                                record_data[col['name']] = float(record_data[col['name']])
                            except ValueError:
                                pass
                    table.insert_record(record_data)
            return True
        except (IOError, OSError, csv.Error) as e:
            print(f"Error loading from CSV: {e}")
            return False

    def _load_sqlite(self, filename: str) -> bool:

        pass

        # try:
        #     conn = sqlite3.connect(filename)
        #     cursor = conn.cursor()
        #     cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        #     tables = cursor.fetchall()
        #     for table_name_tuple in tables:
        #         table_name = table_name_tuple[0]
        #         if isinstance(table_name, int):  # Handle integer table names
        #             table_name = str(table_name)

        #         # Get column information (excluding 'id')
        #         cursor.execute(f"PRAGMA table_info({table_name});")
        #         columns = []
        #         column_names = []
        #         for column in cursor.fetchall():
        #             name, type, *_ = column
        #             if name != 'id':
        #                 columns.append({'name': name, 'type': type})
        #                 column_names.append(name)

        #         table = UFOTable(table_name, columns)

        #         select_columns = ", ".join(column_names)
        #         cursor.execute(f"SELECT id, {select_columns} FROM {table_name};")

        #         records = cursor.fetchall()

        #         # Optimization and fix for empty tables: get max id outside the loop
        #         max_id = 0
        #         for record_tuple in records:
        #             record_id, *values = record_tuple
        #             record_data = dict(zip(column_names, values))
        #             record = UFORecords(record_data)
        #             record.set_field('id', record_id)
        #             table.records.append(record)
        #             max_id = max(max_id, record_id) # Update max_id in loop



        #         table.next_id = max_id + 1 if records else 1  # Fix for empty tables and optimization
        #         self.tables[table_name] = table

        #     conn.close()
        #     return True
        # except sqlite3.Error as e:
        #     print(f"Error loading from SQLite: {e}")
        #     return False

    def _convert_type(self, value: str, type_str: str) -> Any:
        if type_str == 'int':
            return int(value)
        elif type_str == 'float':
            return float(value)
        return value