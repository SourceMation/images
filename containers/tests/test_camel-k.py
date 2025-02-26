import subprocess

def test_camel_k_installed():
    result = subprocess.run(["kamel", "version"], capture_output=True, text=True, timeout=60)
    assert result.returncode == 0, "Camel-K is not installed or not accessible"
    assert "Camel K" in result.stdout, "Unexpected output from 'kamel version'"

def test_camel_k_help():
    result = subprocess.run(["kamel", "-h"], capture_output=True, text=True, timeout=60)
    assert result.returncode == 0, "Camel-K is not installed or not accessible"
    assert "Apache Camel K is a lightweight integration platform" in result.stdout, "Unexpected output from 'kamel -h'"

def test_camel_k_get_help():
    result = subprocess.run(["kamel", "get", "-h"], capture_output=True, text=True, timeout=60)
    assert result.returncode == 0, "Camel-K is not installed or not accessible"
    assert "Get the status of integrations deployed on Kubernetes" in result.stdout, "Unexpected output from 'kamel get -h'"