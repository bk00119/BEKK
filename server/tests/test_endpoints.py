
import server.endpoints as ep

TEST_CLIENT = ep.app.test_client()

SAMPLE_USER = {
    'id': 'user1234',
    'password': 'pw1234'
}

def test_login():
    resp = TEST_CLIENT.post(ep.LOGIN_EP, json=SAMPLE_USER)
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert ep.TOKEN_RESP in resp_json