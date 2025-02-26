import subprocess
import time
import requests

def test_karavan_running():
    result = subprocess.run(["pgrep", "-f", "karavan.jar"], capture_output=True, text=True)
    assert result.returncode == 0, "Karavan is not running as a Java process"

def test_karavan_http_response():
    url = "http://localhost:8080"
    
    time.sleep(5)
    
    try:
        response = requests.get(url)
        assert response.status_code == 200, f"Karavan is not responding correctly, status code: {response.status_code}"
    except requests.exceptions.ConnectionError:
        assert False, "No connection to Karavan on port 8080"
