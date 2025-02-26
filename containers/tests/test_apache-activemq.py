import subprocess
import pytest
import os
import requests
from requests.auth import HTTPBasicAuth

ACTIVEMQ_HOME = "/opt/apache-activemq"
ACTIVEMQ_BIN = os.path.join(ACTIVEMQ_HOME, "bin", "activemq")
ACTIVEMQ_URL = "http://localhost:8161"
USERNAME = "admin"
PASSWORD = "admin"

@pytest.mark.skipif(not os.path.exists(ACTIVEMQ_BIN), reason="ActiveMQ is not installed.")
def test_activemq_installed():
    assert os.path.exists(ACTIVEMQ_BIN), "ActiveMQ is not installed at the expected location."

def test_activemq_version():
    try:
        result = subprocess.run([ACTIVEMQ_BIN, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        assert result.returncode == 0, "Failed to execute 'activemq --version'."
        assert "ActiveMQ" in result.stdout, "Unexpected output from 'activemq --version'."
    except FileNotFoundError:
        pytest.fail("ActiveMQ binary not found.")

def test_activemq_web_console_accessible():
    try:
        response = requests.get(ACTIVEMQ_URL, auth=HTTPBasicAuth(USERNAME, PASSWORD))
        assert response.status_code == 200, f"ActiveMQ web console returned unexpected status code {response.status_code}."
        assert "ActiveMQ" in response.text, "ActiveMQ web console did not return expected content."
    except requests.ConnectionError:
        pytest.fail("Unable to connect to ActiveMQ web console.")

def test_activemq_send_message():
    message = "Test_Message"
    queue = "test_queue"
    
    command = f"activemq producer --destination {queue} --message \"{message}\" --messageCount 1"
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    
    assert result.returncode == 0, f"Failed to send message: {result.stderr}"
    assert "Elapsed time in second" in result.stdout, f"Unexpected output: {result.stdout}"

def test_activemq_receive_message():
    message = "Test_Message"
    queue = "test_queue"
    
    receive_command = f"activemq consumer --destination {queue} --messageCount 1"
    receive_result = subprocess.run(receive_command, shell=True, text=True, capture_output=True)
    
    assert receive_result.returncode == 0, f"Failed to receive message: {receive_result.stderr}"
    assert message in receive_result.stdout, f"Expected message not found: {receive_result.stdout}"
