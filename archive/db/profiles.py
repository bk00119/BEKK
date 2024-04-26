# import db.db_connect as dbc
# from bson import ObjectId
# import random

# MOCK_ID = "_id"
# NAME = "Name"

# GOALS = "Goals"
# POSTS = "Posts"
# TASKS = "Tasks"
# PRIVATE = "Private"

# GROUPS = "Groups"
# GROUP = "GROUP"
# GOAL = "Goal"
# PROFILES_COLLECT = "profiles"


# TEST_PROFILE = {
#     NAME: "john adams",
#     GOALS: ["cs hw1", "fin hw2"],
#     TASKS: [],
#     POSTS: [],
#     PRIVATE: True,
# }
# ID_LEN = 24

# BIG_NUM = 100_000_000_000_000_000_000


# def get_new_test_goal():
#     """
#     example task for testing add_goal()
#     """
#     test_goal = {}
#     _id = random.randint(0, BIG_NUM)
#     _id = str(_id)
#     _id = _id.rjust(ID_LEN, '0')
#     # test_goal[MOCK_ID] = 'test123'
#     # test_goal[NAME] = 'Test name'
#     # test_goal[GROUPS] = 'Test group'
#     # return test_goal
#     test_goal[MOCK_ID] = _id
#     test_goal[NAME] = 'Test name'
#     test_goal[GROUPS] = 'Test group'
#     test_goal[GOALS] = ['goal1', 'goal2']
#     test_goal[GOAL] = 'goal1'
#     test_goal[PRIVATE] = True
#     return test_goal


# def get_new_test_group():
#     """
#     example task for testing add_goal()
#     """
#     test_group = {}
#     _id = random.randint(0, BIG_NUM)
#     _id = str(_id)
#     _id = _id.rjust(ID_LEN, '0')
#     # test_goal[MOCK_ID] = 'test123'
#     # test_goal[NAME] = 'Test name'
#     # test_goal[GROUPS] = 'Test group'
#     # return test_goal
#     test_group[MOCK_ID] = _id
#     test_group[NAME] = 'Test name'
#     test_group[GROUPS] = 'Test group'
#     test_group[GOALS] = ['goal1', 'goal2']
#     test_group[GOAL] = 'goal1'
#     test_group[PRIVATE] = True
#     return test_group


# def get_test_profile():
#     return TEST_PROFILE


# def get_profile(user_id: str):
#     dbc.connect_db()
#     profile = dbc.fetch_one(PROFILES_COLLECT, {MOCK_ID: ObjectId(user_id)})
#     return profile


# def del_profile(user_id: str):
#     dbc.connect_db()
#     dbc.del_one(PROFILES_COLLECT, {MOCK_ID: ObjectId(user_id)})
#     return dbc.fetch_one(PROFILES_COLLECT, {MOCK_ID: ObjectId(user_id)})


# def get_goals():
#     dbc.connect_db()
#     return dbc.fetch_all_as_dict(dbc.DB, PROFILES_COLLECT)


# def get_groups(user_id: str):
#     dbc.connect_db()
#     # profiles = dbc.fetch_all_as_dict(dbc.DB, PROFILES_COLLECT)
#     profile = dbc.fetch_one(PROFILES_COLLECT, {MOCK_ID: ObjectId(user_id)})
#     groups = profile.get('Groups')
#     return groups


# def add_profile(name: str, goals: list,
#                 tasks: list, posts: list, private: bool):
#     dbc.connect_db()
#     _id = dbc.insert_one(
#                         PROFILES_COLLECT,
#                         {
#                             NAME: name,
#                             GOALS: goals,
#                             TASKS: tasks,
#                             POSTS: posts,
#                             PRIVATE: private,
#                         })
#     return _id


# def add_goal(id: str, goal: str):
#     dbc.connect_db()

#     dbc.update_one(
#         PROFILES_COLLECT,
#         {MOCK_ID: ObjectId(id)},
#         {'$push': {GOALS: goal}}
#     )
#     return dbc.fetch_one(PROFILES_COLLECT, {MOCK_ID: ObjectId(id)})


# def add_group(id: str, group: str):
#     dbc.connect_db()
#     # added = dbc.DB[PROFILES_COLLECT].update_one(
#     #     {'_id': id},
#     #     {'$push': {'Groups': group}}
#     # )
#     dbc.update_one(
#         PROFILES_COLLECT,
#         {MOCK_ID: ObjectId(id)},
#         {'$push': {GROUPS: group}}
#     )
#     return dbc.fetch_one(PROFILES_COLLECT, {MOCK_ID: ObjectId(id)})


# # def add_goal(user_id: str, goal: str):
# #     dbc.connect_db()
# #     if not user_id:
# #         raise ValueError('user_id may not be blank')
# #     if not goal:
# #         raise ValueError('goal may not be blank')
# #     goal = {}
# #     goal[USER_ID] = user_id
# #     task[TITLE] = title
# #     task[CONTENT] = content
# #     task[STATUS] = 1
# #     task[LIKES] = []
# #     dbc.connect_db()
# #     _id = dbc.insert_one(TASKS_COLLECT, task)
# #     return _id
