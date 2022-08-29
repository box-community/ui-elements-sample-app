import pytest
from apps.authentication.models import User
from apps import create_app, db
from apps.booking.models import Dive_Site, Diver
from apps.config import config_dict

@pytest.fixture(scope='module')
def new_user():
    user = User(username='test',email = 'test@abc.local',password = 'test')
    return user

@pytest.fixture(scope='module')
def new_diver_john():
    diver = Diver(name='John Smith',email = 'sjohn@example.com')
    return diver

@pytest.fixture(scope='module')
def new_diver_barduino():
    diver = Diver(name='Barduino R',email = 'barduinor@gmail.com')
    return diver

@pytest.fixture(scope='module')
def new_diver_barbas():
    diver = Diver(name='Barbas R',email = 'barbasr@gmail.com')
    return diver    

@pytest.fixture(scope='module')
def new_diver_jane():
    diver = Diver(name='Jane Smith',email = 'sjane@example.com')
    return diver    

@pytest.fixture(scope='module')
def db_diver_john():
    diver = Diver.query.filter_by(email='sjohn@example.com').first()
    return diver


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
    user1 = User(username = 'John Smith', email='sjohn@example.com', password='s3cr3t')
    user2 = User(username = 'Jane Smith', email='sjane@example.com', password='s3cr3t')
    db.session.add(user1)
    db.session.add(user2)

    # Insert dive site data
    dive_site1 = Dive_Site(name = 'Test dive site 1')
    dive_site2 = Dive_Site(name = 'Test dive site 2')
    db.session.add(dive_site1)
    db.session.add(dive_site2)
    

    # Commit the changes for the users
    db.session.commit()

    yield  # this is where the testing happens!

    db.drop_all()

@pytest.fixture(scope='module')
def init_db(test_client):
    # Create the database and the database table
    db.create_all()

    db.session.commit()

    yield  # this is where the testing happens!

    db.drop_all()



  