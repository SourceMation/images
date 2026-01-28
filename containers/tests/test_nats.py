import pytest
import subprocess
import time
import requests

def test_nats_installed():
    # Use /bin/nats-server since that's where we put it
    result = subprocess.run(
        ['/bin/nats-server', '--version'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    assert result.returncode == 0, "nats-server is not installed"
    assert "nats-server" in result.stdout or "nats-server" in result.stderr, "Unexpected output from nats-server --version"

def test_nats_running():
    # Wait for nats to start (although the build script usually waits 10s)
    # The monitoring port is 8222 by default in our config
    max_retries = 5
    for i in range(max_retries):
        try:
            response = requests.get("http://localhost:8222/varz")
            if response.status_code == 200:
                data = response.json()
                assert data['port'] == 4222
                return
        except requests.exceptions.ConnectionError:
            time.sleep(1)
    
    pytest.fail("NATS server is not responding on monitoring port 8222")
