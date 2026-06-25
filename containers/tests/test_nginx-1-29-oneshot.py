import pytest
import subprocess
import requests
import os


def test_nginx_installed():
    result = subprocess.run(['nginx', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Nginx is not installed or nginx command is not found."
    assert "nginx version:" in result.stderr, f"Nginx version output does not contain expected string. Output: {result.stderr}"


def test_nginx_process_running():
    try:
        # Check if nginx process is running with the specified arguments
        result = subprocess.run(['pgrep', '-f', 'nginx -g daemon off;'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        assert len(result.stdout.strip().splitlines()) >= 1, "Nginx process with 'nginx -g daemon off;' not found."
    except FileNotFoundError:
        pytest.skip("pgrep command not found. Cannot verify running process.")


def test_nginx_listening_on_port_80():
    try:
        # Check if nginx is listening on port 80
        result = subprocess.run(['ss', '-tuln'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        assert 'tcp' in result.stdout
        assert ':80' in result.stdout, "Nginx is not listening on port 80."
    except FileNotFoundError:
        pytest.skip("ss command not found. Cannot verify listening ports.")


def test_nginx_default_page_responds():
    try:
        response = requests.get("http://localhost:80", timeout=1)
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}."
        assert "Welcome to nginx!" in response.text, "Default nginx page content not found."
    except requests.exceptions.ConnectionError:
        pytest.fail("Failed to connect to nginx on port 80.")
    except requests.exceptions.Timeout:
        pytest.fail("Connection to nginx on port 80 timed out.")


def test_docker_entrypoint_files_exist():
    files_to_check = [
        '/docker-entrypoint.sh',
        '/docker-entrypoint.d/10-listen-on-ipv6-by-default.sh',
        '/docker-entrypoint.d/15-local-resolvers.envsh',
        '/docker-entrypoint.d/20-envsubst-on-templates.sh',
        '/docker-entrypoint.d/30-tune-worker-processes.sh'
    ]
    for file_path in files_to_check:
        assert os.path.exists(file_path), f"File not found: {file_path}"
