from pymongo import MongoClient
import pymongo
def get_database():
    CONNECTION_STRING = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false"
    client = MongoClient(CONNECTION_STRING)

    dbname = client['LocalDatas']
    collectionName = dbname["searchEngine"]

    return collectionName.find_one({"docId":1})

if __name__ == "__main__":
    dbname = get_database()
    print(dbname)  