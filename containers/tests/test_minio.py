import pytest
import subprocess
import requests
import time
import json
import os
import base64
import hashlib
from pathlib import Path
from xml.etree import ElementTree as ET

MINIO_HOST = "localhost"
MINIO_API_PORT = "9000"
MINIO_CONSOLE_PORT = "9001"
MINIO_API_URL = f"http://{MINIO_HOST}:{MINIO_API_PORT}"
MINIO_CONSOLE_URL = f"http://{MINIO_HOST}:{MINIO_CONSOLE_PORT}"

def test_minio_binary_installed():
    """Test that MinIO binary is installed and accessible."""
    assert os.path.isfile("/usr/local/bin/minio"), "MinIO binary not found at /usr/local/bin/minio"
    assert os.access("/usr/local/bin/minio", os.X_OK), "MinIO binary is not executable"

def test_minio_version():
    """Test that MinIO returns version information."""
    result = subprocess.run(['/usr/local/bin/minio', '--version'], 
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Failed to get MinIO version"
    assert "minio version" in result.stdout, f"Unexpected version output: {result.stdout}"

def test_minio_help():
    """Test that MinIO help command works."""
    result = subprocess.run(['/usr/local/bin/minio', '--help'], 
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Failed to get MinIO help"
    assert "server" in result.stdout, "Server command not found in help"
    assert "High Performance Object Storage" in result.stdout, "Expected help text not found"

def test_data_directory_exists():
    """Test that the data directory exists and has correct permissions."""
    data_dir = "/data"
    assert os.path.exists(data_dir), f"Data directory {data_dir} does not exist"
    assert os.path.isdir(data_dir), f"{data_dir} exists but is not a directory"

def test_license_files_exist():
    """Test that license files exist."""
    license_file = "/LICENSE"
    notice_file = "/NOTICE"
    
    assert os.path.exists(license_file), "LICENSE file not found"
    assert os.path.exists(notice_file), "NOTICE file not found"

def test_minio_server_help():
    """Test that MinIO server command shows help."""
    result = subprocess.run(['/usr/local/bin/minio', 'server', '--help'], 
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Failed to get MinIO server help"
    assert "--address" in result.stdout, "Address flag not found in help"
    assert "--console-address" in result.stdout, "Console address flag not found in help"

def test_minio_service_running():
    """Test that MinIO service is running and accessible."""
    max_retries = 15
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            response = requests.get(f"{MINIO_API_URL}/minio/health/live", timeout=5)
            if response.status_code == 200:
                return
        except requests.exceptions.RequestException:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                pytest.fail(f"Failed to connect to MinIO service after {max_retries} attempts")
    
    pytest.fail("MinIO service is not responding to health checks")

def test_minio_health_endpoints():
    """Test MinIO health endpoints."""
    # Test liveness probe
    try:
        response = requests.get(f"{MINIO_API_URL}/minio/health/live", timeout=10)
        assert response.status_code == 200, f"Liveness check failed with status {response.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to liveness endpoint: {e}")
    
    # Test readiness probe
    try:
        response = requests.get(f"{MINIO_API_URL}/minio/health/ready", timeout=10)
        assert response.status_code == 200, f"Readiness check failed with status {response.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to readiness endpoint: {e}")

def test_minio_console_accessible():
    """Test that MinIO console web interface is accessible."""
    try:
        response = requests.get(f"{MINIO_CONSOLE_URL}/", timeout=10)
        assert response.status_code == 200, f"Console failed with status {response.status_code}"
        
        # Check for basic HTML content
        content = response.text.lower()
        assert "<html" in content, "Response should be valid HTML"
        # Console should redirect or show login page
        assert "minio" in content or "login" in content, "Console should contain MinIO or login references"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to access MinIO console: {e}")

@pytest.mark.parametrize("endpoint", [
    "/minio/health/live",
    "/minio/health/ready",
    "/minio/v2/metrics/cluster"
])
def test_minio_operational_endpoints(endpoint):
    """Test various MinIO operational endpoints."""
    try:
        response = requests.get(f"{MINIO_API_URL}{endpoint}", timeout=10)
        # These endpoints should be accessible and return valid responses
        assert response.status_code in [200, 403], f"Endpoint {endpoint} failed with status {response.status_code}"
        
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to access endpoint {endpoint}: {e}")
