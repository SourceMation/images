import os
import pytest
import subprocess
import pwd
import requests
import time

GRAFANA_HOME = "/usr/share/grafana"
GRAFANA_USER = "grafana"
GRAFANA_PORT = 3000
GRAFANA_LOG_FILE = os.path.join(GRAFANA_HOME, 'data', 'log', 'grafana.log')

@pytest.fixture(scope="module")
def grafana_server_is_ready():
    health_url = f"http://localhost:{GRAFANA_PORT}/api/health"
    for _ in range(15):
        try:
            response = requests.get(health_url, timeout=5)
            if response.status_code == 200:
                return
        except requests.ConnectionError:
            time.sleep(6)
    else:
        pytest.fail(f"Grafana server did not become available on port {GRAFANA_PORT} within the timeout period.")

def test_installation_and_permissions():
    dirs_to_check = [GRAFANA_HOME, os.path.join(GRAFANA_HOME, 'data')]
    for d in dirs_to_check:
        assert os.path.isdir(d)
        stat_info = os.stat(d)
        owner_uid = stat_info.st_uid
        owner_user = pwd.getpwuid(owner_uid).pw_name
        assert owner_user == GRAFANA_USER

@pytest.mark.parametrize("binary_name", ["grafana", "grafana-server"])
def test_grafana_binaries_exist_and_are_executable(binary_name):
    binary_path = os.path.join(GRAFANA_HOME, 'bin', binary_name)
    assert os.path.isfile(binary_path), f"Binary not found: {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Binary is not executable: {binary_path}"

def test_grafana_process_is_running():
    try:
        result = subprocess.run(['ps', 'auxww'], capture_output=True, text=True, check=True)
        assert "bin/grafana server" in result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        pytest.fail(f"Failed to check processes with 'ps auxww': {e}")

def test_grafana_is_listening_on_port():
    try:
        result = subprocess.run(['ss', '-tuln'], capture_output=True, text=True, check=True)
        port_is_listening = False
        for line in result.stdout.splitlines():
            if "LISTEN" in line and f":{GRAFANA_PORT}" in line:
                port_is_listening = True
                break
        assert port_is_listening, f"Port {GRAFANA_PORT} was not found in a 'LISTEN' state."
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        pytest.fail(f"Failed to check listening ports with 'ss': {e}")

def test_health_check_endpoint(grafana_server_is_ready):
    health_url = f"http://localhost:{GRAFANA_PORT}/api/health"
    try:
        response = requests.get(health_url, timeout=10)
        response.raise_for_status()

        health_json = response.json()
        assert health_json.get('database') == 'ok', f"Health check failed. DB status is not 'ok'. Response: {health_json}"
        assert 'version' in health_json, "Health check response is missing 'version' key."

    except requests.RequestException as e:
        pytest.fail(f"Failed to get cluster health: {e}")
        
def test_startup_log_messages(grafana_server_is_ready):
    assert os.path.isfile(GRAFANA_LOG_FILE), f"Log file not found at {GRAFANA_LOG_FILE}"
    
    with open(GRAFANA_LOG_FILE, 'r') as f:
        log_content = f.read()

    assert "HTTP Server Listen" in log_content, "Log message for HTTP server start not found."
    assert "ngalert.scheduler" in log_content and "Starting scheduler" in log_content
    assert "app-registry" in log_content and "app registry initialized" in log_content