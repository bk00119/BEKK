 
import db.users as usrs
import pytest

@pytest.fixture(scope='function')
def temp_user():
    sample_user = {
        'username': 'user1234',
        'password': 'pw1234'
    }
    return sample_user

# def test_get_users():
#     users = usrs.get_users()
#     assert isinstance(users, dict)
#     assert len(users) > 0  # at least one user!
#     for key in users:
#         assert isinstance(key, str)
#         assert len(key) >= usrs.MIN_USER_NAME_LEN
#         user = users[key]
#         assert isinstance(user, dict)
#         assert usrs.LEVEL in user
#         assert isinstance(user[usrs.LEVEL], int)

@pytest.mark.skip(reason="endpoint does not exist yet") 
def test_get_profile():
    users = usrs.get_profile()
    assert isinstance(users, dict)

def test_duplicate_username_signup(temp_user):
    # check signing up with the exisitng username
    with pytest.raises(ValueError):
        usrs.signup(temp_user)
