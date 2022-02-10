from unittest.mock import ANY


def test_signup(api_client):
    response = api_client.post('/user/signup/', json={'email': 'test1@test.org', 'username': 'test',
                                                      'password': 'testing321'})
    assert response.status_code == 201
    assert response.json == {'id': ANY, 'email': 'test1@test.org', 'username': 'test'}


def test_signin(api_client, user1):
    response = api_client.post('/user/signin/', json={'email': 'user1@gmail.com', 'password': 'testing321'})
    assert response.status_code == 200
    assert response.json == {'user': {'id': ANY, 'email': 'user1@gmail.com', 'username': ANY}, 'token': ANY}
