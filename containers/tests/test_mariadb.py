import pytest
import subprocess
import os

def test_mariadb_installed():
    result = subprocess.run(['mariadbd', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "MariaDB server is not installed or not found in system PATH"
    assert "mariadb" in result.stdout.lower(), "Unexpected output from 'mariadbd --version'"

def test_mariadb_version():
    result = subprocess.run(['mariadbd', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "MariaDB server is not installed or not found in system PATH"
    
    version_line = result.stdout.strip()
    # Extract version from output like "mariadbd Ver 12.0.2-MariaDB..."
    version_parts = version_line.split()
    version_info = None
    for i, part in enumerate(version_parts):
        if "Ver" in part and i + 1 < len(version_parts):
            version_info = version_parts[i + 1]
            break
    
    assert version_info is not None, f"Could not extract version from: {version_line}"
    major_version = int(version_info.split('.')[0])
    minor_version = int(version_info.split('.')[1])
    
    assert major_version >= 12, f"MariaDB major version should be >= 12: {version_info}"
    assert minor_version >= 0, f"MariaDB minor version should be >= 0: {version_info}"

def test_mariadb_client_installed():
    result = subprocess.run(['mariadb', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "MariaDB client is not installed or not found in system PATH"
    assert "mariadb" in result.stdout.lower(), "Unexpected output from 'mariadb --version'"

def test_mariadb_client_version():
    result = subprocess.run(['mariadb', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "MariaDB client is not installed or not found in system PATH"
    
    version_line = result.stdout.strip()
    # Extract version from output like "mariadb Ver 15.1 Distrib 12.0.2-MariaDB..."
    if "Distrib" in version_line:
        version_info = version_line.split("Distrib ")[1].split()[0]
        major_version = int(version_info.split('.')[0])
        assert major_version >= 12, f"MariaDB client major version should be >= 12: {version_info}"

def test_mariadb_config_file():
    config_file = '/etc/mysql/mariadb.conf.d/10-docker.cnf'
    assert os.path.exists(config_file), f"MariaDB config file not found: {config_file}"
    
    # Check if config file has expected content
    with open(config_file, 'r') as f:
        content = f.read()
    
    assert "[mariadb]" in content, "MariaDB config file missing [mariadb] section"

def test_docker_entrypoint_script():
    entrypoint_script = '/usr/local/bin/docker-entrypoint.sh'
    assert os.path.exists(entrypoint_script), f"Docker entrypoint script not found: {entrypoint_script}"
    
    # Check if script is executable
    import stat
    file_stat = os.stat(entrypoint_script)
    assert file_stat.st_mode & stat.S_IEXEC, "Docker entrypoint script is not executable"

def test_mysql_user_exists():
    # Check if mysql user exists
    result = subprocess.run(['id', 'mysql'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "mysql user does not exist"
    
    # Check if mysql group exists  
    result = subprocess.run(['getent', 'group', 'mysql'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "mysql group does not exist"

def test_mysql_directories_exist():
    directories = ['/var/lib/mysql', '/var/run/mysqld']
    
    for directory in directories:
        assert os.path.exists(directory), f"Required MySQL directory does not exist: {directory}"
        
        # Check directory permissions
        import stat
        dir_stat = os.stat(directory)
        # Check if directory is owned by mysql user (assuming mysql UID is consistent)
        # This might vary depending on how the container is run

def test_timezone_data_present():
    # Check if timezone data is available
    assert os.path.exists('/usr/share/zoneinfo'), "Timezone data not found"
    assert os.path.exists('/usr/share/zoneinfo/UTC'), "UTC timezone file not found"

def test_mariadbadmin_tool():
    result = subprocess.run(['mariadb-admin', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "mariadb-admin tool is not installed or not found in system PATH"
    assert "mariadb" in result.stdout.lower(), "Unexpected output from 'mariadb-admin --version'"

def test_mariadb_utilities():
    utilities = ['mariadb-dump', 'mariadb-import', 'mariadb-show']
    
    for utility in utilities:
        result = subprocess.run([utility, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        assert result.returncode == 0, f"MariaDB utility {utility} is not installed or not found in system PATH"
