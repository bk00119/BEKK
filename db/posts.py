MOCK_ID = 0
USER_ID = "user_id"
IS_COMPLETED = "is_completed"
CONTENT = "content"
TASK_IDS = "task_ids"
GOAL_IDS = "goal_ids"
LIKE_IDS = "like_ids"
COMMENT_IDS = "comment_ids"


def get_test_post():
    return {
        USER_ID: "1",
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
    pass
