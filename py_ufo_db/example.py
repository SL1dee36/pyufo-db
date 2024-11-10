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