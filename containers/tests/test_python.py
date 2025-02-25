import pytest
import subprocess
import os
from pathlib import Path

def test_python3_version():
    result = subprocess.run(['python3', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Failed to retrieve Python3 version"
    version_output = result.stdout.strip() or result.stderr.strip()  # Some systems return the version in stderr
    assert version_output.startswith("Python 3"), f"Unexpected Python version: {version_output}"

def test_python3_basic_script():
    script = "print('Hello, Python3!')"
    result = subprocess.run(['python3', '-c', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Failed to run basic Python3 script"
    assert result.stdout.strip() == "Hello, Python3!", "Unexpected script output"

def test_python3_pythonpath():
    tmp_path = Path("/tmp/")
    script_content = "import sys; print(sys.path)"
    script_file = tmp_path / "test_pythonpath.py"
    script_file.write_text(script_content)

    env = os.environ.copy()
    env['PYTHONPATH'] = str(tmp_path)

    result = subprocess.run(['python3', str(script_file)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
    assert result.returncode == 0, "Failed to run Python script with PYTHONPATH"
    assert str(tmp_path) in result.stdout, f"PYTHONPATH {tmp_path} not found in sys.path"

def test_python3_sys_module():
    script = "import sys; print(sys.version)"
    result = subprocess.run(['python3', '-c', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Failed to run sys module in Python3"
    assert "3." in result.stdout.strip(), "Unexpected output from sys.version"

def test_python3_os_module():
    script = "import os; print(os.getcwd())"
    result = subprocess.run(['python3', '-c', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Failed to run os module in Python3"
    assert result.stdout.strip(), "os.getcwd() did not return a valid path"

def test_python3_standard_modules():
    modules = ["json", "os", "sys", "re"]
    for module in modules:
        script = f"import {module}"
        result = subprocess.run(['python3', '-c', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        assert result.returncode == 0, f"Failed to import module: {module}"

def test_python3_run_script_file():
    tmp_path = Path("/tmp/")
    script_content = "print('This is a test script.')"
    script_file = tmp_path / "test_script.py"

    script_file.write_text(script_content)

    result = subprocess.run(['python3', str(script_file)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Failed to run Python script from file"
    assert result.stdout.strip() == "This is a test script.", "Unexpected script output from file"

def test_python3_pip_installed():
    result = subprocess.run(['python3', '-m', 'pip', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "pip is not installed for Python3"
    assert "python 3" in result.stdout.lower(), "pip does not seem to be associated with Python 3"

def test_python3_pip_install_package():
    tmp_path = Path("/tmp/")
    result = subprocess.run(['python3', '-m', 'pip', 'install', '--target', str(tmp_path), 'requests'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Failed to install package 'requests' using pip"
    assert (tmp_path / 'requests').exists(), "'requests' package not found in the target directory"

def test_python3_virtualenv():
    tmp_path = Path("/tmp/")
    venv_path = tmp_path / "venv"

    result = subprocess.run(['python3', '-m', 'venv', str(venv_path)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Failed to create a virtual environment"

    activate_script = venv_path / "bin" / "activate"

    command = f". {activate_script} && python --version"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, executable="/bin/bash")
    assert result.returncode == 0, "Failed to activate virtual environment"
    assert "Python 3" in result.stdout, "Unexpected Python version in virtual environment"