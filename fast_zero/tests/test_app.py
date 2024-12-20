from http import HTTPStatus


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Estelar'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'estela',
            'email': 'stel@stel.com',
            'password': 'asol',
        },
    )

    # Retornou o status_code correto?
    assert response.status_code == HTTPStatus.CREATED

    # Valida UserPublic
    assert response.json() == {
        'id': 1,
        'username': 'estela',
        'email': 'stel@stel.com',
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'username': 'estela',
                'email': 'stel@stel.com',
            }
        ]
    }


def test_update_users(client):
    response = client.put(
        '/users/1',
        json={
            'id': 1,
            'username': 'filium',
            'email': 'fill@fill.com',
            'password': 'beyond',
        },
    )

    assert response.json() == {
        'id': 1,
        'username': 'filium',
        'email': 'fill@fill.com',
    }


def test_put_a_non_existing_user(client):
    response = client.put(
        '/users/4',
        json={
            'id': 4,
            'username': 'filium',
            'email': 'fill@fill.com',
            'password': 'beyond',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_a_non_existing_user_(client):
    response = client.delete('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
