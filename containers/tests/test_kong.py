import subprocess
import requests
import pytest

KONG_ADMIN_API_URL = "http://localhost:8001"
KONG_PROXY_URL = "http://localhost:8000"
TEST_SERVICE_URL = "http://httpbin.org/get"
TEST_ROUTE_PATH = "/test"


def test_kong_process_running():
    result = subprocess.run(["ps", "aux"], stdout=subprocess.PIPE, text=True)
    assert "nginx" in result.stdout, "Kong process not found (nginx not running)"

def test_kong_admin_api_accessible():
    """Test: Sprawdź, czy Admin API jest dostępne."""
    try:
        response = requests.get(f"{KONG_ADMIN_API_URL}/")
        assert response.status_code == 200, "Admin API is not accessible."
        assert "version" in response.json(), "Version info not found in Admin API response."
    except requests.ConnectionError:
        pytest.fail("Failed to connect to Kong Admin API.")

def test_kong_proxy_api_accessible():
    """Test: Sprawdź, czy Proxy API jest dostępne."""
    try:
        response = requests.get(KONG_PROXY_URL)
        assert response.status_code in [200, 404], "Proxy API did not return a valid response."
    except requests.ConnectionError:
        pytest.fail("Failed to connect to Kong Proxy API.")

def test_create_service_and_route():
    """Test: Stwórz usługę i trasę w Kong i przetestuj routing."""
    service_response = requests.post(
        f"{KONG_ADMIN_API_URL}/services",
        json={"name": "test-service", "url": TEST_SERVICE_URL}
    )
    assert service_response.status_code == 201, "Failed to create service."

    route_response = requests.post(
        f"{KONG_ADMIN_API_URL}/services/test-service/routes",
        json={"paths": [TEST_ROUTE_PATH]}
    )
    assert route_response.status_code == 201, "Failed to create route."

def test_cleanup_service_and_route():
    route_response = requests.get(f"{KONG_ADMIN_API_URL}/services/test-service/routes")
    assert route_response.status_code == 200, f"Failed to get routes, got {route_response.status_code}."
    route_data = route_response.json()
    
    if route_data["data"]:
        route_id = route_data["data"][0]["id"]
        route_delete_response = requests.delete(f"{KONG_ADMIN_API_URL}/routes/{route_id}")
        assert route_delete_response.status_code == 204, f"Failed to delete route, got {route_delete_response.status_code}."
    else:
        print("No routes found, skipping route deletion.")

    service_response = requests.get(f"{KONG_ADMIN_API_URL}/services/test-service")
    assert service_response.status_code == 200, f"Failed to get service, got {service_response.status_code}."
    service_data = service_response.json()
    
    if service_data:
        service_id = service_data["id"]
        service_delete_response = requests.delete(f"{KONG_ADMIN_API_URL}/services/{service_id}")
        assert service_delete_response.status_code == 204, f"Failed to delete service, got {service_delete_response.status_code}."
    else:
        print("Service not found, skipping service deletion.")