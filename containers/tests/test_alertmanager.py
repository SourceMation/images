import pytest
import subprocess
import requests
import json
import time
import os
from pathlib import Path

def test_alertmanager_binary_exists():
    result = subprocess.run(['which', 'alertmanager'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Alertmanager binary not found in PATH."
    assert result.stdout.strip() == '/bin/alertmanager', f"Alertmanager binary found at unexpected location: {result.stdout.strip()}"

def test_amtool_binary_exists():
    result = subprocess.run(['which', 'amtool'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "amtool binary not found in PATH."
    assert result.stdout.strip() == '/bin/amtool', f"amtool binary found at unexpected location: {result.stdout.strip()}"

def test_alertmanager_version():
    result = subprocess.run(['alertmanager', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Failed to get Alertmanager version."
    assert "alertmanager, version 0.28.1" in result.stderr, f"Unexpected version output: {result.stderr}"

def test_amtool_version():
    result = subprocess.run(['amtool', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Failed to get amtool version."
    assert "amtool, version 0.28.1" in result.stderr, f"Unexpected version output: {result.stderr}"

def test_default_config_file_exists():
    config_path = '/etc/alertmanager/alertmanager.yml'
    assert os.path.exists(config_path), f"Default configuration file {config_path} does not exist."
    
    with open(config_path, 'r') as f:
        content = f.read()
        assert len(content) > 0, "Configuration file is empty."

def test_data_directory_exists():
    data_dir = '/alertmanager'
    assert os.path.exists(data_dir), f"Data directory {data_dir} does not exist."
    assert os.path.isdir(data_dir), f"{data_dir} exists but is not a directory."

def test_data_directory_permissions():
    data_dir = '/alertmanager'
    stat_info = os.stat(data_dir)
    
    # Check if directory is writable by group (nobody group)
    assert stat_info.st_mode & 0o020, f"Data directory {data_dir} is not writable by group."

def test_alertmanager_config_validation():
    """Test that the default configuration is valid"""
    result = subprocess.run([
        'alertmanager',
        '--config.file=/etc/alertmanager/alertmanager.yml',
        '--config.check'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    assert result.returncode == 0, f"Configuration validation failed: {result.stderr}"

def test_alertmanager_help():
    result = subprocess.run(['alertmanager', '--help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Failed to get Alertmanager help."
    assert "--config.file" in result.stdout, "Expected --config.file option not found in help output."
    assert "--storage.path" in result.stdout, "Expected --storage.path option not found in help output."

def test_amtool_help():
    result = subprocess.run(['amtool', '--help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Failed to get amtool help."
    assert "alert" in result.stdout or "silence" in result.stdout, "Expected amtool subcommands not found in help output."

def test_exposed_port_9093():
    """Test that port 9093 is the expected port for Alertmanager"""
    # Start alertmanager in background for a short time to test port binding
    process = subprocess.Popen([
        'alertmanager',
        '--config.file=/etc/alertmanager/alertmanager.yml',
        '--storage.path=/tmp/alertmanager-test',
        '--web.listen-address=:9093'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    try:
        # Give it a moment to start
        time.sleep(3)
        
        # Check if process is still running
        assert process.poll() is None, "Alertmanager process terminated unexpectedly"
        
        # Try to connect to the web interface
        try:
            response = requests.get('http://localhost:9093', timeout=5)
            # Alertmanager should return a response (even if it's a redirect or error page)
            assert response.status_code in [200, 302, 404], f"Unexpected status code: {response.status_code}"
        except requests.ConnectionError:
            pytest.fail("Could not connect to Alertmanager on port 9093")
        except requests.Timeout:
            pytest.fail("Timeout connecting to Alertmanager on port 9093")
            
    finally:
        # Clean up the process
        process.terminate()
        process.wait(timeout=10)

def test_alertmanager_api_endpoints():
    """Test that Alertmanager API endpoints are accessible"""
    process = subprocess.Popen([
        'alertmanager',
        '--config.file=/etc/alertmanager/alertmanager.yml',
        '--storage.path=/tmp/alertmanager-test-api',
        '--web.listen-address=:9093'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    try:
        # Give it time to start
        time.sleep(5)
        
        # Test API endpoints
        endpoints = [
            '/api/v1/status',
            '/api/v1/alerts',
            '/api/v1/silences'
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.get(f'http://localhost:9093{endpoint}', timeout=5)
                assert response.status_code == 200, f"API endpoint {endpoint} returned status {response.status_code}"
                
                # Verify JSON response
                data = response.json()
                assert 'status' in data, f"API endpoint {endpoint} did not return expected JSON structure"
                
            except requests.RequestException as e:
                pytest.fail(f"Failed to access API endpoint {endpoint}: {e}")
                
    finally:
        process.terminate()
        process.wait(timeout=10)

def test_amtool_config_show():
    """Test amtool can read and display configuration"""
    result = subprocess.run([
        'amtool',
        'config',
        'show',
        '--alertmanager.url=http://localhost:9093'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)
    
    # amtool might fail if alertmanager is not running, but it should not crash
    assert result.returncode in [0, 1], f"amtool config show failed unexpectedly: {result.stderr}"

def test_working_directory():
    """Test that the working directory is set correctly"""
    cwd = os.getcwd()
    assert cwd == '/alertmanager', f"Working directory is {cwd}, expected /alertmanager"

def test_user_permissions():
    """Test that the container runs as nobody user"""
    result = subprocess.run(['whoami'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Failed to get current user"
    current_user = result.stdout.strip()
    assert current_user == 'nobody', f"Container is running as {current_user}, expected nobody"

def test_alertmanager_storage_path():
    """Test that alertmanager can write to storage path"""
    test_storage = '/tmp/alertmanager-storage-test'
    os.makedirs(test_storage, exist_ok=True)
    
    process = subprocess.Popen([
        'alertmanager',
        '--config.file=/etc/alertmanager/alertmanager.yml',
        '--storage.path=' + test_storage,
        '--web.listen-address=:9094'  # Use different port to avoid conflicts
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    try:
        time.sleep(3)
        assert process.poll() is None, "Alertmanager failed to start with custom storage path"
        
        # Check if alertmanager created files in the storage directory
        storage_files = os.listdir(test_storage)
        assert len(storage_files) > 0, "Alertmanager did not create any files in storage directory"
        
    finally:
        process.terminate()
        process.wait(timeout=10)
        
        # Clean up
        import shutil
        shutil.rmtree(test_storage, ignore_errors=True)

@pytest.mark.parametrize("flag", [
    "--config.file",
    "--storage.path",
    "--web.listen-address",
    "--web.external-url",
    "--cluster.listen-address",
    "--log.level"
])
def test_alertmanager_command_line_flags(flag):
    """Test that important command line flags are recognized"""
    result = subprocess.run(['alertmanager', '--help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0
    assert flag in result.stdout, f"Command line flag {flag} not found in help output"
