from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(
        username='aurelion',
        email='aurelion@asol.com',
        password='asol',
    )

    session.add(user)
    session.commit()

    result = session.scalar(
        select(User).where(User.email == 'aurelion@asol.com')
    )

    assert result.username == 'aurelion'
