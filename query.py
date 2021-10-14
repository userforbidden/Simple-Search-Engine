'''
Author: Saranyan Senthivel
Date Created: 13-Oct-2021
'''
from index import index
from timed import timing
from pymongo import MongoClient
import argparse

class Query:
    def __init__(self) -> None:
        self.index = {}
        self.documents = {}

    def index_document(self,document):
        docId = document['docId']
        if docId not in self.documents:
            self.documents[docId] = document
        
        tokens = document['tokens']
        for token in tokens:
            if token not in self.index:
                self.index[token] = set()
            self.index[token].add(docId)
        # return 
    def _results(self,expression):
        return [self.index.get(expression,set())]
    @timing
    def search(self,expression):
        results = self._results(expression)
        # print (*results)

        return [docId for docId in set(*results)]
@timing    
def load_documents():
    CONNECTION_STRING = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false"
    client = MongoClient(CONNECTION_STRING)

    dbname = client['LocalDatas']
    collectionName = dbname["searchEngine"]

    return collectionName.find()

@timing
def gather_documents(documents, query):
    for i, document in enumerate(documents):
        query.index_document(document)
    
    return query

def main():
    query = gather_documents(load_documents(),Query())

    parser = argparse.ArgumentParser(description='query search Engine.')

    parser.add_argument('expression',type=str,help="token to be searched",)
    args = parser.parse_args()

    try: 
        expression = args.expression
    except Exception as e:
        print(e)


    # query = Query()
    print(query.search(expression))

if __name__ == "__main__":
    main()