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
        USER_ID: "6575033f3b89d2b4f309d7af",
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
                'comment_ids': 1,
                'timestamp': 1,
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


def id_exists(id: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(POSTS_COLLECT, {ID: ObjectId(id)})


def add_comment(post_id: str, comment_id: str):
    if id_exists(post_id):
        dbc.update_one(POSTS_COLLECT, {ID: ObjectId(post_id)},
                       {"$addToSet": {COMMENT_IDS: comment_id}})
    else:
        raise ValueError(f'Adding comment Failed: {post_id} not in DB.')


def is_post_liked(post_id: str, user_id: str):
    if id_exists(post_id):
        post = dbc.fetch_one(POSTS_COLLECT, {ID: ObjectId(post_id),
                                             LIKE_IDS: {"$in": [user_id]}})
        if post:
            return True
        return False
    else:
        raise ValueError(f'Post {post_id} has no likes.')


def like_post(post_id: str, user_id: str):
    if id_exists(post_id):
        if is_post_liked(post_id, user_id):
            raise ValueError(f'Failed: user {user_id} already liked task.')

        dbc.update_one(POSTS_COLLECT, {ID: ObjectId(post_id)},
                       {"$addToSet": {LIKE_IDS: user_id}})
    else:
        raise ValueError(f'Like Failed: {post_id} not in DB.')


def unlike_post(post_id: str, user_id: str):
    if id_exists(post_id):
        if not is_post_liked(post_id, user_id):
            raise ValueError(f'Failed: Already unliked task {post_id}.')

        dbc.update_one(POSTS_COLLECT, {ID: ObjectId(post_id)},
                       {"$pull": {LIKE_IDS: user_id}})
    else:
        raise ValueError(f'Unlike Failed: post {post_id} not in DB.')


def get_post_likes(post_id: str):
    try:
        post = fetch_by_post_id(post_id)

        if post:
            user_ids = post.get(LIKE_IDS)
            like_count = len(user_ids)
            users = []
            for user_id in user_ids:
                if usrs.id_exists(user_id):
                    user_data = usrs.get_user_public(user_id)
                    if usrs.USERNAME in user_data:
                        users.append({
                            usrs.USERNAME: user_data[usrs.USERNAME],
                            usrs.USER_ID: user_id
                        })

            return {
                "like_count": like_count,
                "users": users
            }
        else:
            raise ValueError(f'Post: {post_id} not found.')
    except Exception as e:
        raise ValueError(f'Error getting post likes: {e}')


def remove_task(post_id: str, task_id: str):
    if id_exists(post_id):
        # check if task_id in in the field
        tasks = fetch_by_post_id(post_id)[TASK_IDS]
        if (task_id not in tasks):
            raise ValueError(f'Task ID: {task_id} DNE in post {post_id}')

        # pop it off the field
        dbc.update_one(POSTS_COLLECT, {ID: ObjectId(post_id)},
                       {"$pull": {TASK_IDS: task_id}})
    else:
        raise ValueError(f'Adding comment Failed: {post_id} not in DB.')


def remove_goal(post_id: str, goal_id: str):
    if id_exists(post_id):
        # check if goal_id is in the field
        goals = fetch_by_post_id(post_id)[GOAL_IDS]
        if (goal_id not in goals):
            raise ValueError(f'Goal ID: {goal_id} DNE in post {post_id}')

        # remove it from the field
        dbc.update_one(POSTS_COLLECT, {ID: ObjectId(post_id)},
                       {"$pull": {GOAL_IDS: goal_id}})
    else:
        raise ValueError(f'Removing goal failed: {post_id} not found in DB.')
