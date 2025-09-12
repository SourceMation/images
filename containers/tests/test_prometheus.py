import pytest
import subprocess
import requests
import time
import json
import os
from datetime import datetime, timedelta

PROMETHEUS_HOST = "localhost"
PROMETHEUS_PORT = "9090"
PROMETHEUS_URL = f"http://{PROMETHEUS_HOST}:{PROMETHEUS_PORT}"

def test_prometheus_binaries_installed():
    """Test that Prometheus and Promtool binaries are installed and accessible."""
    # Test prometheus binary
    result = subprocess.run(['/bin/prometheus', '--version'], 
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Prometheus binary is not installed or not found"
    assert "prometheus, version" in result.stdout, f"Unexpected output from prometheus --version: {result.stdout}"
    
    # Test promtool binary
    result = subprocess.run(['/bin/promtool', '--version'], 
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Promtool binary is not installed or not found"
    assert "promtool, version" in result.stdout, f"Unexpected output from promtool --version: {result.stdout}"

def test_prometheus_config_file_exists():
    """Test that the Prometheus configuration file exists."""
    config_path = "/etc/prometheus/prometheus.yml"
    assert os.path.exists(config_path), f"Prometheus config file not found at {config_path}"
    
    # Validate config file with promtool
    result = subprocess.run(['/bin/promtool', 'check', 'config', config_path], 
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, f"Invalid Prometheus configuration: {result.stderr}"
    assert "SUCCESS" in result.stdout, f"Configuration validation failed: {result.stdout}"

def test_prometheus_service_running():
    """Test that Prometheus service is running and accessible."""
    try:
        response = requests.get(f"{PROMETHEUS_URL}/-/healthy", timeout=10)
        assert response.status_code == 200, f"Prometheus health check failed with status {response.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Prometheus service: {e}")

def test_prometheus_ready_endpoint():
    """Test that Prometheus ready endpoint responds correctly."""
    try:
        response = requests.get(f"{PROMETHEUS_URL}/-/ready", timeout=10)
        assert response.status_code == 200, f"Prometheus ready check failed with status {response.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Prometheus ready endpoint: {e}")

def test_prometheus_api_version():
    """Test that Prometheus API version endpoint is accessible."""
    try:
        response = requests.get(f"{PROMETHEUS_URL}/api/v1/status/buildinfo", timeout=10)
        assert response.status_code == 200, f"API version endpoint failed with status {response.status_code}"
        
        data = response.json()
        assert data["status"] == "success", f"API returned error status: {data}"
        assert "version" in data["data"], "Build info should contain version information"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Prometheus API: {e}")
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse JSON response: {e}")

def test_prometheus_metrics_endpoint():
    """Test that Prometheus exposes its own metrics."""
    try:
        response = requests.get(f"{PROMETHEUS_URL}/metrics", timeout=10)
        assert response.status_code == 200, f"Metrics endpoint failed with status {response.status_code}"
        
        metrics_text = response.text
        assert "prometheus_build_info" in metrics_text, "Prometheus build info metric not found"
        assert "prometheus_config_last_reload_successful" in metrics_text, "Config reload metric not found"
        assert "up" in metrics_text, "Basic 'up' metric not found"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Prometheus metrics endpoint: {e}")

def test_prometheus_targets_endpoint():
    """Test that Prometheus targets endpoint is accessible."""
    try:
        response = requests.get(f"{PROMETHEUS_URL}/api/v1/targets", timeout=10)
        assert response.status_code == 200, f"Targets endpoint failed with status {response.status_code}"
        
        data = response.json()
        assert data["status"] == "success", f"Targets API returned error: {data}"
        assert "activeTargets" in data["data"], "Targets response should contain activeTargets"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Prometheus targets endpoint: {e}")
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse JSON response: {e}")

def test_prometheus_query_endpoint():
    """Test that Prometheus query endpoint works with a basic query."""
    try:
        # Query for Prometheus up metric
        params = {"query": "up"}
        response = requests.get(f"{PROMETHEUS_URL}/api/v1/query", params=params, timeout=10)
        assert response.status_code == 200, f"Query endpoint failed with status {response.status_code}"
        
        data = response.json()
        assert data["status"] == "success", f"Query returned error: {data}"
        assert "result" in data["data"], "Query response should contain result data"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to query Prometheus: {e}")
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse JSON response: {e}")

def test_prometheus_query_range_endpoint():
    """Test that Prometheus range query endpoint works."""
    try:
        # Query range for the last 5 minutes
        end_time = datetime.now()
        start_time = end_time - timedelta(minutes=5)
        
        params = {
            "query": "up",
            "start": start_time.isoformat() + "Z",
            "end": end_time.isoformat() + "Z",
            "step": "15s"
        }
        
        response = requests.get(f"{PROMETHEUS_URL}/api/v1/query_range", params=params, timeout=10)
        assert response.status_code == 200, f"Range query endpoint failed with status {response.status_code}"
        
        data = response.json()
        assert data["status"] == "success", f"Range query returned error: {data}"
        assert "result" in data["data"], "Range query response should contain result data"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to perform range query on Prometheus: {e}")
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse JSON response: {e}")

def test_prometheus_config_reload():
    """Test that Prometheus configuration can be reloaded."""
    try:
        # Send reload signal
        response = requests.post(f"{PROMETHEUS_URL}/-/reload", timeout=10)
        assert response.status_code == 200, f"Config reload failed with status {response.status_code}"
        
        # Wait a moment for reload to complete
        time.sleep(2)
        
        # Verify service is still healthy after reload
        response = requests.get(f"{PROMETHEUS_URL}/-/healthy", timeout=10)
        assert response.status_code == 200, "Prometheus not healthy after config reload"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to reload Prometheus configuration: {e}")

def test_prometheus_tsdb_status():
    """Test that Prometheus TSDB status endpoint is accessible."""
    try:
        response = requests.get(f"{PROMETHEUS_URL}/api/v1/status/tsdb", timeout=10)
        assert response.status_code == 200, f"TSDB status endpoint failed with status {response.status_code}"
        
        data = response.json()
        assert data["status"] == "success", f"TSDB status returned error: {data}"
        assert "headStats" in data["data"], "TSDB status should contain head statistics"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to get TSDB status: {e}")
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse JSON response: {e}")

def test_promtool_config_validation():
    """Test that promtool can validate the configuration file."""
    config_path = "/etc/prometheus/prometheus.yml"
    result = subprocess.run(['/bin/promtool', 'check', 'config', config_path], 
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    assert result.returncode == 0, f"Configuration validation failed: {result.stderr}"
    assert "SUCCESS" in result.stdout, f"Expected SUCCESS message not found: {result.stdout}"

def test_prometheus_web_ui():
    """Test that Prometheus web UI is accessible."""
    try:
        response = requests.get(f"{PROMETHEUS_URL}/graph", timeout=10)
        assert response.status_code == 200, f"Web UI failed with status {response.status_code}"
        
        # Check for basic HTML content that indicates the UI loaded
        content = response.text.lower()
        assert "prometheus" in content, "Web UI should contain 'Prometheus' text"
        assert "<html" in content, "Response should be valid HTML"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to access Prometheus web UI: {e}")

def test_prometheus_storage_permissions():
    """Test that the storage directory has correct permissions."""
    storage_path = "/prometheus"
    
    # Check if directory exists
    assert os.path.exists(storage_path), f"Storage directory {storage_path} does not exist"
    
    # Check if directory is writable (this test assumes running as nobody user)
    stat_info = os.stat(storage_path)
    # Check group write permission (bit 5)
    group_write = bool(stat_info.st_mode & 0o020)
    assert group_write, f"Storage directory {storage_path} should have group write permission"

def test_prometheus_labels_endpoint():
    """Test that Prometheus labels endpoint works."""
    try:
        response = requests.get(f"{PROMETHEUS_URL}/api/v1/labels", timeout=10)
        assert response.status_code == 200, f"Labels endpoint failed with status {response.status_code}"
        
        data = response.json()
        assert data["status"] == "success", f"Labels API returned error: {data}"
        assert isinstance(data["data"], list), "Labels response should contain a list of labels"
        
        # Should at least contain some basic labels
        labels = data["data"]
        assert "__name__" in labels, "Labels should contain the '__name__' label"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to get labels from Prometheus: {e}")
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse JSON response: {e}")

def test_prometheus_series_endpoint():
    """Test that Prometheus series endpoint works."""
    try:
        # Get series for 'up' metric
        params = {"match[]": "up"}
        response = requests.get(f"{PROMETHEUS_URL}/api/v1/series", params=params, timeout=10)
        assert response.status_code == 200, f"Series endpoint failed with status {response.status_code}"
        
        data = response.json()
        assert data["status"] == "success", f"Series API returned error: {data}"
        assert isinstance(data["data"], list), "Series response should contain a list"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to get series from Prometheus: {e}")
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse JSON response: {e}")
