import pytest
import subprocess
import os
import tempfile

def test_git_installed():
    result = subprocess.run(['git', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Git is not installed or not found in system PATH"
    assert "git version" in result.stdout.lower(), "Unexpected output from 'git --version'"

def test_git_version():
    result = subprocess.run(['git', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Git is not installed or not found in system PATH"
    
    version_line = result.stdout.strip()
    # Extract version from "git version X.YY.Z"
    version_info = version_line.split(' ')[2]
    major_version = int(version_info.split('.')[0])
    minor_version = int(version_info.split('.')[1])
    
    assert major_version >= 2, f"Git major version should be >= 2: {version_info}"
    assert minor_version >= 30, f"Git minor version should be >= 30: {version_info}"

def test_git_init_repository():
    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        
        init_result = subprocess.run(['git', 'init', 'test-repo'], 
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        assert init_result.returncode == 0, f"Failed to initialize git repository: {init_result.stderr}"
        assert os.path.exists('test-repo/.git'), "Git repository not created"

def test_git_config_and_commit():
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_path = os.path.join(temp_dir, 'test-repo')
        os.makedirs(repo_path)
        os.chdir(repo_path)
        
        # Initialize repository
        subprocess.run(['git', 'init'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        
        # Configure git
        subprocess.run(['git', 'config', 'user.email', 'test@example.com'], 
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        subprocess.run(['git', 'config', 'user.name', 'Test User'], 
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        
        # Create and add file
        with open('test.txt', 'w') as f:
            f.write('Hello Git!')
        
        add_result = subprocess.run(['git', 'add', 'test.txt'], 
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        assert add_result.returncode == 0, f"Failed to add file to git: {add_result.stderr}"
        
        # Commit
        commit_result = subprocess.run(['git', 'commit', '-m', 'Initial commit'], 
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        assert commit_result.returncode == 0, f"Failed to commit: {commit_result.stderr}"
        
        # Check log
        log_result = subprocess.run(['git', 'log', '--oneline'], 
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        assert log_result.returncode == 0, "Failed to get git log"
        assert "Initial commit" in log_result.stdout, "Commit not found in git log"

def test_git_clone_https():
    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        
        clone_result = subprocess.run(['git', 'clone', '--depth', '1', 
                                     'https://github.com/sourcemation/images.git', 'test-clone'], 
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        assert clone_result.returncode == 0, f"Failed to clone repository: {clone_result.stderr}"
        assert os.path.exists('test-clone'), "Cloned repository directory not found"
        assert os.path.exists('test-clone/.git'), "Cloned repository is not a git repository"
