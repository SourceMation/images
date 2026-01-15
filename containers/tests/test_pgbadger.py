import pytest
import subprocess
import os

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

def test_pgbadger_generate_report():
    """Test if pgBadger can generate a report from a log file"""
    log_file = "/tmp/tests/data/postgresql.log"
    output_file = "/tmp/out.html"
    
    # Ensure log file exists
    assert os.path.exists(log_file), f"Log file not found at {log_file}"

    # Run pgBadger
    # -f stderr is often used for postgres logs in containers, but auto-detection usually works.
    # We'll stick to defaults unless it fails.
    result = subprocess.run(['pgbadger', log_file, '-o', output_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    assert result.returncode == 0, f"pgBadger failed to generate report. Stderr: {result.stderr}"
    
    # Check if output file exists and is not empty
    assert os.path.exists(output_file), "Output HTML report was not created"
    assert os.path.getsize(output_file) > 0, "Output HTML report is empty"
    
    # Cleanup
    if os.path.exists(output_file):
        os.remove(output_file)
