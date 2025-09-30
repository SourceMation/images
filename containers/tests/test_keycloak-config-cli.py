import os
import pytest
import subprocess
import pwd
import requests

CLI_HOME = "/opt/keycloak-config-cli"
CLI_USER = "cli"
CLI_JAR = os.path.join(CLI_HOME, 'keycloak-config-cli.jar')
CLI_COMMAND = ["java", "-jar", CLI_JAR]
KEYCLOAK_USERNAME = os.getenv("KEYCLOAK_USER")
KEYCLOAK_PASSWORD = os.getenv("KEYCLOAK_PASSWORD")
KEYCLOAK_URL = os.getenv("KEYCLOAK_URL")
IMPORT_FILES_LOCATIONS = os.getenv("IMPORT_FILES_LOCATIONS")

def get_admin_token():
    """Helper function to obtain an admin access token from Keycloak."""
    token_url = f"{KEYCLOAK_URL}/realms/master/protocol/openid-connect/token"
    payload = {
        "client_id": "admin-cli",
        "username": KEYCLOAK_USERNAME,
        "password": KEYCLOAK_PASSWORD,
        "grant_type": "password",
    }
    response = requests.post(token_url, data=payload, verify=False)
    response.raise_for_status()
    return response.json()["access_token"]

def test_installation_and_permissions():
    """
    Tests that the home directory has the correct ownership.
    """
    assert os.path.isdir(CLI_HOME)
    stat_info = os.stat(CLI_HOME)
    owner_user = pwd.getpwuid(stat_info.st_uid).pw_name
    assert owner_user == CLI_USER

def test_key_files_exist():
    """
    Tests that key files (the JAR and entrypoint script) exist and are executable.
    """
    assert os.path.isfile(CLI_JAR), f"CLI JAR file not found at {CLI_JAR}"
    
    entrypoint_path = '/usr/local/bin/entrypoint.sh'
    assert os.path.isfile(entrypoint_path), f"Entrypoint script not found at {entrypoint_path}"
    assert os.access(entrypoint_path, os.X_OK), "Entrypoint script is not executable"


def test_import_realm_on_live_keycloak():
    """
    End-to-end test: imports a realm from /config, then verifies its creation via the API.
    """
    command = CLI_COMMAND
    
    print(f"Running import command: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True, check=True, timeout=60)
    
    assert "keycloak-config-cli ran in" in result.stdout, f"CLI import failed. Output:\n{result.stdout}\n{result.stderr}"

    token = get_admin_token()
    headers = {"Authorization": f"Bearer {token}"}

    realm_url = f"{KEYCLOAK_URL}/admin/realms/my-example-realm"
    response_realm = requests.get(realm_url, headers=headers, verify=False)
    assert response_realm.status_code == 200, "Realm 'my-example-realm' was not found after import."

    role_url = f"{KEYCLOAK_URL}/admin/realms/my-example-realm/roles/user"
    response_role = requests.get(role_url, headers=headers, verify=False)
    assert response_role.status_code == 200, "Role 'user' was not found after import."

    users_url = f"{KEYCLOAK_URL}/admin/realms/my-example-realm/users?username=testuser&exact=true"
    response_users = requests.get(users_url, headers=headers, verify=False)
    assert response_users.status_code == 200, "Request for user 'testuser' failed."
    users_data = response_users.json()
    assert len(users_data) == 1, "User 'testuser' was not found after import."
    assert users_data[0]["username"] == "testuser"
