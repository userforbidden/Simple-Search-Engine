'''
Author: Saranyan Senthivel
Date Created: 13-Oct-2021
'''
from index import index
from timed import timing
from pymongo import MongoClient
import argparse
import re
import ast

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
    def _results(self,token):
        return self.index.get(token,set()) 
    
    def _list_results(self,tokens):
        return [self.index.get(token,set()) for token in tokens] 

    @timing
    def search(self,query_Tokens,searchType):
        
        if searchType == 'simple':
            results = self._results(query_Tokens)
            documents = results
        if searchType == '&':
            results = self._list_results(query_Tokens)
            documents = [docId for docId in set.intersection(*results)]
        if searchType =='|':
            results = self._list_results(query_Tokens)
            documents = [docId for docId in set.union(*results)]

        return documents
'''
This function Get the documents from the database 
'''
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
    def intersection(lst1, lst2):
        lst3 = [value for value in lst1 if value in lst2]
        return lst3

    def dfs(left,right,op):
        queryResults = []

        if type(left) is ast.Name and type(right) is ast.Name:
            if op == '&':
                queryResults = queryResults + query.search([left.id,right.id],'&')
            elif op == '|':
                queryResults = queryResults + query.search([left.id,right.id],'|')
        elif type(left) is ast.BinOp and type(right) is ast.Name:
            if op == '&':
                queryResults = queryResults + intersection([query.search(right.id,'simple')] ,[dfs(left.left,left.right,left.op)])
            elif op == '|':
                queryResults = queryResults + [query.search(right.id,'simple')] + [dfs(left.left,left.right,left.op)]
        elif type(left) is ast.Name and type(right) is ast.BinOp:
            if op == '&':
                queryResults = queryResults + intersection([query.search(right.id,'simple')] ,[dfs(left.left,left.right,left.op)])
            elif op == '|':
                queryResults = queryResults + [query.search(left.id,'simple')] + [dfs(right.left,right.right,right.op)]

        return queryResults
        

    query = gather_documents(load_documents(),Query())

    # Get the command line arguments
    parser = argparse.ArgumentParser(description='query search Engine.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--simple', type=str,help="enter simple token to be searched")
    group.add_argument('--complex', type=str,help="Enter the complex search query")
    # parser.add_argument('expression',type=str,help="token to be searched",)
    args = parser.parse_args()
    if args.simple is not None:
        expression = args.simple
        queryResults = query.search(expression,'simple')
        
    elif args.complex is not None:
        expression = args.complex
        try:
            t = ast.parse(expression)
            for body in t.body:
                if (type(body) is ast.Expr):
                    exprValue = body.value
                    # print(exprValue)
                    print(type(exprValue))
                    if type(exprValue) is ast.Name:
                        queryResults = query.search(exprValue.id,'simple')
                    elif type(exprValue) is ast.BinOp:
                        left = exprValue.left
                        right = exprValue.right
                        op = exprValue.op
                        if type(op) is ast.BitAnd:
                            queryResults = dfs(left,right,'&')
                        elif type(op) is ast.BitOr:
                            queryResults = dfs(left,right,'|')
                        print(left, right, op)
            # match = re.search(r'\((.*?)\)',expression)
            # insideBracket = match.group(1)
            # span = match.span()
            # print(insideBracket,span)
        except AttributeError as e:
            andCondition = expression.find('&')
            orCondition = expression.find('|')
            # print(andCondition,orCondition)
            if andCondition != -1:
                queryTokens = [expression[:andCondition].strip(),expression[andCondition+1:].strip()]
                queryResults = query.search(queryTokens,'&')
            elif orCondition != -1:
                print("I'm here")
                queryTokens = [expression[:orCondition].strip(),expression[orCondition+1:].strip()]
                queryResults = query.search(queryTokens,'|')
            else: 
                print("query error invalid search query")
    try:
        print("query results {}".format(' '.join(map(str,queryResults))))
    except UnboundLocalError as e:
        print("query error use simple search token with --simple parsing argument")
if __name__ == "__main__":
    main()