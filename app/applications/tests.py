from unittest.mock import ANY


def test_application_list(api_client, token_user1, app1_user1, app2_user1):
    response = api_client.get('/application/', headers={'Authorization': f'Token {token_user1}'})
    assert response.status_code == 200
    assert response.json == [{'id': ANY, 'name': 'app1'}, {'id': ANY, 'name': 'app2'}]


def test_application_post(api_client, token_user1, app1_user1):
    pass
