import os
import pytest
import subprocess
import shutil
import socket

def test_os_release_is_rocky_9():
    os_release_path = '/etc/os-release'
    assert os.path.exists(os_release_path), f"File {os_release_path} does not exist."

    release_info = {}
    with open(os_release_path, 'r') as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                release_info[key] = value.strip('"')

    assert release_info.get('ID') == 'rocky'
    assert release_info.get('VERSION_ID').startswith('9')
    assert "Rocky Linux 9" in release_info.get('PRETTY_NAME')

def test_redhat_release_file_is_correct():
    release_file = '/etc/redhat-release'
    assert os.path.exists(release_file)
    with open(release_file, 'r') as f:
        content = f.read()
        assert content.strip().startswith("Rocky Linux release 9")

def test_default_user_is_root():
    try:
        result = subprocess.run(['whoami'], capture_output=True, text=True, check=True)
        assert result.stdout.strip() == 'root'
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        pytest.fail(f"Could not verify user with 'whoami': {e}")

def test_dnf_package_manager_exists():
    assert shutil.which('dnf') is not None, "dnf command not found in PATH."

def test_dnf_can_check_updates():
    try:
        result = subprocess.run(['dnf', 'check-update'], capture_output=True, text=True,timeout=180)
        assert result.returncode in [0, 100], f"dnf check-update failed with unexpected exit code: {result.returncode}"
    except FileNotFoundError:
        pytest.fail("Command 'dnf' not found in the container.")
    except subprocess.TimeoutExpired:
        pytest.fail("'dnf check-update' timed out after 3 minutes.")

def test_network_dns_and_tcp_connectivity():
    try:
        socket.create_connection(("rockylinux.org", 80), timeout=10)
    except socket.gaierror:
        pytest.fail("DNS resolution failed. Could not resolve 'rockylinux.org'.")
    except socket.timeout:
        pytest.fail("Connection timed out. A firewall might be blocking outbound traffic on port 80.")
    except OSError as e:
        pytest.fail(f"An OS error occurred during connection: {e}")
        
@pytest.mark.parametrize("directory_path", ["/proc", "/sys", "/tmp", "/var/log", "/etc", "/root"])
def test_core_filesystem_directories_exist(directory_path):
    assert os.path.isdir(directory_path), f"Expected directory '{directory_path}' not found."

@pytest.mark.parametrize("path", ["/bin", "/sbin", "/lib"])
def test_merged_usr_filesystem_layout(path):
    assert os.path.islink(path), f"Path '{path}' is not a symlink as expected"
    
    target = os.readlink(path)
    expected_target = f"usr/{os.path.basename(path)}"
    assert target == expected_target, f"Symlink '{path}' points to '{target}', but expected 'usr/{os.path.basename(path)}'."

@pytest.mark.parametrize("path", ["/bin", "/sbin", "/lib", "/lib64" ])
def test_merged_usr_filesystem_layout(path):
    assert os.path.islink(path), f"Path '{path}' is not a symlink as expected in Rocky Linux 9."
    
    target = os.readlink(path)
    expected_target = f"usr/{os.path.basename(path)}"
    assert target == expected_target, f"Symlink '{path}' points to '{target}', but expected '{expected_target}'."