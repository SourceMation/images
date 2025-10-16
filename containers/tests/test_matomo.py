import os
import pytest
import subprocess
import requests
import time

MATOMO_ROOT = "/var/www/html"
APACHE_PORT = 80

def test_core_files_were_copied():
    """
    Tests that the entrypoint script successfully copied the Matomo files.
    """
    assert os.path.isfile(os.path.join(MATOMO_ROOT, "index.php")), "Core Matomo files seem to be missing."
    assert os.path.isdir(os.path.join(MATOMO_ROOT, "config")), "config/ directory not found."
    assert not os.path.isfile(os.path.join(MATOMO_ROOT, "config/config.ini.php"))

def test_apache_process_is_running():
    """
    Tests that the Apache server process is running.
    """
    try:
        result = subprocess.run(['ps', 'auxww'], capture_output=True, text=True, check=True)
        assert "apache2 -DFOREGROUND" in result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        pytest.fail(f"Failed to check processes with 'ps auxww': {e}")

def test_apache_is_listening_on_port():
    """
    Tests that Apache is listening on port 80.
    """
    try:
        result = subprocess.run(['ss', '-tuln'], capture_output=True, text=True, check=True)
        port_is_listening = False
        for line in result.stdout.splitlines():
            if "LISTEN" in line and f":{APACHE_PORT}" in line:
                port_is_listening = True
                break
        assert port_is_listening, f"Port {APACHE_PORT} was not found in a 'LISTEN' state."
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        pytest.fail(f"Failed to check listening ports with 'ss': {e}")

def test_matomo_welcome_page_is_served():
    """
    Tests that the server returns the Matomo welcome/setup page,
    which confirms that the stack is working.
    """
    url = f"http://localhost:{APACHE_PORT}/"
    
    response = None
    for _ in range(15):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                break
        except requests.ConnectionError:
            time.sleep(5)
    else:
        pytest.fail("Matomo server did not become available.")

    assert response.status_code == 200
    assert "text/html" in response.headers.get('Content-Type', '')
    
    response_text = response.text
    
    assert "<title>Matomo" in response_text and "Installation</title>" in response_text
    assert "<h2>Welcome</h2>" in response_text
    assert "System Check" in response_text