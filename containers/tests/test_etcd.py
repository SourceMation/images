import pytest
import subprocess
import requests
import time
import json
import os
from pathlib import Path

ETCD_HOST = "localhost"
ETCD_CLIENT_PORT = "2379"
ETCD_PEER_PORT = "2380"
ETCD_CLIENT_URL = f"http://{ETCD_HOST}:{ETCD_CLIENT_PORT}"

def test_etcd_binaries_installed():
    """Test that etcd, etcdctl, and etcdutl binaries are installed and accessible."""
    binaries = ["/usr/local/bin/etcd", "/usr/local/bin/etcdctl", "/usr/local/bin/etcdutl"]
    
    for binary in binaries:
        assert os.path.isfile(binary), f"Binary not found: {binary}"
        assert os.access(binary, os.X_OK), f"Binary is not executable: {binary}"

def test_etcd_version():
    """Test that etcd returns version information."""
    result = subprocess.run(['/usr/local/bin/etcd', '--version'], 
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Failed to get etcd version"
    assert "etcd Version:" in result.stdout, f"Unexpected version output: {result.stdout}"

def test_etcdctl_version():
    """Test that etcdctl returns version information."""
    result = subprocess.run(['/usr/local/bin/etcdctl', 'version'], 
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Failed to get etcdctl version"
    assert "etcdctl version:" in result.stdout, f"Unexpected version output: {result.stdout}"
    assert "API version:" in result.stdout, f"API version not found in output: {result.stdout}"

def test_etcdutl_version():
    """Test that etcdutl returns version information."""
    result = subprocess.run(['/usr/local/bin/etcdutl', 'version'], 
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Failed to get etcdutl version"
    assert "etcdutl version:" in result.stdout, f"Unexpected version output: {result.stdout}"

def test_data_directories_exist():
    """Test that required data directories exist."""
    directories = ["/var/lib/etcd", "/var/etcd"]
    
    for directory in directories:
        assert os.path.exists(directory), f"Data directory {directory} does not exist"
        assert os.path.isdir(directory), f"{directory} exists but is not a directory"

def test_data_directories_permissions():
    """Test that data directories have correct permissions for nobody user."""
    directories = ["/var/lib/etcd", "/var/etcd"]
    
    for directory in directories:
        stat_info = os.stat(directory)
        # Check that the directory is accessible (readable and executable for others or group)
        others_access = stat_info.st_mode & 0o005  # read and execute for others
        group_access = stat_info.st_mode & 0o050   # read and execute for group
        assert others_access or group_access, f"Data directory {directory} is not accessible by nobody user"

def test_etcd_service_running():
    """Test that etcd service is running and accessible."""
    max_retries = 10
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            response = requests.get(f"{ETCD_CLIENT_URL}/health", timeout=5)
            if response.status_code == 200:
                return
        except requests.exceptions.RequestException:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                pytest.fail(f"Failed to connect to etcd service after {max_retries} attempts")
    
    pytest.fail("etcd service is not responding to health checks")

def test_etcd_health_endpoint():
    """Test that etcd health endpoint responds correctly."""
    try:
        response = requests.get(f"{ETCD_CLIENT_URL}/health", timeout=10)
        assert response.status_code == 200, f"Health check failed with status {response.status_code}"
        
        data = response.json()
        assert "health" in data, "Health response should contain 'health' field"
        assert data["health"] == "true", f"etcd reports unhealthy: {data}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to etcd health endpoint: {e}")
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse JSON response from health endpoint: {e}")

def test_etcd_version_endpoint():
    """Test that etcd version endpoint is accessible."""
    try:
        response = requests.get(f"{ETCD_CLIENT_URL}/version", timeout=10)
        assert response.status_code == 200, f"Version endpoint failed with status {response.status_code}"
        
        data = response.json()
        assert "etcdserver" in data, "Version response should contain etcdserver information"
        assert "etcdcluster" in data, "Version response should contain etcdcluster information"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to etcd version endpoint: {e}")
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse JSON response from version endpoint: {e}")

def test_etcd_metrics_endpoint():
    """Test that etcd exposes metrics."""
    try:
        response = requests.get(f"{ETCD_CLIENT_URL}/metrics", timeout=10)
        assert response.status_code == 200, f"Metrics endpoint failed with status {response.status_code}"
        
        metrics_text = response.text
        assert "etcd_server_has_leader" in metrics_text, "Leader metric not found"
        assert "etcd_server_leader_changes_seen_total" in metrics_text, "Leader changes metric not found"
        assert "etcd_disk_wal_fsync_duration_seconds" in metrics_text, "WAL fsync duration metric not found"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to etcd metrics endpoint: {e}")

def test_etcdctl_basic_operations():
    """Test basic etcdctl operations like put and get."""
    endpoint = f"--endpoints={ETCD_CLIENT_URL}"
    
    # Test put operation
    result = subprocess.run([
        '/usr/local/bin/etcdctl', endpoint, 'put', 'test_key', 'test_value'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)
    
    assert result.returncode == 0, f"etcdctl put failed: {result.stderr}"
    assert "OK" in result.stdout, f"Unexpected put response: {result.stdout}"
    
    # Test get operation
    result = subprocess.run([
        '/usr/local/bin/etcdctl', endpoint, 'get', 'test_key'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)
    
    assert result.returncode == 0, f"etcdctl get failed: {result.stderr}"
    assert "test_key" in result.stdout, "Key not found in get response"
    assert "test_value" in result.stdout, "Value not found in get response"

def test_etcdctl_endpoint_health():
    """Test etcdctl endpoint health command."""
    result = subprocess.run([
        '/usr/local/bin/etcdctl', f'--endpoints={ETCD_CLIENT_URL}', 'endpoint', 'health'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)
    
    assert result.returncode == 0, f"etcdctl endpoint health failed: {result.stderr}"
    assert "is healthy" in result.stdout, f"Unexpected health response: {result.stdout}"

def test_etcdctl_endpoint_status():
    """Test etcdctl endpoint status command."""
    result = subprocess.run([
        '/usr/local/bin/etcdctl', f'--endpoints={ETCD_CLIENT_URL}', 'endpoint', 'status'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)
    
    assert result.returncode == 0, f"etcdctl endpoint status failed: {result.stderr}"
    assert ETCD_CLIENT_URL in result.stdout, "Endpoint URL not found in status output"

def test_etcdctl_member_list():
    """Test etcdctl member list command."""
    result = subprocess.run([
        '/usr/local/bin/etcdctl', f'--endpoints={ETCD_CLIENT_URL}', 'member', 'list'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)
    
    assert result.returncode == 0, f"etcdctl member list failed: {result.stderr}"
    # Should contain at least one member in the output
    assert len(result.stdout.strip()) > 0, "Member list should not be empty"

def test_etcd_v3_api():
    """Test that etcd v3 API is accessible through HTTP."""
    try:
        # Test keys endpoint with v3 API
        headers = {'Content-Type': 'application/json'}
        data = {
            "key": "dGVzdF9rZXk=",  # base64 encoded "test_key"
        }
        
        response = requests.post(f"{ETCD_CLIENT_URL}/v3/kv/range", 
                               json=data, headers=headers, timeout=10)
        
        # Should get 200 or 404, both indicate API is working
        assert response.status_code in [200, 404], f"V3 API failed with status {response.status_code}"
        
        # Should be valid JSON
        response.json()
        
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to etcd v3 API: {e}")
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse JSON response from v3 API: {e}")

def test_etcd_snapshot_operations():
    """Test etcdctl snapshot operations."""
    endpoint = f"--endpoints={ETCD_CLIENT_URL}"
    snapshot_path = "/tmp/test_snapshot.db"
    
    try:
        # Create a test key before snapshot
        subprocess.run([
            '/usr/local/bin/etcdctl', endpoint, 'put', 'snapshot_test', 'snapshot_value'
        ], check=True, timeout=10)
        
        # Create snapshot
        result = subprocess.run([
            '/usr/local/bin/etcdctl', endpoint, 'snapshot', 'save', snapshot_path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30)
        
        assert result.returncode == 0, f"etcdctl snapshot save failed: {result.stderr}"
        assert os.path.exists(snapshot_path), "Snapshot file was not created"
        
        # Test snapshot status using etcdutl
        result = subprocess.run([
            '/usr/local/bin/etcdutl', 'snapshot', 'status', snapshot_path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)
        
        assert result.returncode == 0, f"etcdutl snapshot status failed: {result.stderr}"
        
    finally:
        # Clean up snapshot file
        if os.path.exists(snapshot_path):
            os.remove(snapshot_path)

def test_etcd_workdir():
    """Test that etcd working directory is set correctly."""
    # The Dockerfile sets WORKDIR to /var/etcd/ and /var/lib/etcd/
    # We'll check that these directories exist and are accessible
    working_dirs = ["/var/etcd", "/var/lib/etcd"]
    
    for workdir in working_dirs:
        assert os.path.exists(workdir), f"Working directory {workdir} does not exist"
        assert os.path.isdir(workdir), f"Working directory {workdir} is not a directory"

@pytest.mark.parametrize("flag", [
    "--name",
    "--data-dir", 
    "--listen-client-urls",
    "--advertise-client-urls",
    "--listen-peer-urls",
    "--initial-advertise-peer-urls",
    "--initial-cluster",
    "--initial-cluster-token",
    "--initial-cluster-state"
])
def test_etcd_command_line_flags(flag):
    """Test that etcd supports expected command line flags."""
    result = subprocess.run(['/usr/local/bin/etcd', '--help'], 
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0
    help_output = result.stdout + result.stderr  # Some help might go to stderr
    assert flag in help_output, f"Command line flag {flag} not found in help output"

def test_etcd_lease_operations():
    """Test etcd lease operations."""
    endpoint = f"--endpoints={ETCD_CLIENT_URL}"
    
    try:
        # Grant a lease
        result = subprocess.run([
            '/usr/local/bin/etcdctl', endpoint, 'lease', 'grant', '60'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)
        
        assert result.returncode == 0, f"etcdctl lease grant failed: {result.stderr}"
        assert "lease" in result.stdout, "Lease ID not found in grant response"
        
        # Extract lease ID (format: "lease <ID> granted with TTL(60s)")
        import re
        lease_match = re.search(r'lease (\w+) granted', result.stdout)
        assert lease_match, f"Could not extract lease ID from: {result.stdout}"
        lease_id = lease_match.group(1)
        
        # List leases
        result = subprocess.run([
            '/usr/local/bin/etcdctl', endpoint, 'lease', 'list'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)
        
        assert result.returncode == 0, f"etcdctl lease list failed: {result.stderr}"
        assert lease_id in result.stdout, f"Lease {lease_id} not found in lease list"
        
    except subprocess.TimeoutExpired:
        pytest.fail("Lease operations timed out")
    except Exception as e:
        pytest.fail(f"Lease operations failed: {e}")

def test_etcd_auth_status():
    """Test etcd auth status (should be disabled by default)."""
    endpoint = f"--endpoints={ETCD_CLIENT_URL}"
    
    result = subprocess.run([
        '/usr/local/bin/etcdctl', endpoint, 'auth', 'status'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)
    
    # Auth status command should succeed
    assert result.returncode == 0, f"etcdctl auth status failed: {result.stderr}"
    # By default, authentication should be disabled
    assert "Authentication Status: false" in result.stdout or "false" in result.stdout.lower(), \
        f"Expected authentication to be disabled by default: {result.stdout}"
