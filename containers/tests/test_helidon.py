import subprocess
import os
import time
import requests

def test_helidon_version():
    result = subprocess.run(["helidon", "--version"], capture_output=True, text=True)
    assert result.returncode == 0, "Helidon is not installed or not working correctly"
    assert "default.helidon.version" in result.stdout, "Invalid response from helidon --version"

def get_lts_version():
    try:
        import urllib.request
        req = urllib.request.urlopen("https://helidon.io/cli-data/versions.xml", timeout=5)
        content = req.read().decode('utf-8')
        for line in content.splitlines():
            if '<version order=' in line and '>4.' in line:
                return line.split('>')[1].split('<')[0]
    except Exception:
        pass
    return "4.5.4"

def test_helidon_init():
    test_dir = "helidon_test_project"
    
    if os.path.exists(test_dir):
        subprocess.run(["rm", "-rf", test_dir])
    
    lts_version = get_lts_version()
    result = subprocess.run(["helidon", "init", "--batch", "--version", lts_version, "--project", test_dir], capture_output=True, text=True)
    assert result.returncode == 0, "Helidon init failed"
    assert os.path.isdir(test_dir), "Project directory was not created"
    assert os.path.isfile(os.path.join(test_dir, "pom.xml")), "Missing pom.xml file in the new project"

def test_helidon_dev():
    test_dir = "helidon_test_project"
    os.chdir(test_dir)
    
    process = subprocess.Popen(["helidon", "dev"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    time.sleep(120)
    
    try:
        response = requests.get("http://localhost:8080/simple-greet")
        assert response.status_code == 200, "The application is not running correctly on port 8080"
    finally:
        process.terminate()
        process.wait()
    
    os.chdir("..")
