import pytest


@pytest.fixture(scope="function")
def unauthenticated_api_client(request):
    # What about drf-mongoengine
    from rest_framework.test import APIClient

    client = APIClient()
    # tox fails without the following client.get()
    # without it the next client.get(url)...
    # will result in 404 regardless of the url
    # it seems like it is an initialization issue maybe
    # of client.requests and not of the client itself.
    response = client.get("")
    assert response.status_code == 404
    yield client
