import pytest
import subprocess
import os
import pwd

def test_azure_cli_installed():
    """Test if Azure CLI is installed and accessible"""
    result = subprocess.run(['az', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Azure CLI is not installed or not found in system PATH"
    assert "azure-cli" in result.stdout.lower(), "Unexpected output from 'az --version'"

def test_azure_cli_version():
    """Test if Azure CLI version meets minimum requirements"""
    result = subprocess.run(['az', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Azure CLI is not installed or not found in system PATH"
    
    version_line = result.stdout.strip()
    # Extract version from output like "azure-cli 2.77.0"
    lines = version_line.split('\n')
    version_info = None
    
    for line in lines:
        if 'azure-cli' in line and not line.strip().startswith('azure-cli-'):
            parts = line.split()
            if len(parts) >= 2:
                version_info = parts[1]
                break
    
    assert version_info is not None, f"Could not extract version from: {version_line}"
    
    # Parse version (e.g., "2.77.0")
    version_parts = version_info.split('.')
    major_version = int(version_parts[0])
    minor_version = int(version_parts[1])
    
    assert major_version >= 2, f"Azure CLI major version should be >= 2: {version_info}"
    assert minor_version >= 77, f"Azure CLI minor version should be >= 70: {version_info}"

def test_azure_cli_basic_commands():
    """Test basic Azure CLI commands work"""
    # Test help command
    result = subprocess.run(['az', '--help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Azure CLI help command failed"
    assert "azure" in result.stdout.lower(), "Azure CLI help output doesn't contain expected content"
    
    # Test version command
    result = subprocess.run(['az', 'version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Azure CLI version command failed"

def test_azure_cli_extensions_support():
    """Test if Azure CLI can list extensions"""
    result = subprocess.run(['az', 'extension', 'list'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Azure CLI extension list command failed"

def test_azure_user_exists():
    """Test if the azure-cli user exists"""
    try:
        user_info = pwd.getpwnam('azure-cli')
        assert user_info.pw_name == 'azure-cli', "azure-cli user does not exist"
        assert user_info.pw_shell == '/bin/bash', "azure-cli user shell is not /bin/bash"
        assert os.path.exists(user_info.pw_dir), "azure-cli user home directory does not exist"
    except KeyError:
        pytest.fail("azure-cli user does not exist")

def test_azure_user_home_directory():
    """Test if azure-cli user home directory is properly set up"""
    user_info = pwd.getpwnam('azure-cli')
    home_dir = user_info.pw_dir
    
    assert os.path.exists(home_dir), f"Home directory does not exist: {home_dir}"
    assert os.path.isdir(home_dir), f"Home path is not a directory: {home_dir}"
    
    # Check directory ownership
    dir_stat = os.stat(home_dir)
    assert dir_stat.st_uid == user_info.pw_uid, "Home directory is not owned by azure-cli user"
