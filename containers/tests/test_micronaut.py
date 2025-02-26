import os
import subprocess
import pytest
import time
import socket

@pytest.fixture(scope="module", autouse=True)
def setup_environment():
    # Configure environment variables
    java_home = "/home/micronaut/.sdkman/candidates/java/current"
    os.environ["JAVA_HOME"] = java_home
    os.environ["PATH"] = f"{java_home}/bin:/home/micronaut/.sdkman/candidates/micronaut/current/bin:" + os.environ.get("PATH", "")
    
def is_port_open(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        return sock.connect_ex((host, port)) == 0

def test_micronaut_version():
    result = subprocess.run(["mn", "--version"], capture_output=True, text=True)
    assert result.returncode == 0, "Micronaut CLI command failed."
    assert "Micronaut" in result.stdout, "Micronaut CLI output is incorrect."

def test_micronaut_create_app():
    app_name = "test-app"
    subprocess.run(["rm", "-rf", app_name])

    result = subprocess.run(["mn", "create-app", app_name], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to create Micronaut application."
    assert app_name in os.listdir(), f"{app_name} directory not found."

    # Clean up
    subprocess.run(["rm", "-rf", app_name])

def test_micronaut_help():
    result = subprocess.run(["mn", "--help"], capture_output=True, text=True)
    assert result.returncode == 0, "Micronaut CLI help command failed."
    assert "Usage:" in result.stdout, "Micronaut CLI help output is incorrect."

def test_micronaut_test_command():
    app_name = "test-app"
    subprocess.run(["rm", "-rf", app_name])

    # Create application
    subprocess.run(["mn", "create-app", app_name], check=True)

    # Navigate to the app directory
    os.chdir(app_name)

    # Run tests within the application
    result = subprocess.run(["./gradlew", "test"], capture_output=True, text=True)
    assert result.returncode == 0, "Micronaut application tests failed."
    assert "BUILD SUCCESSFUL" in result.stdout, "Application tests did not complete successfully."

    # Navigate back and clean up
    os.chdir(".."); subprocess.run(["rm", "-rf", app_name])

def test_micronaut_run_command():
    app_name = "test-app"
    subprocess.run(["rm", "-rf", app_name])  # Clean up any previous app

    # Create application
    subprocess.run(["mn", "create-app", app_name], check=True)

    # Navigate to the app directory
    os.chdir(app_name)

    try:
        # Run the application in the background
        process = subprocess.Popen(["./gradlew", "run"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        time.sleep(60)
        for _ in range(20):
            if is_port_open("localhost", 8080):
                break
            time.sleep(10)
        else:
            pytest.fail("Micronaut application did not start on expected port.")

        assert process.poll() is None, "Micronaut application process terminated unexpectedly."
    finally:
        # Terminate the process if it is still running
        process.terminate()
        process.wait(timeout=10)

        # Navigate back and clean up
        os.chdir("..")
        subprocess.run(["rm", "-rf", app_name])
