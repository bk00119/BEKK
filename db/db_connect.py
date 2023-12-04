import os
import random
import pymongo as pm
from bson.objectid import ObjectId

LOCAL = "0"
CLOUD = "1"

DB = "BEKK"

client = None

MONGO_ID = '_id'

ID_LEN = 24
BIG_NUM = 100_000_000_000_000_000_000


def connect_db():
    """
    This provides a uniform way to connect to the DB across all uses.
    Returns a mongo client object... maybe we shouldn't?
    Also set global client variable.
    We should probably either return a client OR set a
    client global.
    """
    global client
    if client is None:  # not connected yet!
        print("Setting client because it is None.")
        if os.environ.get("CLOUD_MONGO", LOCAL) == CLOUD:
            username = os.environ.get("CLOUD_MONGO_USER")
            password = os.environ.get("CLOUD_MONGO_PW")
            db_url = os.environ.get("CLOUD_MONGO_URL")
            if not password:
                raise ValueError('You must set your password '
                                 + 'to use Mongo in the cloud.')
            print("Connecting to Mongo in the cloud.")
            client = pm.MongoClient(f'mongodb+srv://{username}:{password}'
                                    + f'@{db_url}')
            # PA recommends these settings:
            # + 'connectTimeoutMS=30000&'
            # + 'socketTimeoutMS=None
            # + '&connect=false'
            # + 'maxPoolsize=1')
            # but they don't seem necessary
        else:
            print("Connecting to Mongo locally.")
            client = pm.MongoClient()


def gen_object_id():
    _id = random.randint(0, BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(ID_LEN, '0')
    return ObjectId(_id)


def fetch_one(collection, filt, db=DB):
    """
    fetch the first doc with filter in the collection
    """
    for doc in client[db][collection].find(filt):
        if MONGO_ID in doc:
            # Convert mongo ID to a string so it works as JSON
            doc[MONGO_ID] = str(doc[MONGO_ID])
        return doc


def fetch_all_as_dict(db_name, collection):
    """
    fetching all data of a collection as dict type
    """
    db = client[db_name]
    tasks = db[collection]
    data = {}
    print(db, tasks)
    for task in tasks.find():
        # _id: ObjectID; ObjectId is not JSON serializable
        key = str(task['_id'])
        del task['_id']
        data[key] = task
    return data


def insert_one(collection, doc, db=DB):
    """
    inserting one document to the collection
    """
    res = client[db][collection].insert_one(doc)
    # return res
    return str(res.inserted_id)


def del_one(collection, filt, db=DB):
    """
    deleting one document of the collection
    """
    client[db][collection].delete_one(filt)
