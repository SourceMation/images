import os
import pytest
import subprocess
import pwd
import requests
import time

ELASTIC_HOME = "/usr/share/elasticsearch"
ELASTIC_USER = "elasticsearch"
HTTP_PORT = 9200
TRANSPORT_PORT = 9300

def test_installation_and_permissions():
    dirs_to_check = [ELASTIC_HOME, os.path.join(ELASTIC_HOME, 'data'), os.path.join(ELASTIC_HOME, 'logs')]
    for d in dirs_to_check:
        assert os.path.isdir(d)
        stat_info = os.stat(d)
        owner_uid = stat_info.st_uid
        owner_user = pwd.getpwuid(owner_uid).pw_name
        assert owner_user == ELASTIC_USER

@pytest.mark.parametrize("binary_name", ["elasticsearch", "elasticsearch-plugin", "elasticsearch-keystore", "elasticsearch-reset-password", "elasticsearch-users"])
def test_core_binaries_exist_and_are_executable(binary_name):
    binary_path = os.path.join(ELASTIC_HOME, 'bin', binary_name)
    assert os.path.isfile(binary_path), f"Binary not found: {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Binary is not executable: {binary_path}"

def test_elasticsearch_process_is_running():
    try:
        result = subprocess.run(['ps', 'auxww'], capture_output=True, text=True, check=True)
        assert "org.elasticsearch.bootstrap.Elasticsearch" in result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        pytest.fail(f"Failed to check processes with 'ps auxww': {e}")

@pytest.mark.parametrize("port", [HTTP_PORT, TRANSPORT_PORT])
def test_elasticsearch_is_listening_on_ports(port):
    try:
        result = subprocess.run(['ss', '-tuln'], capture_output=True, text=True, check=True)
        port_is_listening = False
        for line in result.stdout.splitlines():
            if "LISTEN" in line and f":{port}" in line:
                port_is_listening = True
                break
        assert port_is_listening, f"Port {port} was not found in a 'LISTEN' state."
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        pytest.fail(f"Failed to check listening ports with 'ss': {e}")

def test_cluster_health_is_yellow_or_green():
    health_url = f"http://localhost:{HTTP_PORT}/_cluster/health"
    
    for _ in range(20):
        try:
            requests.get(f"http://localhost:{HTTP_PORT}/", timeout=5)
            break
        except requests.ConnectionError:
            time.sleep(5)
    else:
        pytest.fail("Elasticsearch server did not become available on port 9200 within the timeout period.")

    try:
        health_check_url = f"{health_url}?wait_for_status=yellow&timeout=60s"
        response = requests.get(health_check_url, timeout=65)
        response.raise_for_status()

        health_json = response.json()
        status = health_json.get('status')
        assert status in ['yellow', 'green'], f"Cluster health is '{status}', expected 'yellow' or 'green'."

    except requests.RequestException as e:
        pytest.fail(f"Failed to get cluster health: {e}")