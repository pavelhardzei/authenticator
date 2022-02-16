from http import HTTPStatus
from unittest.mock import ANY

import pyotp


def test_application_list(api_client, token_user1, app1_user1, app2_user1):
    response = api_client.get('/application/', headers={'Authorization': f'Token {token_user1}'})
    assert response.status_code == HTTPStatus.OK
    assert response.json == [{'id': ANY, 'name': 'app1'}, {'id': ANY, 'name': 'app2'}]


def test_application_post(api_client, token_user1):
    response = api_client.post('/application/', headers={'Authorization': f'Token {token_user1}'},
                               json={'name': 'app', 'secret': 'base32secret'})
    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {'id': ANY, 'name': 'app'}


def test_application_detail(api_client, token_user1, app1_user1):
    response = api_client.get(f'/application/{app1_user1.id}/', headers={'Authorization': f'Token {token_user1}'})
    assert response.status_code == HTTPStatus.OK
    assert response.json == {'id': app1_user1.id, 'name': 'app1'}


def test_application_detail_violation(api_client, token_user1, app1_user2):
    response = api_client.get(f'/application/{app1_user2.id}/', headers={'Authorization': f'Token {token_user1}'})
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {'message': 'Resource not found'}


def test_application_put(api_client, token_user1, app1_user1):
    response = api_client.put(f'/application/{app1_user1.id}/', headers={'Authorization': f'Token {token_user1}'},
                              json={'name': 'new'})
    assert response.status_code == HTTPStatus.OK
    assert response.json == {'id': app1_user1.id, 'name': 'new'}


def test_application_delete(api_client, token_user1, app1_user1):
    response = api_client.delete(f'/application/{app1_user1.id}/', headers={'Authorization': f'Token {token_user1}'})
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_application_code(api_client, token_user2, app1_user2):
    response = api_client.get(f'/application/{app1_user2.id}/code/',
                              headers={'Authorization': f'Token {token_user2}'})
    assert response.status_code == HTTPStatus.OK
    assert response.json == {'totp': pyotp.TOTP('base32secret').now()}
