import pytest
import subprocess
import os

def test_node_installed():
    result = subprocess.run(['node', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Node.js is not installed or not found in system PATH"
    assert result.stdout.startswith('v'), f"Unexpected output from 'node --version': {result.stdout}"

def test_npm_installed():
    result = subprocess.run(['npm', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "npm is not installed or not found in system PATH"

def test_node_version():
    result = subprocess.run(['node', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Node.js is not installed or not found in system PATH"
    
    version_info = result.stdout.strip()
    major_version = int(version_info[1:version_info.index('.')])
    
    assert major_version >= 14, f"Node.js version is too old: {version_info}. Requires Node.js 14 or higher."

def test_npm_version():
    result = subprocess.run(['npm', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "npm is not installed or not found in system PATH"
    
    version_info = result.stdout.strip()
    assert version_info, "Unexpected output from 'npm -v'"

def test_run_simple_node_script():
    script_content = """
    console.log("Node.js is working!");
    """
    
    with open('test_script.js', 'w') as f:
        f.write(script_content)

    result = subprocess.run(['node', 'test_script.js'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, f"Failed to run Node.js script: {result.stderr}"
    assert "Node.js is working!" in result.stdout, "Node.js script did not produce expected output"

    os.remove('test_script.js')

def test_install_npm_package():
    result = subprocess.run(['npm', 'install', 'express'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    assert result.returncode == 0, f"Failed to install npm package: {result.stderr}"
    assert 'added' in result.stdout or 'up to date' in result.stdout, "npm did not install the package as expected"

    package_check = subprocess.run(['node', '-e', 'require("express")'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert package_check.returncode == 0, "Failed to load installed npm package"

    subprocess.run(['npm', 'uninstall', 'express'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)