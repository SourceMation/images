import os
import pytest
import subprocess
import shutil
import socket

def test_os_release_is_debian_11():
    os_release_path = '/etc/os-release'
    assert os.path.exists(os_release_path), f"File {os_release_path} does not exist."

    release_info = {}
    with open(os_release_path, 'r') as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                release_info[key] = value.strip('"')

    assert release_info.get('ID') == 'debian'
    assert release_info.get('VERSION_ID') == '12'
    assert release_info.get('VERSION_CODENAME') == 'bookworm'
    assert release_info.get('PRETTY_NAME') == 'Debian GNU/Linux 12 (bookworm)'

def test_default_user_is_root():
    """
    Sprawdza, czy domyślnym użytkownikiem w kontenerze jest root.
    """
    try:
        result = subprocess.run(['whoami'], capture_output=True, text=True, check=True)
        current_user = result.stdout.strip()
        assert current_user == 'root'
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        pytest.fail(f"Could not verify user with 'whoami': {e}")

def test_apt_package_manager_exists():
    assert shutil.which('apt-get') is not None, "apt-get command not found in PATH."

def test_apt_get_update_works():
    try:
        subprocess.run(['apt-get', 'update'], check=True, capture_output=True, timeout=180)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"'apt-get update' failed with exit code {e.returncode}:\n{e.stderr}")
    except FileNotFoundError:
        pytest.fail("Command 'apt-get' not found in the container.")

def test_network_dns_and_tcp_connectivity():
    try:
        socket.create_connection(("debian.org", 80), timeout=10)
    except socket.gaierror:
        pytest.fail("DNS resolution failed. Could not resolve 'debian.org'.")
    except socket.timeout:
        pytest.fail("Connection timed out. A firewall might be blocking outbound traffic on port 80.")
    except OSError as e:
        pytest.fail(f"An OS error occurred during connection: {e}")

def test_path_variable_is_sane():
    path_var = os.environ.get('PATH')
    assert path_var is not None, "PATH environment variable is not set."
    
    expected_paths = ['/usr/local/sbin', '/usr/local/bin', '/usr/sbin', '/usr/bin', '/sbin', '/bin']
    for expected_path in expected_paths:
        assert expected_path in path_var.split(':')

@pytest.mark.parametrize("directory_path", ["/proc", "/sys", "/tmp", "/var/log", "/etc", "/root"])
def test_core_filesystem_directories_exist(directory_path):
    assert os.path.isdir(directory_path), f"Expected directory '{directory_path}' not found."

@pytest.mark.parametrize("path", ["/bin", "/sbin", "/lib"])
def test_merged_usr_filesystem_layout(path):
    assert os.path.islink(path), f"Path '{path}' is not a symlink as expected in Debian 12."
    
    target = os.readlink(path)
    expected_target = f"usr/{os.path.basename(path)}"
    assert target == expected_target, f"Symlink '{path}' points to '{target}', but expected 'usr/{os.path.basename(path)}'."

def test_openssl_version_is_3_0():
    try:
        result = subprocess.run(['openssl', 'version'], capture_output=True, text=True, check=True)
        version_output = result.stdout.strip()
        assert version_output.startswith('OpenSSL 3.0')
    except FileNotFoundError:
        pytest.fail("Command 'openssl' not found. Is the openssl package installed?")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"'openssl version' failed: {e.stderr}")