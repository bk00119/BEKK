
MOCK_ID = 123

NAME = "Name" 
GROUPS = "Groups"
PRIVATE = "Private"
GOALS = "Goals" 

TEST_PROFILE = {
    NAME: "john smith", 
    GROUPS: ["cs", "fin"],
    PRIVATE: True,
    GOALS: ["cs hw1", "fin hw2"] 
}

def get_test_profile():
    return TEST_PROFILE  

def get_profile(user_id:str):
    return TEST_PROFILE

def add_profile(name: str, goals: list, private: bool, groups: list):
    pass
