import os
import subprocess
import pytest
import time
import requests

QUARKUS_APP_DIR = "/home/quarkus"
QUARKUS_PORT = 8080

def test_add_jbang_trust():
    try:
        subprocess.run(
            ["jbang", "trust", "add", "https://repo1.maven.org/maven2/io/quarkus/quarkus-cli/"],
            check=True,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to add trust to jbang: {e}")

def test_quarkus_installed():
    result = subprocess.run(["quarkus", "--version"], capture_output=True, text=True)
    assert result.returncode == 0, "Quarkus is not installed."

def test_create_quarkus_app():
    result = subprocess.run(
        ["quarkus", "create", "app", "com.example.quarkus.test", "--output-directory", QUARKUS_APP_DIR],
        cwd=QUARKUS_APP_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "Failed to create Quarkus app."
    assert os.path.exists(os.path.join(QUARKUS_APP_DIR, "com.example.quarkus.test")), "Quarkus app directory not created."

def test_build_quarkus_app():
    app_dir = os.path.join(QUARKUS_APP_DIR, "com.example.quarkus.test")
    result = subprocess.run(
        ["./mvnw", "package", "-Dquarkus.package.type=uber-jar"],
        cwd=app_dir,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "Failed to build Quarkus app."
    assert os.path.exists(os.path.join(app_dir, "target", "com.example.quarkus.test-1.0.0-SNAPSHOT-runner.jar")), "JAR file not created."

@pytest.fixture(scope="module")
def run_quarkus_app():
    app_dir = os.path.join(QUARKUS_APP_DIR, "com.example.quarkus.test")
    process = subprocess.Popen(
        ["java", "-jar", "target/com.example.quarkus.test-1.0.0-SNAPSHOT-runner.jar"],
        cwd=app_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(5)
    yield process
    process.terminate()
    process.wait()

def test_quarkus_app_running(run_quarkus_app):
    url = f"http://localhost:{QUARKUS_PORT}/hello"
    response = requests.get(url)
    assert response.status_code == 200, f"Failed to access Quarkus app: {response.status_code}"
    assert "Hello" in response.text, "Unexpected response from Quarkus app."
