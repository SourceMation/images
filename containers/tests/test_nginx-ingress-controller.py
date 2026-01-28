import pytest
import subprocess

def test_nginx_ingress_controller_installed():
    result = subprocess.run(
        ['nginx-ingress-controller', '--version'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    # The output format might vary, but it should exit 0 or print version info
    assert result.returncode == 0 or "Release" in result.stdout or "Release" in result.stderr, "nginx-ingress-controller is not installed or failed to print version"

def test_nginx_ingress_controller_help():
    result = subprocess.run(
        ['nginx-ingress-controller', '--help'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    assert result.returncode == 0, "nginx-ingress-controller --help failed"
    assert "Usage" in result.stdout or "Usage" in result.stderr, "Did not find expected text in help output"

def test_nginx_installed():
    result = subprocess.run(
        ['nginx', '-v'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    assert result.returncode == 0, "nginx is not installed"
    assert "nginx version" in result.stderr, "Unexpected output from nginx -v"
