import os
import pytest
import subprocess
import pwd
import requests
import time

KIBANA_HOME = "/usr/share/kibana"
KIBANA_USER = "kibana"
KIBANA_PORT = 5601

def test_installation_and_permissions():
    assert os.path.isdir(KIBANA_HOME)
    stat_info = os.stat(KIBANA_HOME)
    owner_uid = stat_info.st_uid
    owner_user = pwd.getpwuid(owner_uid).pw_name
    assert owner_user == KIBANA_USER

def test_kibana_binary_is_linked():
    symlink_path = '/usr/local/bin/kibana'
    assert os.path.islink(symlink_path)
    assert os.path.basename(os.readlink(symlink_path)) == 'kibana'

def test_kibana_process_is_running():
    try:
        result = subprocess.run(['ps', 'auxww'], capture_output=True, text=True, check=True)

        kibana_process_found = False
        for line in result.stdout.splitlines():
            if line.startswith(KIBANA_USER) and "bin/node" in line and "cli/dist" in line:
                kibana_process_found = True
                break
        
        assert kibana_process_found, "Kibana Node.js process not found or command structure has changed."

    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        pytest.fail(f"Failed to check processes with 'ps auxww': {e}")

def test_kibana_is_listening_on_port():
    try:
        result = subprocess.run(['ss', '-tuln'], capture_output=True, text=True, check=True)
        
        port_is_listening = False
        for line in result.stdout.splitlines():
            if "LISTEN" in line and f":{KIBANA_PORT}" in line:
                port_is_listening = True
                break
        
        assert port_is_listening, f"Port {KIBANA_PORT} was not found in a 'LISTEN' state."

    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        pytest.fail(f"Failed to check listening ports with 'ss': {e}")

def test_api_status_endpoint_is_unavailable_without_elasticsearch():
    status_url = f"http://localhost:{KIBANA_PORT}/api/status"
    
    response = None
    for _ in range(15):
        try:
            response = requests.get(status_url, timeout=10)
            if response is not None:
                break
        except requests.ConnectionError:
            time.sleep(6)
    else:
        pytest.fail("Kibana server did not become available on port 5601 within the timeout period.")

    assert response.status_code == 503, f"Expected status 503 (Service Unavailable) from /api/status, but got {response.status_code}"
    
    status_json = response.json()
    assert 'status' in status_json, "Status JSON response is missing 'status' key."
    
    overall_status = status_json.get('status', {}).get('overall', {})
    level = overall_status.get('level')
    
    assert level == 'unavailable', f"Expected overall level to be 'unavailable' without Elasticsearch, but got '{level}'."