def test_signup(api_client):
    response = api_client.post('/user/signup/', json={'email': 'test1@test.org', 'username': 'test',
                                                      'password': 'testing321'})
    assert response.status_code == 200
