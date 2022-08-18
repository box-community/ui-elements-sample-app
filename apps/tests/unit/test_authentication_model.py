from apps.authentication.models import User
from apps.authentication.util import verify_pass

def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, password_hashed, authenticated, and active fields are defined correctly
    """
    user = User(username='test',email = 'test@abc.local',password = 'test')
    assert user.username == 'test'
    assert user.email == 'test@abc.local'
    assert verify_pass('test',user.password)


def test_new_user_with_fixture(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email and password_hashed fields are defined correctly
    """
    assert new_user.username == 'test'
    assert new_user.email == 'test@abc.local'
    assert verify_pass('test',new_user.password)