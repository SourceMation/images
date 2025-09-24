import os
import pytest
import subprocess
import pwd
import requests
import time
import re

APACHE_HOME = "/opt/apache2"
APACHE_USER_UID = 1001
APACHE_PORT = 8080

def test_installation_and_permissions():
    # Sprawdź istnienie i uprawnienia do katalogu APACHE_HOME
    assert os.path.isdir(APACHE_HOME)
    stat_info = os.stat(APACHE_HOME)
    assert stat_info.st_uid == APACHE_USER_UID
    assert stat_info.st_gid == APACHE_USER_UID

@pytest.mark.parametrize("binary_name", ["httpd", "apachectl"])
def test_apache_binaries_exist_and_are_executable(binary_name):
    binary_path = os.path.join(APACHE_HOME, 'bin', binary_name)
    assert os.path.isfile(binary_path), f"Binary not found: {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Binary is not executable: {binary_path}"

def test_apache_configuration():
    config_file = os.path.join(APACHE_HOME, 'conf/httpd.conf')
    assert os.path.isfile(config_file)
    
    with open(config_file, 'r') as f:
        config_content = f.read()
    
    assert "Listen 8080" in config_content
    assert "ServerName localhost" in config_content

def test_apache_process_is_running():
    try:
        result = subprocess.run(['ps', 'auxww'], capture_output=True, text=True, check=True)
        assert os.path.join(APACHE_HOME, 'bin/httpd') in result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        pytest.fail(f"Failed to check processes with 'ps auxww': {e}")

def test_apache_is_listening_on_port():
    try:
        time.sleep(2)
        result = subprocess.run(['ss', '-tuln'], capture_output=True, text=True, check=True)
        port_is_listening = False
        for line in result.stdout.splitlines():
            if "LISTEN" in line and f":{APACHE_PORT}" in line:
                port_is_listening = True
                break
        assert port_is_listening, f"Port {APACHE_PORT} was not found in a 'LISTEN' state."
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        pytest.fail(f"Failed to check listening ports with 'ss': {e}")

def test_default_page_is_served():
    url = f"http://localhost:{APACHE_PORT}/"
    try:
        for _ in range(5):
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    break
            except requests.ConnectionError:
                time.sleep(1)
        else:
            pytest.fail("Apache server did not become available.")

        assert response.status_code == 200
        assert "Apache" in response.headers.get('Server', '')
        assert "It works!" in response.text
        
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to Apache server: {e}")