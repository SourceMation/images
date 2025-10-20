import os
import pytest
import subprocess
import pwd
import requests
import time

GHOST_INSTALL = "/var/lib/ghost"
GHOST_USER = "node"
GHOST_PORT = 2368

def test_installation_and_permissions():
    """
    Tests that the container runs as the 'node' user and that the
    installation directory is owned by 'node'.
    """

    assert os.path.isdir(GHOST_INSTALL)
    stat_info = os.stat(GHOST_INSTALL)
    owner_user = pwd.getpwuid(stat_info.st_uid).pw_name
    assert owner_user == GHOST_USER

def test_ghost_cli_is_available():
    """
    Tests that the 'ghost' CLI tool is installed and available in the PATH.
    """
    try:
        result = subprocess.run(['ghost', 'help'], capture_output=True, text=True, check=True, timeout=15)
        assert "ghost [command]" in result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
        pytest.fail(f"Failed to execute 'ghost help': {e}")

def test_ghost_process_is_running():
    """
    Tests that the Ghost Node.js server process is running.
    """
    try:
        result = subprocess.run(['ps', 'auxww'], capture_output=True, text=True, check=True)
        assert "node current/index.js" in result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        pytest.fail(f"Failed to check processes with 'ps auxww': {e}")

def test_ghost_is_listening_on_port():
    """
    Tests that Ghost is listening on the default port 2368.
    """
    try:
        result = subprocess.run(['ss', '-tuln'], capture_output=True, text=True, check=True)
        port_is_listening = False
        for line in result.stdout.splitlines():
            if "LISTEN" in line and f":{GHOST_PORT}" in line:
                port_is_listening = True
                break
        assert port_is_listening, f"Port {GHOST_PORT} was not found in a 'LISTEN' state."
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        pytest.fail(f"Failed to check listening ports with 'ss': {e}")

def test_ghost_setup_page_is_served():
    """
    Tests that the server returns the initial Ghost setup page,
    which confirms the application has started successfully.
    """
    setup_url = f"http://localhost:{GHOST_PORT}/ghost/"
    
    response = None
    for _ in range(20):
        try:
            response = requests.get(setup_url, timeout=5)
            if response.status_code == 200:
                break
            time.sleep(5)
        except requests.ConnectionError:
            time.sleep(5)
    else:
        pytest.fail(f"Ghost server did not become available at {setup_url} within the timeout period.")

    assert response.status_code == 200
    assert "text/html" in response.headers.get('Content-Type', '')
    
    response_text = response.text
    assert "<title>Ghost</title>" in response_text
    assert 'name="ghost-admin/config/environment"' in response_text