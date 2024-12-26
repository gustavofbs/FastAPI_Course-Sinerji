from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.schemas import UserPublic
from fast_zero.security import create_access_token


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


def test_read_users(client: TestClient, token):
    response = client.get(
        '/users/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'username': 'aurelion',
                'email': 'asol@asol.com',
            }
        ]
    }


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


def test_update_users(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'beyond',
            'email': 'bey@ond.com',
            'password': 'great',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': 'beyond',
        'email': 'bey@ond.com',
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_get_current_user_not_found(client):
    data = {'no-email': 'test'}
    token = create_access_token(data)

    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_does_not_exists(client):
    data = {'sub': 'as@as.com'}
    token = create_access_token(data)

    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert token['access_token']
