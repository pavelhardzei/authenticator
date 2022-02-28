from http import HTTPStatus
from unittest.mock import ANY


def test_signup(api_client):
    response = api_client.post('/user/signup/', json={'email': 'test@test.org', 'username': 'test',
                                                      'password': 'testing321'})
    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {'id': ANY, 'email': 'test@test.org', 'username': 'test'}


def test_signin(api_client, user1):
    response = api_client.post('/user/signin/', json={'email': 'user1@gmail.com', 'password': 'testing321'})
    assert response.status_code == HTTPStatus.OK
    assert response.json == {'user': {'id': ANY, 'email': 'user1@gmail.com', 'username': 'user1'}, 'token': ANY}


def test_user_detail(api_client, token_user1):
    response = api_client.get('/user/', headers={'Authorization': f'Token {token_user1}'})
    assert response.status_code == HTTPStatus.OK
    assert response.json == {'id': ANY, 'email': 'user1@gmail.com', 'username': 'user1'}


def test_user_detail_unauthorized(api_client):
    response = api_client.get('/user/')
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json == {'message': 'Token is required'}


def test_user_put(api_client, token_user1):
    response = api_client.put('/user/', headers={'Authorization': f'Token {token_user1}'},
                              json={'email': 'new@gmail.com', 'username': 'new'})
    assert response.status_code == HTTPStatus.OK
    assert response.json == {'id': ANY, 'email': 'new@gmail.com', 'username': 'new'}


def test_user_invalid_put(api_client, token_user1):
    response = api_client.put('/user/', headers={'Authorization': f'Token {token_user1}'},
                              json={'email': 'new@gmail.com', 'username': 'new', 'password': 'testing321'})
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json == {'message': [{'password': ['Unknown field.']}]}


def test_user_patch(api_client, token_user1):
    response = api_client.patch('/user/', headers={'Authorization': f'Token {token_user1}'}, json={'username': 'new'})
    assert response.status_code == HTTPStatus.OK
    assert response.json == {'id': ANY, 'email': 'user1@gmail.com', 'username': 'new'}


def test_user_delete(api_client, token_user1):
    response = api_client.delete('/user/', headers={'Authorization': f'Token {token_user1}'})
    assert response.status_code == HTTPStatus.NO_CONTENT
