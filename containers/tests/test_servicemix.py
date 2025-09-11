import os
import pytest
import subprocess
import time

SERVICEMIX_HOME = '/opt/servicemix'
SERVICEMIX_LOG_FILE = os.path.join(SERVICEMIX_HOME, 'data/log/servicemix.log')

def test_installation_directories_and_files():
    assert os.path.isdir(SERVICEMIX_HOME)
    executables = ['servicemix', 'client', 'karaf']
    for exe in executables:
        path = os.path.join(SERVICEMIX_HOME, 'bin', exe)
        assert os.path.isfile(path)
        assert os.access(path, os.X_OK)

def test_java_home_is_set_correctly():
    java_home = os.environ.get('JAVA_HOME')
    assert java_home is not None, "JAVA_HOME environment variable is not set."
    assert os.path.isdir(java_home), f"JAVA_HOME directory does not exist: {java_home}"
    
    java_executable_path = os.path.join(java_home, 'bin', 'java')
    assert os.path.isfile(java_executable_path), f"Java executable not found at {java_executable_path}"
    assert os.access(java_executable_path, os.X_OK), f"Java executable is not executable: {java_executable_path}"

def test_servicemix_version_file():
    version_file = '/var/tmp/sourcemation.yml'
    assert os.path.exists(version_file)
    with open(version_file, 'r') as f:
        content = f.read()
        assert "servicemix:" in content

def test_java_process_is_running():
    java_home = os.environ.get('JAVA_HOME')
    assert java_home, "Cannot run test because JAVA_HOME is not set."
    
    expected_java_path = os.path.join(java_home, 'bin', 'java')
    
    try:
        result = subprocess.run(['ps', 'auxww'], capture_output=True, text=True, check=True)
        assert expected_java_path in result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        pytest.fail(f"Failed to check processes with 'ps auxww': {e}")

def test_server_is_ready_and_client_connects():
    server_ready = False
    for i in range(45):
        time.sleep(1)
        if os.path.exists(SERVICEMIX_LOG_FILE):
            with open(SERVICEMIX_LOG_FILE, 'r') as log:
                log_content = log.read()
                if 'Pax Web available at' in log_content:
                    server_ready = True
                    break
    
    assert server_ready, f"Server did not become ready within the timeout period. Log file '{SERVICEMIX_LOG_FILE}' might not contain 'Pax Web available at'."
    
    command = [os.path.join(SERVICEMIX_HOME, 'bin/client'), 'bundle:list']
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True, timeout=20)
        output = result.stdout
        assert "ID" in output
        assert "State" in output
        assert "Lvl" in output
        assert "Name" in output
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        pytest.fail(f"Client command failed: {e}")

@pytest.mark.parametrize("port", [8181, 8101])
def test_default_ports_are_listening(port):
    try:
        result = subprocess.run(['ss', '-tuln'], capture_output=True, text=True, check=True)
        assert f":{port}" in result.stdout
        assert "LISTEN" in result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        pytest.fail(f"Failed to check listening ports with 'ss': {e}")

@pytest.mark.parametrize("feature_name", ["camel", "camel-blueprint", "activemq-broker-noweb", "cxf"])
def test_core_features_are_installed(feature_name):
    command = [os.path.join(SERVICEMIX_HOME, 'bin/client'), 'feature:list']
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True, timeout=20)
        
        feature_found_and_started = False
        for line in result.stdout.splitlines():
            if feature_name in line and "Started" in line:
                columns = [col.strip() for col in line.split('|')]
                if len(columns) > 3 and columns[0] == feature_name and columns[3] == "Started":
                    feature_found_and_started = True
                    break
        
        assert feature_found_and_started, f"Feature '{feature_name}' was not found in 'Started' state."

    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        pytest.fail(f"Failed to list features: {e}")