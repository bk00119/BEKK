import db.db_connect as dbc
import db.users as usrs
from bson import ObjectId
from datetime import datetime

MOCK_ID = 0
POSTS_COLLECT = "posts"
USER_ID = "user_id"
CONTENT = "content"
TASK_IDS = "task_ids"
GOAL_IDS = "goal_ids"
LIKE_IDS = "like_ids"
COMMENT_IDS = "comment_ids"
ID = "_id"
TIMESTAMP = 'timestamp'


def get_test_post():
    return {
        USER_ID: "660e288ea90f1c7ff1ceb612",
        CONTENT: "test post",
        TASK_IDS: [],
        GOAL_IDS: [],
        LIKE_IDS: [],
        COMMENT_IDS: []
    }


def add_post(user_id,
             content,
             task_ids,
             goal_ids,
             like_ids,
             comment_ids):
    dbc.connect_db()
    _id = dbc.insert_one(
                        POSTS_COLLECT,
                        {
                            USER_ID: user_id,
                            CONTENT: content,
                            TASK_IDS: task_ids,
                            GOAL_IDS: goal_ids,
                            LIKE_IDS: like_ids,
                            COMMENT_IDS: comment_ids,
                            TIMESTAMP: str(datetime.now())
                        })
    return _id


def fetch_all():
    """
    fetch all posts
    """
    dbc.connect_db()
    posts = dbc.fetch_data_from_two_collections(dbc.DB, POSTS_COLLECT, [
        {
            "$lookup": {
                "from": "users",
                "let": {
                    "user_id": {
                      # CONVERT USER_ID(STRING) TO OBJECTID
                      "$toObjectId": "$user_id"
                    }
                },
                "pipeline": [{
                    "$match": {
                        "$expr": {
                            "$eq": [
                                "$_id",
                                "$$user_id"
                            ]
                        }
                    }
                }],
                "as": "user"
            }
        },
        {
            "$unwind": "$user"
        },
        {
            "$project": {
                "_id": {
                    '$toString': "$_id"
                },
                "username": "$user.username",
                "user_id": 1,
                'content': 1,
                'task_ids': 1,
                'goal_ids': 1,
                'like_ids': 1,
                'comment_ids': 1
            }
        },
        # {
        #   "$sort": {
        #       "user": 1,
        #       "name": 1
        #   }
        # }
    ])
    return posts


def fetch_by_user_id(user_id: str):
    """
    fetch all posts thats linked to that user_id
    """
    dbc.connect_db()
    if usrs.id_exists(user_id):
        posts = dbc.fetch_all_as_dict(
            dbc.DB, POSTS_COLLECT, {USER_ID: user_id}
            )
        return posts
    else:
        raise ValueError(f'Get failure: {user_id} not in database.')


def fetch_by_post_id(post_id: str):
    """
    fetch all posts thats linked to that user_id
    """
    dbc.connect_db()
    return dbc.fetch_one(POSTS_COLLECT, {ID: ObjectId(post_id)})


def del_post(post_id: str):
    """
    delete post_id
    """
    dbc.connect_db()
    dbc.del_one(POSTS_COLLECT, {ID: ObjectId(post_id)})
