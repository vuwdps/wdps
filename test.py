import trident
import json

print("Loading db...")
db = trident.Db(
    "E:\WDPS\assignment-no-elasticsearch-splitted2\assignment-no-elasticsearch-splitted")
print("Done")

while True:
    query = input("Query: ")
    res = db.sparql(query)
    print(json.dumps(json.loads(res), indent=2))
    print()
m
