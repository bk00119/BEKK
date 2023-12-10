import db.db_connect as dbc
MOCK_ID = 123

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
    return TEST_PROFILE[GOALS]


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
