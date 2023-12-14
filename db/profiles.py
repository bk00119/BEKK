import db.db_connect as dbc
from bson import ObjectId
import random

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
ID_LEN = 24

BIG_NUM = 100_000_000_000_000_000_000


def get_new_test_goal():
    """
    example task for testing add_goal()
    """
    test_goal = {}
    _id = random.randint(0, BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(ID_LEN, '0')
    # test_goal[MOCK_ID] = 'test123'
    # test_goal[NAME] = 'Test name'
    # test_goal[GROUPS] = 'Test group'
    # return test_goal
    test_goal[MOCK_ID] = _id
    test_goal[NAME] = 'Test name'
    test_goal[GROUPS] = 'Test group'
    test_goal[GOALS] = ['goal1', 'goal2']
    test_goal[PRIVATE] = True
    return test_goal


def get_test_profile():
    return TEST_PROFILE


def get_profile(user_id: str):
    return TEST_PROFILE


def del_profile(user_id: str):
    dbc.connect_db()
    dbc.del_one(PROFILES_COLLECT, {MOCK_ID: ObjectId(user_id)})
    return dbc.fetch_one(PROFILES_COLLECT, {MOCK_ID: ObjectId(user_id)})


def get_goals():
    dbc.connect_db()
    return dbc.fetch_all_as_dict(dbc.DB, PROFILES_COLLECT)


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

    dbc.update_one(
        PROFILES_COLLECT,
        {MOCK_ID: ObjectId(id)},
        {'$push': {GOALS: goal}}
    )
    return dbc.fetch_one(PROFILES_COLLECT, {MOCK_ID: ObjectId(id)})
