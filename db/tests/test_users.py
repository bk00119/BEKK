 
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

@pytest.mark.skip(reason="endpoint does not exist yet") 
def test_get_profile():
    users = usrs.get_profile()
    assert isinstance(users, dict)

def test_generate_access_token(temp_user):
    temp_access_token = usrs.generate_access_token(temp_user[usrs.ID])
    payload = jwt.decode(temp_access_token,
        auth.SECRET_KEY, algorithms=['HS256'])
    assert temp_user[usrs.ID] == payload[usrs.USER_ID]
