import os
import pytest
import subprocess
import requests
import time
import re

PMA_ROOT = "/var/www/html"
APACHE_PORT = 80

def test_config_file_was_created_for_specific_host():
    """
    Tests that the entrypoint script generated config.inc.php
    with a specific host configuration (not arbitrary server mode).
    """
    config_file = os.path.join(PMA_ROOT, "config.inc.php")
    assert os.path.isfile(config_file), "config.inc.php was not created."

    with open(config_file, 'r') as f:
        config_content = f.read()
    
    assert "$cfg['blowfish_secret'] = ''" not in config_content
    assert "$cfg['Servers'][$i]['host']" in config_content
    assert "$cfg['AllowArbitraryServer'] = true;" not in config_content

def test_core_files_and_dirs_exist():
    """
    Tests that key phpMyAdmin files and directories are in place.
    """
    assert os.path.isfile(os.path.join(PMA_ROOT, "index.php")), "index.php is missing."
    assert os.path.isdir(os.path.join(PMA_ROOT, "tmp")), "tmp/ directory was not created."

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

def test_can_login_to_database():
    """
    Tests that we can successfully log in to the MariaDB database
    through the phpMyAdmin web interface.
    """
    base_url = f"http://localhost:{APACHE_PORT}/"
    login_url = f"{base_url}index.php"
    
    for _ in range(10):
        try:
            requests.get(login_url, timeout=5)
            break
        except requests.ConnectionError:
            time.sleep(2)
    else:
        pytest.fail("phpMyAdmin server did not become available.")
    
    with requests.Session() as session:
        get_response = session.get(login_url)
        assert get_response.status_code == 200
        
        token_match = re.search(r'<input type="hidden" name="token" value="([a-f0-9]+)"', get_response.text)
        assert token_match, "Could not find login token on the page."
        token = token_match.group(1)

        login_data = {
            'pma_username': 'root',
            'pma_password': 'root',
            'server': '1',
            'token': token
        }
        
        post_response = session.post(login_url, data=login_data, allow_redirects=True)
        
        assert post_response.status_code == 200, f"Login POST request failed with status {post_response.status_code}"
        
        response_text = post_response.text
        
        title_match = re.search(r'<title>(.*?)<\/title>', response_text)
        assert title_match and 'phpMyAdmin' in title_match.group(1), "Could not find 'phpMyAdmin' in the page title after login."
        
        assert "Database server" in response_text
        assert "Server version:" in response_text
        assert "pma_login_form" not in response_text, "Login form is still visible, login likely failed."