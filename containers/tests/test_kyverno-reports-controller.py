import subprocess
import os

BINARY_PATH = "/usr/local/bin/kyverno-reports-controller"

def test_binary_exists():
    assert os.path.exists(BINARY_PATH), f"Binary not found: {BINARY_PATH}"
    assert os.access(BINARY_PATH, os.X_OK), f"Binary is not executable: {BINARY_PATH}"

def test_binary_help():
    result = subprocess.run([BINARY_PATH, '--help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, f"Running {BINARY_PATH} --help failed with exit code {result.returncode}. Stderr: {result.stderr}"
    output = (result.stdout + result.stderr).lower()
    assert "help" in output or "usage" in output, "Help output not found."
