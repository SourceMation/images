import pytest
import subprocess
import requests
import os
import json
from pathlib import Path

def test_alertmanager_binary_exists():
    assert os.path.isfile("/bin/alertmanager"), f"Binary not found: /bin/alertmanager"
    assert os.access("/bin/alertmanager", os.X_OK), f"Binary is not executable: /bin/alertmanager"

def test_amtool_binary_exists():
    assert os.path.isfile("/bin/amtool"), f"Binary not found: /bin/amtool"
    assert os.access("/bin/amtool", os.X_OK), f"Binary is not executable: /bin/amtool"

def test_alertmanager_version():
    result = subprocess.run(['alertmanager', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Failed to get Alertmanager version."
    assert "alertmanager, version 0.28.1" in result.stdout, f"Unexpected version output: {result.stdout}"

def test_amtool_version():
    result = subprocess.run(['amtool', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Failed to get amtool version."
    assert "amtool, version 0.28.1" in result.stdout, f"Unexpected version output: {result.stdout}"

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
    
    assert stat_info.st_mode & 0o020, f"Data directory {data_dir} is not writable by group."

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
    try:
        response = requests.get('http://localhost:9093/-/ready', timeout=5)
        assert response.status_code == 200, f"Unexpected status code for /-/ready: {response.status_code}"
    except requests.ConnectionError:
        pytest.fail("Could not connect to Alertmanager on port 9093")
    except requests.Timeout:
        pytest.fail("Timeout connecting to Alertmanager on port 9093")

def test_alertmanager_api_endpoints():
    endpoints = [
        '/api/v2/status',
        '/api/v2/alerts',
        '/api/v2/silences'
    ]
        
    for endpoint in endpoints:
        try:
            response = requests.get(f'http://localhost:9093{endpoint}', timeout=5)
            assert response.status_code == 200, f"API endpoint {endpoint} returned status {response.status_code}"
                
            data = response.json()

            if endpoint == '/api/v2/status':
                assert 'cluster' in data, "Response from /api/v2/status is missing 'cluster' key"
                assert 'versionInfo' in data, "Response from /api/v2/status is missing 'versionInfo' key"
                assert 'config' in data, "Response from /api/v2/status is missing 'config' key"
            
            elif endpoint in ['/api/v2/alerts', '/api/v2/silences']:
                assert isinstance(data, list), f"Response from {endpoint} should be a list, but was {type(data)}"
                
        except requests.RequestException as e:
            pytest.fail(f"Failed to access API endpoint {endpoint}: {e}")
        except json.JSONDecodeError:
            pytest.fail(f"Response from {endpoint} is not valid JSON.")
                

def test_amtool_config_show():
    result = subprocess.run([
        'amtool',
        'config',
        'show',
        '--alertmanager.url=http://localhost:9093'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)
    
    assert result.returncode in [0, 1], f"amtool config show failed unexpectedly: {result.stderr}"
        

@pytest.mark.parametrize("flag", [
    "--config.file",
    "--storage.path",
    "--web.listen-address",
    "--web.external-url",
    "--cluster.listen-address",
    "--log.level"
])
def test_alertmanager_command_line_flags(flag):
    result = subprocess.run(['alertmanager', '--help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0
    assert flag in result.stdout, f"Command line flag {flag} not found in help output"
