import db.db_connect as dbc
from bson import ObjectId

MOCK_ID = "_id"

NAME = "Name"
GROUPS = "Groups"
PRIVATE = "Private"
GOALS = "Goals"
PROFILES_COLLECT = "profiles"

TEST_PROFILE = {
    NAME: "john smith",
    GROUPS: ["cs", "fin"],
    PRIVATE: True,
    GOALS: ["cs hw1", "fin hw2"]
}


def get_test_profile():
    return TEST_PROFILE


def get_profile(user_id: str):
    return TEST_PROFILE


def get_goals():
    dbc.connect_db()
    return dbc.fetch_all_as_dict(dbc.DB, PROFILES_COLLECT)


def get_groups():
    dbc.connect_db()
    profiles = dbc.fetch_all_as_dict(dbc.DB, PROFILES_COLLECT)
    groups_list = [profile.get('Groups', []) if isinstance(profile, dict)
                   else [] for profile in profiles]
    return groups_list


def add_profile(name: str, goals: list, private: bool, groups: list):
    dbc.connect_db()
    _id = dbc.insert_one(
                        PROFILES_COLLECT,
                        {
                            NAME: name,
                            GROUPS: groups,
                            PRIVATE: private,
                            GOALS: goals,
                        })
    return _id


def add_goal(id: str, goal: str):
    dbc.connect_db()
    dbc.insert_one(PROFILES_COLLECT, {MOCK_ID: ObjectId(id), GOALS: goal})
    return dbc.fetch_one(PROFILES_COLLECT, {MOCK_ID: ObjectId(id)})


def add_group(id: str, group: str):
    dbc.connect_db()
    added = dbc.DB[PROFILES_COLLECT].update_one(
        {'_id': id},
        {'$push': {'Groups': group}}
    )
    if added.modified_count > 0:
        return id
    else:
        return False

# def add_goal(user_id: str, goal: str):
#     dbc.connect_db()
#     if not user_id:
#         raise ValueError('user_id may not be blank')
#     if not goal:
#         raise ValueError('goal may not be blank')
#     goal = {}
#     goal[USER_ID] = user_id
#     task[TITLE] = title
#     task[CONTENT] = content
#     task[STATUS] = 1
#     task[LIKES] = []
#     dbc.connect_db()
#     _id = dbc.insert_one(TASKS_COLLECT, task)
#     return _id
