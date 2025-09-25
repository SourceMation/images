import os
import pytest
import subprocess
import requests
import time

HUGO_SRC = "/src"
HUGO_PORT = 1313

def test_src_dir():
    assert os.path.isdir(HUGO_SRC)

def test_hugo_binary_exists_and_is_executable():
    binary_path = os.path.join('/usr', 'local', 'bin', 'hugo')
    assert os.path.isfile(binary_path), f"Binary not found: {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Binary is not executable: {binary_path}"

def test_hugo_environment():
    try:
        result = subprocess.run(['hugo', 'env'], capture_output=True, text=True, check=True)
        assert 'extended+withdeploy' in result.stdout, "Wrong hugo edition type detected"
        assert 'dart-sass' in result.stdout, "No dart-sass"
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        pytest.fail(f"Failed to execute 'hugo env': {e}")

def test_project_is_hosted_and_public_dir_created():
    result = subprocess.run(['hugo', 'new', 'site', HUGO_SRC], capture_output=True, text=True, check=True)
    with open(os.path.join(HUGO_SRC, "layouts", "index.html"), "w", encoding="utf8") as f:
        f.write("Hello, Hugo!")
    try:
        hugo_server = subprocess.Popen(["hugo", "server", "-s", HUGO_SRC], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        start = time.time()
        hugo_started = False
        while time.time() - start < 10:
            line = hugo_server.stdout.readline()
            if not line:
                break
            if "Web Server is available" in line:
                hugo_started = True
                break
        if not hugo_started:
            pytest.fail("Hugo server failed to start in desired time!")

        url = f"http://localhost:{HUGO_PORT}/"
        try:
            for _ in range(5):
                try:
                    response = requests.get(url, timeout=5)
                    if response.status_code == 200:
                        break
                except requests.ConnectionError:
                    time.sleep(1)
            else:
                pytest.fail("Hugo server did not become available.")

            assert response.status_code == 200
            assert "Hello, Hugo!" in response.text
        except requests.RequestException as e:
            pytest.fail(f"Failed to connect to Hugo server: {e}")

        assert os.path.isdir(os.path.join(HUGO_SRC, 'public')), "public dir has not been created"

    finally:
        if hugo_server:
            hugo_server.terminate()
