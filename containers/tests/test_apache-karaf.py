import os
import subprocess
import pytest
import time

@pytest.fixture(scope="module", autouse=True)
def setup_environment():
    # Add Karaf bin directory to PATH if necessary
    karaf_home = os.getenv("KARAF_HOME", "/opt/apache-karaf")
    os.environ["PATH"] = f"{karaf_home}/bin:" + os.environ.get("PATH", "")
    os.environ["JAVA_HOME"] = "/usr/lib/jvm/jre-11-openjdk"
    assert os.path.exists(karaf_home), "KARAF_HOME directory does not exist. Ensure Karaf is installed."

def test_karaf_version():
    result = subprocess.run(["karaf", "--version"], capture_output=True, text=True)
    assert result.returncode == 0, "Karaf command failed. Ensure Karaf is installed and accessible."
    assert "Apache Karaf" in result.stdout, "Karaf version output is incorrect."


def test_karaf_client():
    """Test Karaf client interaction."""
    try:
        result = subprocess.run(["karaf", "client", "help"], capture_output=True, text=True, timeout=10)
        assert "karaf@root()" in result.stdout, "Karaf client output is incorrect."
    except subprocess.TimeoutExpired:
        pytest.fail("Karaf client command timed out.")


def test_karaf_start():
    """Start Karaf and verify it is running."""
    result = subprocess.run(["karaf", "start"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to start Karaf with karaf start"
    # Wait for Karaf to start
    # NOW start karaf as server that is detached so we can run the test case
    karaf_server = subprocess.Popen(["karaf", "server"],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
    time.sleep(2)
    ps_result = subprocess.run(["ps", "auxww"], capture_output=True, text=True)
    assert "karaf" in ps_result.stdout, "Karaf process not found after starting."
    try:
        karaf_server.kill()
    except:
        pass
