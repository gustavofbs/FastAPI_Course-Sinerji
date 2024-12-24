from http import HTTPStatus

from fast_zero.schemas import UserPublic


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


def test_create_a_existing_username(client, user):
    response = client.post(
        '/users/',
        json={
            'id': 2,
            'username': 'aurelion',
            'email': 'beyond@riot.com',
            'password': '159',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_create_a_existing_email(client, user):
    response = client.post(
        '/users/',
        json={
            'id': 2,
            'username': 'beyond',
            'email': 'asol@asol.com',
            'password': '159',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_read_user_by_id(client, user):
    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': user.username,
        'email': user.email,
    }


def test_read_a_non_existing_user(client):
    response = client.get('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User Not Found'}


def test_update_users(client, user):
    response = client.put(
        '/users/1',
        json={
            'id': 1,
            'username': 'aurelion',
            'email': 'asol@asol.com',
            'password': 'great',
        },
    )

    assert response.json() == {
        'id': 1,
        'username': 'aurelion',
        'email': 'asol@asol.com',
    }


def test_put_a_non_existing_user(client, user):
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
    assert response.json() == {'detail': 'User Not Found'}


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_a_non_existing_user_(client):
    response = client.delete('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User Not Found'}
