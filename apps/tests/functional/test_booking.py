"""
Functional tests for the `booking` blueprint.

These tests use GETs and POSTs to different URLs to check for the proper behavior
of the blueprint.
"""

def test_booking_start(test_client, init_database):   
    """
    GIVEN a Flask application configured for testing
    WHEN the '/booking/step1' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/booking')
    assert response.status_code == 200
    assert b'Book a dive' in response.data
    assert b'Date' in response.data
    assert b'Site' in response.data
    