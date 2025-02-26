import os
import subprocess
import pytest
import socket

@pytest.fixture(scope="module")
def jenkins_environment():
    jenkins_home = os.getenv('JENKINS_HOME')
    jenkins_version = os.getenv('JENKINS_VERSION')

    if not jenkins_home or not jenkins_version:
        pytest.fail("Environment variables JENKINS_HOME and/or JENKINS_VERSION are not set")

    return jenkins_home, jenkins_version

def test_jenkins_home_and_version(jenkins_environment):
    jenkins_home, jenkins_version = jenkins_environment

    assert os.path.isdir(jenkins_home), f"Path {jenkins_home} for JENKINS_HOME does not exist"

    assert jenkins_version, "JENKINS_VERSION variable is missing or empty"

def test_initial_admin_password(jenkins_environment):
    jenkins_home, _ = jenkins_environment
    password_file_path = os.path.join(jenkins_home, 'secrets', 'initialAdminPassword')

    assert os.path.isfile(password_file_path), f"File {password_file_path} does not exist"
    with open(password_file_path, 'r') as f:
        content = f.read().strip()
    assert content, "initialAdminPassword file is empty"

def test_jenkins_port():
    port = 8080
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result = s.connect_ex(('localhost', port))
        assert result == 0, f"Jenkins is not listening on port {port}"

def test_jenkins_install_page():
    result = subprocess.run(['curl', 'http://localhost:8080/login?from=%2F'], capture_output=True, text=True, check=True)
    assert 'Unlock Jenkins' in result.stdout, "Text 'Unlock Jenkins' not found on the install page"
    