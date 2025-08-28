import pytest
import subprocess
import os

def test_kubectl_installed():
    result = subprocess.run(
        ['kubectl', 'version', '--client'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    assert result.returncode == 0, "kubectl is not installed or not found in system PATH"
    assert "Client Version" in result.stdout, "Unexpected output from 'kubectl version --client'"


def test_kubectl_functional_check():
    result = subprocess.run(
        ['kubectl', 'help'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    assert result.returncode == 0, f"kubectl help command failed with stderr: {result.stderr}"
    expected_text = "kubectl controls the Kubernetes cluster manager"
    assert expected_text in result.stdout, f"Did not find expected text '{expected_text}' in kubectl help output"
