import os
import pytest
import subprocess
import requests
import time
import socket
import pwd

FLUENTD_CONFIG_DIR = "/etc/fluent"
FLUENTD_PORT = 24224
RUBY_PATH = "/opt/ruby/bin"


def test_config_directory_exists():
    """Test that the Fluentd configuration directory exists."""
    assert os.path.isdir(FLUENTD_CONFIG_DIR), f"Config directory {FLUENTD_CONFIG_DIR} does not exist"


def test_ruby_installation():
    """Test that Ruby is installed and accessible."""
    ruby_binary = os.path.join(RUBY_PATH, "ruby")
    assert os.path.isfile(ruby_binary), f"Ruby binary not found at {ruby_binary}"
    assert os.access(ruby_binary, os.X_OK), f"Ruby binary is not executable: {ruby_binary}"


def test_fluentd_binary_exists_and_is_executable():
    """Test that Fluentd binary is installed and executable."""
    fluentd_binary = os.path.join(RUBY_PATH, "fluentd")
    assert os.path.isfile(fluentd_binary), f"Fluentd binary not found at {fluentd_binary}"
    assert os.access(fluentd_binary, os.X_OK), f"Fluentd binary is not executable: {fluentd_binary}"


def test_fluentd_gem_installed():
    """Test that Fluentd gem is installed."""
    try:
        result = subprocess.run(
            ['gem', 'list', 'fluentd'],
            capture_output=True,
            text=True,
            check=True,
            timeout=10
        )
        assert 'fluentd' in result.stdout.lower(), "Fluentd gem is not installed"
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
        pytest.fail(f"Failed to check Fluentd gem installation: {e}")


def test_fluentd_version():
    """Test that Fluentd returns version information."""
    try:
        result = subprocess.run(
            ['fluentd', '--version'],
            capture_output=True,
            text=True,
            check=True,
            timeout=10
        )
        assert result.returncode == 0, "Failed to get Fluentd version"
        assert 'fluentd' in result.stdout.lower(), f"Unexpected version output: {result.stdout}"
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
        pytest.fail(f"Failed to execute 'fluentd --version': {e}")


def test_fluentd_help():
    """Test that Fluentd help command works."""
    try:
        result = subprocess.run(
            ['fluentd', '--help'],
            capture_output=True,
            text=True,
            check=True,
            timeout=10
        )
        assert result.returncode == 0, "Failed to get Fluentd help"
        assert '--config' in result.stdout or '-c' in result.stdout, "Config option not found in help"
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
        pytest.fail(f"Failed to execute 'fluentd --help': {e}")


def test_fluentd_process_is_running():
    """Test that the Fluentd process is running."""
    try:
        result = subprocess.run(
            ['ps', 'auxww'],
            capture_output=True,
            text=True,
            check=True,
            timeout=10
        )
        assert 'fluentd' in result.stdout, "Fluentd process not found in process list"
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
        pytest.fail(f"Failed to check processes with 'ps auxww': {e}")


def test_running_as_nobody_user():
    """Test that the container is running as the 'nobody' user."""
    current_user = pwd.getpwuid(os.getuid()).pw_name
    assert current_user == "nobody", f"Expected to run as 'nobody', but running as '{current_user}'"


def test_fluentd_is_listening_on_port():
    """Test that Fluentd is listening on port 24224."""
    max_retries = 20
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            result = subprocess.run(
                ['ss', '-tuln'],
                capture_output=True,
                text=True,
                check=True,
                timeout=10
            )
            if f":{FLUENTD_PORT}" in result.stdout and "LISTEN" in result.stdout:
                return
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        if attempt < max_retries - 1:
            print(f"Attempt {attempt + 1}/{max_retries}: Port {FLUENTD_PORT} not yet listening. Waiting...")
            time.sleep(retry_delay)
    
    pytest.fail(f"Port {FLUENTD_PORT} was not found in a 'LISTEN' state after {max_retries} attempts.")


def test_fluentd_accepts_tcp_connection():
    """Test that Fluentd accepts TCP connections on the forward port."""
    max_retries = 20
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex(('127.0.0.1', FLUENTD_PORT))
            sock.close()
            
            if result == 0:
                return
        except Exception as e:
            if attempt == max_retries - 1:
                pytest.fail(f"Failed to connect to Fluentd port: {e}")
        
        if attempt < max_retries - 1:
            print(f"Attempt {attempt + 1}/{max_retries}: Cannot connect to port {FLUENTD_PORT}. Waiting...")
            time.sleep(retry_delay)
    
    pytest.fail(f"Could not establish TCP connection to port {FLUENTD_PORT} after {max_retries} attempts.")


def test_required_libraries_installed():
    """Test that required system libraries are installed."""
    required_libs = [
        '/usr/lib/x86_64-linux-gnu/libssl.so.3',
        '/usr/lib/x86_64-linux-gnu/libyaml-0.so.2'
    ]
    
    for lib in required_libs:
        # Check if the library exists (could be symlink or actual file)
        lib_exists = os.path.exists(lib) or os.path.islink(lib)
        assert lib_exists, f"Required library not found: {lib}"


def test_fluentd_config_files_present():
    """Test that default Fluentd configuration files are present."""
    config_file = os.path.join(FLUENTD_CONFIG_DIR, "fluent.conf")
    assert os.path.isfile(config_file), f"Default config file not found: {config_file}"


def test_ruby_gem_command_available():
    """Test that gem command is available."""
    try:
        result = subprocess.run(
            ['gem', '--version'],
            capture_output=True,
            text=True,
            check=True,
            timeout=10
        )
        assert result.returncode == 0, "gem command failed"
        assert len(result.stdout.strip()) > 0, "gem version output is empty"
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
        pytest.fail(f"Failed to execute 'gem --version': {e}")


@pytest.mark.parametrize("command", ["ruby", "gem", "fluentd"])
def test_path_includes_ruby_bin(command):
    """Test that Ruby binaries are accessible via PATH."""
    try:
        result = subprocess.run(
            ['which', command],
            capture_output=True,
            text=True,
            check=True,
            timeout=10
        )
        assert result.returncode == 0, f"{command} not found in PATH"
        assert RUBY_PATH in result.stdout, f"{command} not found in expected Ruby path"
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
        pytest.fail(f"Failed to locate {command} in PATH: {e}")
