import pytest
from apps.authentication.models import User
from apps import create_app, db
from apps.config import config_dict

@pytest.fixture(scope='module')
def new_user():
    user = User(username='test',email = 'test@abc.local',password = 'test')
    return user


@pytest.fixture(scope='module')
def test_client():
    get_config_mode = 'Testing'
    
    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

    app = create_app(app_config)

    # Create a test client using the Flask application configured for testing
    with app.test_client() as testing_client:
        # Establish an application context
        with app.app_context():
            yield testing_client  # this is where the testing happens!  


@pytest.fixture(scope='module')
def init_database(test_client):
    # Create the database and the database table
    db.create_all()

    # Insert user data
    user1 = User(username = 'John Smith', email='sjohn@abc.local', password_plaintext='s3cr3t')
    user2 = User(username = 'Jane Smith', email='sjane@abc.local', password_plaintext='s3cr3t')
    db.session.add(user1)
    db.session.add(user2)

    # Commit the changes for the users
    db.session.commit()

    yield  # this is where the testing happens!

    db.drop_all()


  