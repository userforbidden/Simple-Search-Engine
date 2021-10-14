'''
Author: Saranyan Senthivel
Date Created: 11-Oct-2021
'''
from typing import List
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import argparse

class index:
    '''
    Initializing the data
    docId and tokens
    '''
    def __init__(self,docId,tokens) -> None:
        self.docId = docId;
        self.tokens = tokens
    '''
    function to insert the index data into MongoDb
    '''
    def insertIndextoDatabase(self):
        CONNECTION_STRING = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false"
        client = MongoClient(CONNECTION_STRING)
        dbname = client['LocalDatas']
        # document data to insert 
        document = {
            "docId":self.docId,
            "tokens":self.tokens
            }
        
        # Exception handling to handle duplicate data being inserted 
        # if a docId already exists the existing token will be completely replaced.
        # mongoDb collection has an unique index on docId so it will throw an exception 

        try:
            collectionName = dbname["searchEngine"]
            post_id = collectionName.insert_one(document).inserted_id
            print(post_id)
        except DuplicateKeyError as dupError:
            post_id = collectionName.update({"docId":self.docId},{"$set":{"tokens":self.tokens}},upsert=False)
            '''
            print("index is duplicate so updating the tokens for docId: {}".format(self.docId))
            '''
        print("index ok {}".format(self.docId))
    '''
    Simple function to print the input calues docid and tokens
    '''
    def printValues(self):
        print("index {} {}".format(self.docId," ".join(map(str,self.tokens))))

def main():
    parser = argparse.ArgumentParser(description='Add index for search Engine.')

    parser.add_argument('docId',type=int,help="Document Id of index for the tokens",)
    parser.add_argument('Tokens',metavar='T',type=str, nargs='+',help="<Required> Set flag")
    args = parser.parse_args()

    try: 
        documentId = args.docId
    except Exception as e:
        print(e)

    try:
        tokens = args.Tokens
    except Exception as e:
        print(e)

    index(documentId,tokens).insertIndextoDatabase()

if __name__ == "__main__":
    main()