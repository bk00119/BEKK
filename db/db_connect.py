import os

import pymongo as pm

LOCAL = "0"
CLOUD = "1"

DB = "BEKK"

client = None

MONGO_ID = '_id'


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


def fetch_all_as_dict(db_name, collection):
    db = client[db_name]
    tasks = db[collection]
    data = {}
    for task in tasks.find():
        # _id: ObjectID; ObjectId is not JSON serializable
        key = str(task['_id'])
        del task['_id']
        data[key] = task
    return data
