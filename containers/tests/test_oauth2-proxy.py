import pytest
import subprocess

def test_oauth2_proxy_installed():
    result = subprocess.run(
        ['oauth2-proxy', '--version'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    assert result.returncode == 0, "oauth2-proxy is not installed or not found in system PATH"
    assert "oauth2-proxy" in result.stderr or "oauth2-proxy" in result.stdout, "Unexpected output from 'oauth2-proxy --version'"

def test_oauth2_proxy_help():
    result = subprocess.run(
        ['oauth2-proxy', '--help'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    assert result.returncode == 0, "oauth2-proxy --help failed"
    # oauth2-proxy help output usually contains usage info
    assert "Usage of" in result.stderr or "Usage of" in result.stdout, "Did not find expected text in help output"
