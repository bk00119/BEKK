import db.db_connect as dbc
import db.users as usrs

MOCK_ID = 0
POSTS_COLLECT = "posts"
USER_ID = "user_id"
IS_COMPLETED = "is_completed"
CONTENT = "content"
TASK_IDS = "task_ids"
GOAL_IDS = "goal_ids"
LIKE_IDS = "like_ids"
COMMENT_IDS = "comment_ids"


def get_test_post():
    return {
        USER_ID: "65f27756a4817e4be8a2a5e9",
        IS_COMPLETED: False,
        CONTENT: "test task",
        TASK_IDS: [],
        GOAL_IDS: [],
        LIKE_IDS: [],
        COMMENT_IDS: []
    }


def add_post(user_id,
             is_completed,
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
                            IS_COMPLETED: is_completed,
                            CONTENT: content,
                            TASK_IDS: task_ids,
                            GOAL_IDS: goal_ids,
                            LIKE_IDS: like_ids,
                            COMMENT_IDS: comment_ids
                        })
    return _id


def fetch_by_user_id(user_id: str):
    dbc.connect_db()
    if usrs.id_exists(user_id):
        posts = dbc.fetch_all_as_dict(
            dbc.DB, POSTS_COLLECT, {USER_ID: user_id}
            )
        return posts
    else:
        raise ValueError(f'Get failure: {user_id} not in database.')
