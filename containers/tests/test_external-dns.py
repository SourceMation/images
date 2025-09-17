import pytest
import subprocess
import os
import tempfile


def test_external_dns_installed():
    """Test that external-dns binary is installed and accessible."""
    result = subprocess.run(['external-dns', '--version'], 
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "external-dns is not installed or not found in system PATH"
    
    # Version output can be in stdout or stderr, and might just be the version number
    version_output = result.stdout.strip() + result.stderr.strip()
    assert len(version_output) > 0, "No version output from 'external-dns --version'"
    assert any(char.isdigit() for char in version_output), "Version output should contain digits"

def test_external_dns_help():
    """Test that help command works and shows expected options."""
    result = subprocess.run(['external-dns', '--help'], 
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, f"Help command failed: {result.stderr}"
    
    help_output = result.stdout + result.stderr
    
    # Check for key command line options
    expected_options = [
        '--provider',
        '--source',
        '--log-level',
        '--interval'
    ]
    
    for option in expected_options:
        assert option in help_output, f"Expected option '{option}' not found in help output"

def test_external_dns_providers():
    """Test that external-dns supports expected DNS providers."""
    result = subprocess.run(['external-dns', '--help'], 
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Help command failed"
    
    help_output = result.stdout + result.stderr
    
    # Check for major DNS providers
    expected_providers = [
        'aws',
        'google',
        'azure',
        'cloudflare'
    ]
    
    for provider in expected_providers:
        assert provider in help_output.lower(), f"Provider '{provider}' not found in help output"

def test_external_dns_log_levels():
    """Test different log levels."""
    log_levels = ['debug', 'info', 'warn', 'error']
    
    for level in log_levels:
        result = subprocess.run([
            'external-dns',
            '--provider=aws',
            '--source=service',
            '--dry-run',
            '--once',
            f'--log-level={level}'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30)
        
        assert result.returncode in [0, 1], f"Log level '{level}' test failed: {result.stderr}"

def test_external_dns_invalid_provider():
    """Test external-dns behavior with invalid provider."""
    result = subprocess.run([
        'external-dns',
        '--provider=invalid-provider',
        '--source=service',
        '--dry-run',
        '--once'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=15)
    
    # Should fail with invalid provider
    assert result.returncode != 0, "Should fail with invalid provider"
    
    output = result.stdout + result.stderr
    assert "provider" in output.lower() or "invalid" in output.lower(), \
        "Should indicate provider error"

def test_external_dns_multiple_sources():
    """Test external-dns with multiple sources."""
    result = subprocess.run([
        'external-dns',
        '--provider=aws',
        '--source=service',
        '--source=ingress',
        '--source=node',
        '--txt-owner-id=test-cluster',
        '--dry-run',
        '--once',
        '--log-level=debug'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30)
    
    assert result.returncode in [0, 1], f"Multiple sources test failed: {result.stderr}"
    
    output = result.stdout + result.stderr
    # Should mention the sources in debug output
    assert "service" in output.lower(), "Service source not mentioned in output"

def test_external_dns_binary_permissions():
    """Test that external-dns binary has correct permissions."""
    result = subprocess.run(['which', 'external-dns'], 
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "external-dns binary not found in PATH"
    
    binary_path = result.stdout.strip()
    stat_result = os.stat(binary_path)
    
    # Check if executable by user
    assert stat_result.st_mode & 0o100, "external-dns binary is not executable by user"

def test_external_dns_user_exists():
    result = subprocess.run(['id', 'external-dns'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "external-dns user does not exist"
    
    # Check if external-dns group exists  
    result = subprocess.run(['getent', 'group', 'external-dns'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "external-dns group does not exist"