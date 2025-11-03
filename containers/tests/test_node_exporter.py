import pytest
import subprocess
import requests
import os
import json
from pathlib import Path

def test_node_exporter_binary_exists():
    assert os.path.isfile("/usr/local/bin/node_exporter"), f"Binary not found: /usr/local/bin/node_exporter"
    assert os.access("/usr/local/bin/node_exporter", os.X_OK), f"Binary is not executable: /usr/local/bin/node_exporter"

def test_node_exporter_help():
    result = subprocess.run(['node_exporter', '--help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Failed to get Node Exporter help."
    assert "--web.listen-address" in result.stdout, "Expected --web.listen-address option not found in help output."
    assert "--collector." in result.stdout, "Expected collector options not found in help output."

def test_exposed_port_9100():
    try:
        response = requests.get('http://localhost:9100/', timeout=5)
        assert response.status_code == 200, f"Unexpected status code for /: {response.status_code}"
        assert "Node Exporter" in response.text, "Expected 'Node Exporter' not found in response"
    except requests.ConnectionError:
        pytest.fail("Could not connect to Node Exporter on port 9100")
    except requests.Timeout:
        pytest.fail("Timeout connecting to Node Exporter on port 9100")

def test_metrics_endpoint():
    try:
        response = requests.get('http://localhost:9100/metrics', timeout=10)
        assert response.status_code == 200, f"Metrics endpoint returned status {response.status_code}"
        
        metrics_text = response.text
        
        # Check for common metrics that should always be present
        essential_metrics = [
            'node_cpu_seconds_total',
            'node_memory_MemTotal_bytes',
            'node_load1',
            'node_filesystem_size_bytes',
            'node_network_receive_bytes_total',
            'node_boot_time_seconds'
        ]
        
        for metric in essential_metrics:
            assert metric in metrics_text, f"Essential metric {metric} not found in metrics output"
            
        # Verify HELP and TYPE annotations
        assert '# HELP' in metrics_text, "No HELP annotations found in metrics"
        assert '# TYPE' in metrics_text, "No TYPE annotations found in metrics"
        
        # Check that metrics have actual values (not just definitions)
        lines_with_values = [line for line in metrics_text.split('\n') 
                           if line and not line.startswith('#') and ' ' in line]
        assert len(lines_with_values) > 50, f"Expected more than 50 metric lines, got {len(lines_with_values)}"
        
    except requests.RequestException as e:
        pytest.fail(f"Failed to access metrics endpoint: {e}")

def test_default_collectors_enabled():
    try:
        response = requests.get('http://localhost:9100/metrics', timeout=10)
        assert response.status_code == 200
        
        metrics_text = response.text
        
        # Test for metrics from key default collectors
        default_collectors_metrics = {
            'cpu': 'node_cpu_seconds_total',
            'meminfo': 'node_memory_MemTotal_bytes',
            'filesystem': 'node_filesystem_size_bytes',
            'netdev': 'node_network_receive_bytes_total',
            'loadavg': 'node_load1',
            'diskstats': 'node_disk_reads_completed_total',
            'time': 'node_time_seconds',
            'uname': 'node_uname_info'
        }
        
        for collector, metric in default_collectors_metrics.items():
            assert metric in metrics_text, f"Metric {metric} from collector {collector} not found"
            
    except requests.RequestException as e:
        pytest.fail(f"Failed to test default collectors: {e}")

def test_node_exporter_process_metrics():
    try:
        response = requests.get('http://localhost:9100/metrics', timeout=10)
        assert response.status_code == 200
        
        metrics_text = response.text
        
        # Check for Go runtime metrics (internal to node_exporter)
        go_metrics = [
            'go_goroutines',
            'go_memstats_alloc_bytes',
            'process_cpu_seconds_total',
            'process_resident_memory_bytes'
        ]
        
        for metric in go_metrics:
            assert metric in metrics_text, f"Go runtime metric {metric} not found"
            
    except requests.RequestException as e:
        pytest.fail(f"Failed to test process metrics: {e}")

@pytest.mark.parametrize("flag", [
    "--web.listen-address",
    "--web.telemetry-path",
    "--path.rootfs",
    "--[no-]collector.disable-defaults",
    "--log.level"
])
def test_node_exporter_command_line_flags(flag):
    result = subprocess.run(['node_exporter', '--help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0
    assert flag in result.stdout, f"Command line flag {flag} not found in help output"

@pytest.mark.parametrize("collector", [
    "arp", "cpu", "diskstats", "edac", "entropy", 
    "filefd", "filesystem", "hwmon", "loadavg", "mdadm", 
    "meminfo", "netdev", "netstat", "stat", "time", "uname", "vmstat"
])
def test_collector_flags_available(collector):
    result = subprocess.run(['node_exporter', '--help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0
    collector_flag = f"--collector.{collector}"
    no_collector_flag = f"--[no-]collector.{collector}"
    
    # At least one of the flags should be present
    assert (collector_flag in result.stdout or no_collector_flag in result.stdout), \
           f"Neither {collector_flag} nor {no_collector_flag} found in help output"

def test_metric_families_structure():
    try:
        response = requests.get('http://localhost:9100/metrics', timeout=10)
        assert response.status_code == 200
        
        metrics_text = response.text
        lines = metrics_text.split('\n')
        
        help_lines = [line for line in lines if line.startswith('# HELP')]
        type_lines = [line for line in lines if line.startswith('# TYPE')]
        
        # Should have both HELP and TYPE annotations
        assert len(help_lines) > 20, f"Expected more than 20 HELP lines, got {len(help_lines)}"
        assert len(type_lines) > 20, f"Expected more than 20 TYPE lines, got {len(type_lines)}"
        
        # Check for valid metric types
        valid_types = ['counter', 'gauge', 'histogram', 'summary', 'info', 'stateset', 'untyped']
        for line in type_lines:
            parts = line.split()
            if len(parts) >= 4:  # # TYPE metric_name type
                metric_type = parts[3]
                assert metric_type in valid_types, f"Invalid metric type {metric_type} found"
                
    except requests.RequestException as e:
        pytest.fail(f"Failed to test metric families: {e}")

def test_license_file_exists():
    license_path = '/LICENSE'
    assert os.path.exists(license_path), f"License file {license_path} does not exist."
    
    with open(license_path, 'r') as f:
        content = f.read()
        assert len(content) > 0, "License file is empty."
        assert "Apache" in content, "License file doesn't appear to contain Apache license text."

def test_node_exporter_startup_without_errors():
    # Test that node_exporter can start with basic flags
    result = subprocess.run([
        'timeout', '5s', 'node_exporter', 
        '--web.listen-address=:9101',  # Use different port to avoid conflicts
        '--log.level=debug'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Should exit due to timeout (signal 124) or start successfully
    assert result.returncode in [0, 124], f"node_exporter failed to start: {result.stderr}"
    
    # Check that there are no fatal errors in the output
    stderr_lower = result.stderr.lower()
    assert "fatal" not in stderr_lower, f"Fatal error found in startup: {result.stderr}"
    assert "panic" not in stderr_lower, f"Panic found in startup: {result.stderr}"

def test_specific_collector_disable():
    # Test disabling a specific collector
    result = subprocess.run([
        'timeout', '3s', 'node_exporter',
        '--web.listen-address=:9102',
        '--no-collector.arp',
        '--log.level=info'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    assert result.returncode in [0, 124], f"node_exporter with disabled collector failed: {result.stderr}"
    
    # Should not contain errors about the disabled collector
    assert "error" not in result.stderr.lower() or "arp" not in result.stderr.lower(), \
           f"Error related to disabled arp collector: {result.stderr}"

def test_filesystem_metrics_present():
    try:
        response = requests.get('http://localhost:9100/metrics', timeout=10)
        assert response.status_code == 200
        
        metrics_text = response.text
        
        # Test for essential filesystem metrics
        filesystem_metrics = [
            'node_filesystem_size_bytes',
            'node_filesystem_free_bytes',
            'node_filesystem_avail_bytes',
            'node_filesystem_files',
            'node_filesystem_files_free'
        ]
        
        for metric in filesystem_metrics:
            assert metric in metrics_text, f"Filesystem metric {metric} not found"
            
        # Should have metrics for at least root filesystem
        assert 'device="/' in metrics_text or 'mountpoint="/"' in metrics_text, \
               "No metrics found for root filesystem"
               
    except requests.RequestException as e:
        pytest.fail(f"Failed to test filesystem metrics: {e}")
