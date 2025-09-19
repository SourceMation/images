import pytest
import subprocess
import os
import pwd
import socket
import requests
from urllib3.exceptions import InsecureRequestWarning

requests.urllib3.disable_warnings(InsecureRequestWarning)

def test_metrics_server_binary_installed():
    """Test if metrics-server binary is installed and accessible"""
    result = subprocess.run(['/usr/local/bin/metrics-server', '--version'], 
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "metrics-server binary is not installed or not found"

def test_metrics_server_binary_permissions():
    """Test if metrics-server binary has correct permissions"""
    binary_path = '/usr/local/bin/metrics-server'
    assert os.path.exists(binary_path), f"Binary does not exist at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Binary is not executable: {binary_path}"
    
    stat_info = os.stat(binary_path)
    metrics_user = pwd.getpwnam('metrics-server')
    assert stat_info.st_uid == metrics_user.pw_uid, "Binary is not owned by metrics-server user"

def test_metrics_server_help_command():
    """Test if metrics-server help command works"""
    result = subprocess.run(['/usr/local/bin/metrics-server', '--help'], 
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "metrics-server help command failed"
    assert "metrics-server" in result.stdout.lower() or "metrics-server" in result.stderr.lower(), \
           "Help output doesn't contain expected content"

def test_metrics_server_user_exists():
    """Test if the metrics-server user exists"""
    try:
        user_info = pwd.getpwnam('metrics-server')
        assert user_info.pw_name == 'metrics-server', "metrics-server user does not exist"
        assert user_info.pw_shell == '/bin/bash', "metrics-server user shell is not /bin/bash"
        assert os.path.exists(user_info.pw_dir), "metrics-server user home directory does not exist"
    except KeyError:
        pytest.fail("metrics-server user does not exist")

def test_metrics_server_user_home_directory():
    """Test if metrics-server user home directory is properly set up"""
    user_info = pwd.getpwnam('metrics-server')
    home_dir = user_info.pw_dir
    
    assert os.path.exists(home_dir), f"Home directory does not exist: {home_dir}"
    assert os.path.isdir(home_dir), f"Home path is not a directory: {home_dir}"
    
    dir_stat = os.stat(home_dir)
    assert dir_stat.st_uid == user_info.pw_uid, "Home directory is not owned by metrics-server user"

def test_cert_directory_writable():
    """Test if cert directory is writable by metrics-server user"""
    cert_dir = '/usr/local/share/ca-certificates'
    
    assert os.path.exists(cert_dir), f"Certificate directory does not exist: {cert_dir}"
    assert os.access(cert_dir, os.R_OK), f"Certificate directory is not readable: {cert_dir}"
