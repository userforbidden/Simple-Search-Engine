'''
Author: Saranyan Senthivel
Date Created: 11-Oct-2021
'''
from typing import List
import argparse

class index:
    def __init__(self,docId,tokens) -> None:
        self.docId = docId;
        self.tokens = tokens
    def printValues(self):
        print("index {} {}".format(self.docId," ".join(map(str,self.tokens))))

def main():
    parser = argparse.ArgumentParser(description='Add index for search Engine.')

    parser.add_argument('DocumentID',type=int,help="Document Id of index for the tokens")
    parser.add_argument('Tokens',metavar='T',type=str, nargs='+',help="<Required> Set flag")
    args = parser.parse_args()

    try: 
        documentId = args.DocumentID
    except Exception as e:
        print(e)

    try:
        tokens = args.Tokens
    except Exception as e:
        print(e)

    index(documentId,tokens).printValues()

if __name__ == "__main__":
    main()