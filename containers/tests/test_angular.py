import pytest
import subprocess
import os
import shutil
import re


def test_node_installed():
    result = subprocess.run(['node', '--version'], capture_output=True, text=True)
    assert result.returncode == 0, "Node.js is not installed or not in PATH."

    # Use regex to extract the major version number (e.g., '24' from 'v24.1.0')
    match = re.search(r'v(\d+)\.', result.stdout)
    assert match, f"Could not parse Node.js version from output: {result.stdout}"

    major_version = int(match.group(1))
    assert major_version >= 20, f"Expected Node.js v20+ for Angular, but found: {result.stdout.strip()}"


def test_npm_installed():
    """Checks if npm (Node Package Manager) is installed, as it comes with Node.js."""
    result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
    assert result.returncode == 0, "npm is not installed or not in PATH."
    assert result.stdout.strip(), "npm --version command returned empty output."


def test_angular_cli_installed():
    """
    Checks if the Angular CLI ('ng' command) is installed and operational.
    This is the primary tool for creating and managing Angular projects.
    """
    result = subprocess.run(['ng', '--version'], capture_output=True, text=True)
    assert result.returncode == 0, "Angular CLI is not installed or not in PATH. Run 'npm install -g @angular/cli'."
    # We have to check if there are at some digits in the output
    assert re.search(r'\d\d', result.stdout), "The 'ng --version' command did not return the expected output."


def test_angular_project_lifecycle():
    """
    Verifies the complete Angular workflow:
    1. Creates a new project ('ng new').
    2. Builds the project ('ng build').
    """
    project_name = "angular-test-app"

    # Create project
    print(f"\nCreating new Angular project: '{project_name}'...")
    create_command = [
        'ng', 'new', project_name,
        '--defaults',         # Use default settings to avoid interactive prompts
        '--skip-git=true',    # Don't initialize a git repository
        '--routing=false'     # Create a simpler project without a routing module
    ]
    create_result = subprocess.run(create_command, capture_output=True, text=True, timeout=300)
    assert create_result.returncode == 0, f"Failed to create new Angular project.\nSTDOUT: {create_result.stdout}\nSTDERR: {create_result.stderr}"

    project_path = os.path.join(os.getcwd(), project_name)
    assert os.path.isdir(project_path), f"Project directory '{project_name}' was not created."

    # Build the project
    print("Building the project (this will also install dependencies)...")
    build_result = subprocess.run(['ng', 'build'], cwd=project_path, capture_output=True, text=True, timeout=300)
    assert build_result.returncode == 0, f"Failed to build the Angular project.\nSTDOUT: {build_result.stdout}\nSTDERR: {build_result.stderr}"
    assert os.path.isdir(os.path.join(project_path, 'dist')), "Build did not create the 'dist' directory."

