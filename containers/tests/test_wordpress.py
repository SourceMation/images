import os
import pytest
import subprocess
import requests
import time

WP_ROOT = "/var/www/html"
APACHE_PORT = 80

def test_installation_and_config_files():
    """
    Tests that key WordPress files, including the generated wp-config.php, exist.
    """
    assert os.path.isfile(os.path.join(WP_ROOT, "wp-config.php")), "wp-config.php was not created."
    assert os.path.isfile(os.path.join(WP_ROOT, "wp-login.php")), "Core WordPress files seem to be missing."
    assert os.path.isdir(os.path.join(WP_ROOT, "wp-admin")), "wp-admin directory not found."

def test_wp_config_has_unique_salts():
    """
    Tests that the wp-config.php file contains unique security salts,
    not the default placeholders.
    """
    with open(os.path.join(WP_ROOT, "wp-config.php"), 'r') as f:
        config_content = f.read()
    
    assert "put your unique phrases here" not in config_content

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

def test_wordpress_setup_page_is_served():
    """
    Tests that the server returns the WordPress setup page,
    which confirms a successful database connection.
    """
    url = f"http://localhost:{APACHE_PORT}/"
    
    response = None
    for _ in range(10):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                break
            time.sleep(3)
        except requests.ConnectionError:
            time.sleep(3)
    else:
        pytest.fail("WordPress server did not become available.")

    assert response.status_code == 200
    assert "text/html" in response.headers.get('Content-Type', '')
    
    expected_text_found = (
        "<title>WordPress &rsaquo; Installation</title>" in response.text or
        '<body class="wp-core-ui language-chooser">' in response.text
    )
    
    assert expected_text_found, "The response does not seem to be the WordPress installation page."