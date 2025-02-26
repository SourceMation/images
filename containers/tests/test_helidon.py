import subprocess
import os
import time
import requests

def test_helidon_version():
    result = subprocess.run(["helidon", "--version"], capture_output=True, text=True)
    assert result.returncode == 0, "Helidon is not installed or not working correctly"
    assert "default.helidon.version" in result.stdout, "Invalid response from helidon --version"

def test_helidon_init():
    test_dir = "helidon_test_project"
    
    if os.path.exists(test_dir):
        subprocess.run(["rm", "-rf", test_dir])
    
    result = subprocess.run(["helidon", "init", "--batch", "--project", test_dir], capture_output=True, text=True)
    assert result.returncode == 0, "Helidon init failed"
    assert os.path.isdir(test_dir), "Project directory was not created"
    assert os.path.isfile(os.path.join(test_dir, "pom.xml")), "Missing pom.xml file in the new project"

def test_helidon_dev():
    test_dir = "helidon_test_project"
    os.chdir(test_dir)
    
    process = subprocess.Popen(["helidon", "dev"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    time.sleep(60)
    
    try:
        response = requests.get("http://localhost:8080/simple-greet")
        assert response.status_code == 200, "The application is not running correctly on port 8080"
    finally:
        process.terminate()
        process.wait()
    
    os.chdir("..")
