import pytest
from apps.authentication.models import User

@pytest.fixture(scope='module')
def new_user():
    user = User(name='test',email = 'test@abc.local',password = 'test')
    return user