import os
import pytest
import subprocess
import pwd

SENTINEL_PORT = "26379"
SENTINEL_USER = "redis"

def test_installation_files_exist():
    binaries = ['/usr/local/bin/redis-sentinel', '/usr/local/bin/redis-cli']
    for binary_path in binaries:
        assert os.path.isfile(binary_path), f"Binary not found: {binary_path}"
        assert os.access(binary_path, os.X_OK), f"Binary is not executable: {binary_path}"

    config_file = '/etc/redis/sentinel.conf'
    assert os.path.isfile(config_file), f"Config file not found: {config_file}"

def test_user_and_data_directory():
    data_dir = '/sentinel-data'
    assert os.path.isdir(data_dir)
    
    stat_info = os.stat(data_dir)
    owner_uid = stat_info.st_uid
    owner_user = pwd.getpwuid(owner_uid).pw_name
    assert owner_user == SENTINEL_USER

def test_sentinel_process_is_running():
    try:
        result = subprocess.run(['ps', 'auxww'], capture_output=True, text=True, check=True)
        assert "redis-sentinel" in result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        pytest.fail(f"Failed to check processes with 'ps auxww': {e}")

def test_sentinel_is_listening_on_port():
    try:
        result = subprocess.run(['ss', '-tuln'], capture_output=True, text=True, check=True)
        assert f":{SENTINEL_PORT}" in result.stdout
        assert "LISTEN" in result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        pytest.fail(f"Failed to check listening ports with 'ss': {e}")

def test_sentinel_responds_to_ping():
    command = ['redis-cli', '-p', SENTINEL_PORT, 'PING']
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True, timeout=10)
        assert "PONG" in result.stdout
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        pytest.fail(f"Command '{' '.join(command)}' failed: {e}")

def test_sentinel_info_command_returns_role_sentinel():
    command = ['redis-cli', '-p', SENTINEL_PORT, 'INFO']
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True, timeout=10)
        assert "redis_mode:sentinel" in result.stdout
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        pytest.fail(f"Command '{' '.join(command)}' failed: {e}")