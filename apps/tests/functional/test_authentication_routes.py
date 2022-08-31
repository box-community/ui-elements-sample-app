"""
Functional tests for the `authentication` blueprint.

These tests use GETs and POSTs to different URLs to check for the proper behavior
of the blueprint.
"""

from flask import url_for
from apps.authentication import blueprint

def test_login_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is requested (GET)
    THEN check the response is valid
    """
    url = '/login'
    response = test_client.get(url)
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Email' in response.data
    assert b'Password' in response.data

def test_valid_login_logout(test_client, init_database):

    """
    GIVEN a Flask application configured for testing
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'have an account' in response.data
    assert b'Logout' not in response.data
  
    assert b'Sign UP' in response.data    



    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post('/login',
                                data=dict(email='sjohn@example.com', password='s3cr3t'),
                                follow_redirects=True)
    assert response.status_code == 200
    # print(f"RESPONSE: {response.data}")
    assert b'John Smith' in response.data
    assert b'Explorer' in response.data
    assert b'Logout' in response.data
    # assert b'Login' not in response.data
    # assert b'Register' not in response.data

    """
    GIVEN a Flask application configured for testing
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'have an account' in response.data
    assert b'Logout' not in response.data
  
    assert b'Sign UP' in response.data     