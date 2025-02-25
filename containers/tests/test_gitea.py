import pytest
import subprocess
import os
import requests

def test_gitea_version():
    result = subprocess.run(['gitea', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Failed to retrieve Gitea version"
    assert "Gitea version" in result.stdout, "Unexpected output from Gitea version command"

def test_gitea_web_interface():
    url = "http://localhost:3000"
    try:
        response = requests.get(url)
        assert response.status_code == 200, f"Gitea web interface returned unexpected status code {response.status_code}"
        assert "Gitea: Git with a cup of tea" in response.text, "Gitea web interface did not return the expected content"
    except requests.ConnectionError:
        pytest.fail("Failed to connect to Gitea web interface")

def test_gitea_home_directory():
    gitea_home = os.getenv('GITEA_HOME', '/var/lib/gitea')
    assert os.path.isdir(gitea_home), f"Gitea home directory {gitea_home} does not exist"
