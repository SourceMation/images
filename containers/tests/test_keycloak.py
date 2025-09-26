import pytest
import os
import requests
import random
import string

KEYCLOAK_USER = "admin"
KEYCLOAK_PASSWORD = "admin"
NODE_IP = "localhost"
NODE_PORT = "8080"

if not all([KEYCLOAK_PASSWORD, NODE_IP, NODE_PORT]):
    raise ValueError("One or more environment variables are not set: KEYCLOAK_PASSWORD, KEYCLOAK_NODE_IP, KEYCLOAK_NODE_PORT")

BASE_URL = f"http://{NODE_IP}:{NODE_PORT}"
ADMIN_URL = f"{BASE_URL}/admin"

test_state = {}

def random_string(length=8):
    """Generates a random string."""
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

@pytest.fixture(scope="session")
def admin_token():
    """Acquires an admin token once per session."""
    token_url = f"{BASE_URL}/realms/master/protocol/openid-connect/token"
    payload = {
        'client_id': 'admin-cli',
        'username': KEYCLOAK_USER,
        'password': KEYCLOAK_PASSWORD,
        'grant_type': 'password',
    }
    response = requests.post(token_url, data=payload)
    response.raise_for_status()
    return response.json()["access_token"]

@pytest.fixture(scope="session")
def auth_headers(admin_token):
    """Returns authorization headers for admin API calls."""
    return {
        "Authorization": f"Bearer {admin_token}",
        "Content-Type": "application/json"
    }

@pytest.mark.order(1)
def test_keycloak_is_accessible():
    """Checks if the Keycloak main page is accessible."""
    response = requests.get(BASE_URL, timeout=10)
    assert response.status_code == 200
    assert "Keycloak" in response.text

@pytest.mark.order(2)
def test_create_realm(auth_headers):
    """Creates a new realm for tests and stores its name."""
    realm_name = f"test-realm-{random_string()}"
    test_state["realm_name"] = realm_name
    
    payload = {"realm": realm_name, "enabled": True}
    response = requests.post(f"{ADMIN_URL}/realms", headers=auth_headers, json=payload)
    assert response.status_code == 201, f"Failed to create realm. Response: {response.text}"
    print(f"Created realm: {realm_name}")

@pytest.mark.order(3)
def test_modify_realm(auth_headers):
    """Modifies a setting in the test realm."""
    realm_name = test_state["realm_name"]
    payload = {"registrationEmailAsUsername": True, "rememberMe": True}
    response = requests.put(f"{ADMIN_URL}/realms/{realm_name}", headers=auth_headers, json=payload)
    assert response.status_code == 204

    verify_response = requests.get(f"{ADMIN_URL}/realms/{realm_name}", headers=auth_headers)
    assert verify_response.json()["registrationEmailAsUsername"] is True
    assert verify_response.json()["rememberMe"] is True

@pytest.mark.order(4)
def test_create_user(auth_headers):
    """Creates a new user and stores their details."""
    realm_name = test_state["realm_name"]
    username = f"testuser-{random_string()}"
    email = f"{username}@example.local"
    password = "testpassword123"

    payload = {
        "username": username,
        "email": email,
        "firstName": "Test",
        "lastName": "User",
        "enabled": True,
        "emailVerified": True,
        "credentials": [{"type": "password", "value": password, "temporary": False}],
        "requiredActions": []
    }
    response = requests.post(f"{ADMIN_URL}/realms/{realm_name}/users", headers=auth_headers, json=payload)
    assert response.status_code == 201, f"Failed to create user. Response: {response.text}"

    user_id_url = response.headers.get('Location')
    user_id = user_id_url.split('/')[-1]

    test_state["user_id"] = user_id
    test_state["user_email"] = email
    test_state["user_password"] = password
    print(f"Created user with ID: {user_id}")

@pytest.mark.order(5)
def test_update_user(auth_headers):
    """Modifies the created user's attributes."""
    realm_name = test_state["realm_name"]
    user_id = test_state["user_id"]
    user_url = f"{ADMIN_URL}/realms/{realm_name}/users/{user_id}"

    get_response = requests.get(user_url, headers=auth_headers)
    user_data = get_response.json()

    assert user_data["email"] == test_state["user_email"]

    user_data["firstName"] = "John"
    user_data["lastName"] = "Doe"

    response = requests.put(user_url, headers=auth_headers, json=user_data)
    assert response.status_code == 204

    verify_response = requests.get(user_url, headers=auth_headers)
    assert verify_response.json()["firstName"] == "John"
    assert verify_response.json()["lastName"] == "Doe"

@pytest.mark.order(6)
def test_user_login():
    """Verifies that the created user can log in."""
    realm_name = test_state["realm_name"]
    token_url = f"{BASE_URL}/realms/{realm_name}/protocol/openid-connect/token"
    
    payload = {
        'client_id': 'admin-cli',
        'username': test_state["user_email"],
        'password': test_state["user_password"],
        'grant_type': 'password',
    }
    response = requests.post(token_url, data=payload)
    assert response.status_code == 200, f"Failed to log in. Response: {response.text}"
    assert "access_token" in response.json()

@pytest.mark.order(7)
def test_user_permissions_check(auth_headers):
    """Checks the user's assigned roles (permissions), expecting default roles."""
    user_id = test_state["user_id"]
    realm_name = test_state["realm_name"]
    roles_url = f"{ADMIN_URL}/realms/{realm_name}/users/{user_id}/role-mappings"
    
    response = requests.get(roles_url, headers=auth_headers)
    assert response.status_code == 200
    
    response_data = response.json()
    assert "realmMappings" in response_data, "User should have realm mappings"
    assert len(response_data["realmMappings"]) == 1, "User should have one default realm role"
    assert "default-roles" in response_data["realmMappings"][0]["description"], "User should have one default realm role"

@pytest.mark.order(8)
def test_delete_user(auth_headers):
    """Deletes the created user."""
    realm_name = test_state["realm_name"]
    user_id = test_state["user_id"]
    user_url = f"{ADMIN_URL}/realms/{realm_name}/users/{user_id}"
    
    response = requests.delete(user_url, headers=auth_headers)
    assert response.status_code == 204, "Failed to delete test user"
    print(f"Deleted user with ID: {user_id}")

    response = requests.get(user_url, headers=auth_headers)
    assert response.status_code == 404, "User still exists after deletion"

@pytest.mark.order(9)
def test_delete_realm(auth_headers):
    """Deletes the test realm to clean up."""
    realm_name = test_state["realm_name"]
    realm_url = f"{ADMIN_URL}/realms/{realm_name}"
    
    response = requests.delete(realm_url, headers=auth_headers)
    assert response.status_code == 204, "Failed to delete test realm"
    print(f"Deleted realm: {realm_name}")

    response = requests.get(realm_url, headers=auth_headers)
    assert response.status_code == 404, "Realm still exists after deletion"