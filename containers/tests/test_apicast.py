import pytest
import requests
import json

APICAST_URL = "http://localhost:8080"

def test_gateway_is_online_and_responding():
    response = requests.get(f"{APICAST_URL}/")
    assert response.status_code == 200
    assert "GET / HTTP/1.1" in response.text

@pytest.mark.parametrize("path", [
    "/get",
    "/anything/goes/here"
])
def test_routing_to_echo_api(path):
    url = f"{APICAST_URL}{path}"
    response = requests.get(url)
    assert response.status_code == 200
    assert f"GET {path} HTTP/1.1" in response.text

def test_headers():
    url = f"{APICAST_URL}/headers"
    custom_headers = {
        'X-Test-Header': 'MyTestValue123',
        'User-Agent': 'Pytest-Client'
    }
    response = requests.get(url, headers=custom_headers)
    assert response.status_code == 200
    assert "GET /headers HTTP/1.1" in response.text

def test_post_request():
    url = f"{APICAST_URL}/post"
    payload = {"user": "test_user", "permissions": [1, 2, 3]}
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    assert "POST /post HTTP/1.1" in response.text