import subprocess
import requests
import pytest
import time

# ManageIQ runs on HTTPS by default.
MANAGEIQ_URL = "https://127.0.0.1"
CONTAINER_PROCESSES = ["dumb-init", "httpd", "crond", "memcached", "postgres"]


def test_manageiq_processes_running():
    """
    Test to check if all required ManageIQ processes are running inside the container.
    """
    print("Checking for running ManageIQ processes...")
    try:
        # The 'ps auxww' ww - wide output with unlimited width
        result = subprocess.run(["ps", "auxww"], stdout=subprocess.PIPE, text=True, check=True)
        running_processes_output = result.stdout

        for process in CONTAINER_PROCESSES:
            print(f"  - Verifying if '{process}' is running...")
            assert process in running_processes_output, f"Required process '{process}' not found."

        print("All required processes are running.")

    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run 'ps' command: {e}")
    except Exception as e:
        pytest.fail(f"An unexpected error occurred: {e}")


def test_manageiq_web_accessible(timeout=60):
    """
    Test to check if the ManageIQ web interface is accessible.
    It retries for a specified timeout as the application might take time to start.
    """
    print(f"Waiting for ManageIQ web interface to become accessible at {MANAGEIQ_URL}...")
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            # The 'verify=False' - self signed cert
            response = requests.get(MANAGEIQ_URL, verify=False)
            print("  - Received response from ManageIQ web interface. with code ", response.status_code)
            # A 200 OK response indicates the server is up and responding.
            assert response.status_code == 200, f"Web interface returned status code {response.status_code}."
            
            # Additional check to confirm it's a ManageIQ page.
            # Look for a specific string in the page title or content.
            assert "ManageIQ" in response.text, "Response body does not contain 'ManageIQ'."
            
            print("ManageIQ web interface is accessible.")
            return

        except requests.ConnectionError:
            # If a connection error occurs, we wait and retry.
            print("  - Connection failed. Retrying in 5 seconds...")
            time.sleep(5)
            
    pytest.fail(f"Failed to connect to ManageIQ web interface after {timeout} seconds.")
