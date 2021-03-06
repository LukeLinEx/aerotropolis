from pymongo import MongoClient
from os.path import expanduser

path = expanduser("~/.credentials/aerotropolis.txt")
mongo_connect = open(path, 'r')
ip, port, user, pwd = map(lambda x: x.strip(), mongo_connect.readlines())
client = MongoClient(ip, int(port))


def insert_document2mongo(documents, source):
    """

    :source: str, the name of the desired collection in db
    """
    db = client["aerotropolis"]         
    db.authenticate(user, pwd)
    collection = eval("db." + source)

    if len(documents)==0:
        print("No mew piece today")
    else:
        collection.insert_many(documents)

if __name__ == "__main__":
    insert_document2mongo([], "udn")
