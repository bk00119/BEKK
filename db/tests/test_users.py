 
import db.users as usrs
import pytest
import jwt
import db.auth as auth
import db.db_connect as dbc

@pytest.fixture(scope='function')
def temp_user():
    sample_user = {
        usrs.USERNAME: 'user1234',
        usrs.PASSWORD: 'pw1234',
        usrs.ID: '6575033f3b89d2b4f309d7af',
        usrs.FIRST_NAME: 'Firstname',
        usrs.LAST_NAME: 'Lastname',
        usrs.EMAIL: 'test@test.com'
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

@pytest.mark.skip(reason="working on signup") 
def test_duplicate_username_signup(temp_user):
    # check signing up with the exisitng username
    with pytest.raises(ValueError):
        usrs.signup(temp_user)

@pytest.mark.skip(reason="working on signup") 
def test_signup(temp_user):
    # check signing up with a new username
    temp_user['username'] = 'user12345'
    usrs.signup(temp_user)
    assert usrs.retrieve_user(temp_user['username']) == temp_user['password']

# @pytest.mark.skip(reason="working on signup")
# def test_remove_user(user_id):

def test_generate_access_token(temp_user):
    temp_access_token = usrs.generate_access_token(temp_user[usrs.ID])
    payload = jwt.decode(temp_access_token,
        auth.SECRET_KEY, algorithms=['HS256'])
    assert temp_user[usrs.ID] == payload[usrs.USER_ID]

def test_generate_refresh_token(temp_user):
    # CREATE A TEMP USER IN DB
    del temp_user[usrs.ID]
    user_id = usrs.signup(temp_user)

    # TEST REFRESH TOKEN
    temp_refresh_token = usrs.generate_refresh_token(user_id)

    payload = jwt.decode(temp_refresh_token,
        auth.SECRET_KEY, algorithms=['HS256'])
    assert user_id == payload[usrs.USER_ID]

    # REMVOE A TEMP USER IN DB
    usrs.remove_user(user_id)
