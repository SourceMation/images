import pytest
import subprocess
import os


def test_node_24_installed():
    result = subprocess.run(['node', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Node.js is not installed or not found in system PATH"
    assert result.stdout.startswith('v24.'), f"Expected Node.js version to start with v24., but got: {result.stdout}"


def test_yarn_installed():
    result = subprocess.run(['yarn', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Yarn is not installed or not found in system PATH"
    assert result.stdout.strip() != '', "Yarn version output is empty"


def test_yarn_working():
    # Create a simple package.json
    with open('package.json', 'w') as f:
        f.write('{"name": "test-yarn", "version": "1.0.0"}')

    # Try to initialize yarn
    result_init = subprocess.run(['yarn', 'init', '--yes'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result_init.returncode == 0, f"Yarn init failed: {result_init.stderr}"
    assert 'Saved package.json' in result_init.stdout, "Yarn init did not create package.json as expected"
    assert os.path.exists('package.json'), "package.json was not created"


    # Try to add a package (a lightweight one)
    result_add = subprocess.run(['yarn', 'add', 'lodash'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result_add.returncode == 0, f"Yarn add failed: {result_add.stderr}"
    assert 'Saved 1 new dependency' in result_add.stdout, f"Yarn add output not as expected: {result_add.stdout}"

    result_list = subprocess.run(['yarn', 'list', '--depth=0'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result_list.returncode == 0, f"Yarn list failed: {result_list.stderr}"
    assert 'lodash@' in result_list.stdout or 'No dependencies' in result_list.stdout, f"Yarn list did not show expected output: {result_list.stdout}"

    # Clean up created files and directory
    os.remove('package.json')
    if os.path.exists('yarn.lock'):
        os.remove('yarn.lock')
    if os.path.exists('node_modules'):
        import shutil
        shutil.rmtree('node_modules')


def test_npm_installed():
    result = subprocess.run(['npm', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "npm is not installed or not found in system PATH"


def test_npm_version():
    result = subprocess.run(['npm', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "npm is not installed or not found in system PATH"

    version_info = result.stdout.strip()
    assert version_info, "Unexpected output from 'npm -v'"


def test_run_simple_node_script_24():
    script_content = """
    console.log("Node.js version 24 is working!");
    """

    with open('test_script_24.js', 'w') as f:
        f.write(script_content)

    result = subprocess.run(['node', 'test_script_24.js'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, f"Failed to run Node.js script: {result.stderr}"
    assert "Node.js version 24 is working!" in result.stdout, "Node.js script did not produce expected output"

    os.remove('test_script_24.js')


def test_install_npm_package_24():
    result = subprocess.run(['npm', 'install', 'uuid'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    assert result.returncode == 0, f"Failed to install npm package: {result.stderr}"
    assert 'added' in result.stdout or 'up to date' in result.stdout, "npm did not install the package as expected"

    package_check = subprocess.run(['node', '-e', 'require("uuid")'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert package_check.returncode == 0, "Failed to load installed npm package"
