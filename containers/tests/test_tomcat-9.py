import os
import pytest
import subprocess
import requests
import time

CATALINA_HOME = "/usr/local/tomcat"
TOMCAT_PORT = 8080

def test_installation():
    assert os.path.isdir(CATALINA_HOME)

@pytest.mark.parametrize("binary_name", ["catalina.sh", "startup.sh", "shutdown.sh", "version.sh"])
def test_tomcat_binaries_exist_and_are_executable(binary_name):
    binary_path = os.path.join(CATALINA_HOME, 'bin', binary_name)
    assert os.path.isfile(binary_path), f"Binary not found: {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Binary is not executable: {binary_path}"

def test_tomcat_native_library_loaded():
    try:
        # Run configtest and capture output
        result = subprocess.run([os.path.join(CATALINA_HOME, 'bin/catalina.sh'), 'configtest'], capture_output=True, text=True)
        # Check both stdout and stderr as configtest often prints to stderr
        output = result.stdout + result.stderr
        # We expect to see info about loaded Apache Tomcat Native library
        assert "Apache Tomcat Native library" in output
        assert "INFO: Loaded" in output or "INFO: Apache Tomcat Native library" in output
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        pytest.fail(f"Failed to run catalina.sh configtest: {e}")

def test_tomcat_is_listening_on_port():
    # In some test environments we might need to start the process first if it's not already running
    # but usually the test is run inside the running container
    try:
        # Give it a moment to start if needed
        time.sleep(2)
        result = subprocess.run(['ss', '-tuln'], capture_output=True, text=True, check=True)
        assert f":{TOMCAT_PORT}" in result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        # If ss is not available, try netstat
        try:
            result = subprocess.run(['netstat', '-tuln'], capture_output=True, text=True, check=True)
            assert f":{TOMCAT_PORT}" in result.stdout
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.fail(f"Failed to check listening ports: {e}")

def test_server_is_responding():
    url = f"http://localhost:{TOMCAT_PORT}/"
    try:
        # Retry logic to wait for Tomcat to be ready
        response = None
        for _ in range(15):
            try:
                response = requests.get(url, timeout=5)
                # Any status code is fine as long as the server responds
                break
            except requests.ConnectionError:
                time.sleep(2)
        else:
            pytest.fail("Tomcat server did not become available.")

        # Since we moved webapps to webapps.dist, we expect a 404
        assert response.status_code == 404
        # The default 404 page should contain "Apache Tomcat/9.0"
        assert "Apache Tomcat" in response.text or "Tomcat" in response.text
        
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to Tomcat server: {e}")
