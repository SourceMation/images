import pytest
import subprocess

def test_pgbadger_installed():
    """Test if pgBadger is installed and accessible"""
    result = subprocess.run(['pgbadger', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "pgBadger is not installed or not found in system PATH"
    assert "pgBadger version" in result.stdout, "Unexpected output from 'pgbadger --version'"

def test_pgbadger_help():
    """Test pgBadger help command"""
    result = subprocess.run(['pgbadger', '--help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "pgBadger help command failed"
    assert "Usage: pgbadger [options] logfile" in result.stdout, "pgBadger help output doesn't contain expected usage info"
