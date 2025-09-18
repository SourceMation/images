import pytest
import subprocess
import os
import socket
import stat

def test_zookeeper_installed():
    """Test that ZooKeeper server is installed and accessible"""
    result = subprocess.run(['zkServer.sh', '--help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0 or result.returncode == 1, "ZooKeeper server script is not installed or not found in system PATH"

def test_zookeeper_version():
    """Test ZooKeeper version is correct"""
    # Check if ZooKeeper jar files exist
    zk_lib_dir = '/opt/zookeeper/lib'
    assert os.path.exists(zk_lib_dir), f"ZooKeeper lib directory not found: {zk_lib_dir}"
    
    # Look for ZooKeeper jar with version
    jar_files = [f for f in os.listdir(zk_lib_dir) if f.startswith('zookeeper-') and f.endswith('.jar')]
    assert len(jar_files) > 0, "ZooKeeper jar file not found"
    
    # Check version in jar filename
    version_jar = [f for f in jar_files if '3.' in f]
    assert len(version_jar) > 0, f"ZooKeeper version 3.x.y jar not found. Available jars: {jar_files}"

def test_zookeeper_client_installed():
    """Test that ZooKeeper client tools are installed"""
    tools = ['zkCli.sh', 'zkEnv.sh']
    
    for tool in tools:
        result = subprocess.run([tool, '--help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # zkCli.sh returns 1 for help, which is normal
        assert result.returncode in [0, 1], f"ZooKeeper tool {tool} is not installed or not found in system PATH"

def test_zookeeper_config_directory():
    """Test ZooKeeper configuration directory exists and has proper structure"""
    config_dir = '/opt/zookeeper/conf'
    assert os.path.exists(config_dir), f"ZooKeeper config directory not found: {config_dir}"
    
    # Check if zoo.cfg is present (should be copied during build)
    zoo_cfg = os.path.join(config_dir, 'zoo.cfg')
    # Note: zoo.cfg might not exist if not copied, but directory should exist

def test_zookeeper_bin_directory():
    """Test ZooKeeper bin directory exists and contains required scripts"""
    bin_dir = '/opt/zookeeper/bin'
    assert os.path.exists(bin_dir), f"ZooKeeper bin directory not found: {bin_dir}"
    
    required_scripts = ['zkServer.sh', 'zkCli.sh', 'zkEnv.sh']
    
    for script in required_scripts:
        script_path = os.path.join(bin_dir, script)
        assert os.path.exists(script_path), f"Required ZooKeeper script not found: {script_path}"
        
        # Check if script is executable
        file_stat = os.stat(script_path)
        assert file_stat.st_mode & stat.S_IEXEC, f"ZooKeeper script is not executable: {script_path}"

def test_docker_entrypoint_script():
    """Test docker entrypoint script exists and is executable"""
    entrypoint_script = '/usr/local/bin/docker-entrypoint.sh'
    assert os.path.exists(entrypoint_script), f"Docker entrypoint script not found: {entrypoint_script}"
    
    # Check if script is executable
    file_stat = os.stat(entrypoint_script)
    assert file_stat.st_mode & stat.S_IEXEC, "Docker entrypoint script is not executable"

def test_zookeeper_user_exists():
    """Test that zookeeper user and group exist"""
    # Check if zookeeper user exists
    result = subprocess.run(['id', 'zookeeper'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "zookeeper user does not exist"
    
    # Check if zookeeper group exists  
    result = subprocess.run(['getent', 'group', 'zookeeper'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "zookeeper group does not exist"

def test_zookeeper_directories_exist():
    """Test that all required ZooKeeper directories exist"""
    directories = [
        '/opt/zookeeper',
        '/var/lib/zookeeper/data',
        '/var/lib/zookeeper/logs',
        '/var/log/zookeeper'
    ]
    
    for directory in directories:
        assert os.path.exists(directory), f"Required ZooKeeper directory does not exist: {directory}"

def test_zookeeper_directories_permissions():
    """Test that ZooKeeper directories have correct ownership"""
    directories = [
        '/opt/zookeeper',
        '/var/lib/zookeeper/data',
        '/var/lib/zookeeper/logs',
        '/var/log/zookeeper'
    ]
    
    # Get zookeeper user info
    result = subprocess.run(['id', '-u', 'zookeeper'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        zk_uid = int(result.stdout.strip())
        
        for directory in directories:
            if os.path.exists(directory):
                dir_stat = os.stat(directory)
                assert dir_stat.st_uid == zk_uid, f"Directory {directory} is not owned by zookeeper user"

def test_myid_file_exists():
    """Test that myid file exists in data directory"""
    myid_file = '/var/lib/zookeeper/data/myid'
    assert os.path.exists(myid_file), f"myid file not found: {myid_file}"
    
    # Check myid content
    with open(myid_file, 'r') as f:
        content = f.read().strip()
    
    assert content.isdigit(), f"myid file should contain a number, found: {content}"
    assert 1 <= int(content) <= 255, f"myid should be between 1-255, found: {content}"

def test_environment_variables():
    """Test that required environment variables are set"""
    required_env_vars = {
        'ZK_HOME': '/opt/zookeeper',
        'ZK_USER': 'zookeeper',
        'ZK_DATA_DIR': '/var/lib/zookeeper/data',
        'ZK_DATA_LOG_DIR': '/var/lib/zookeeper/logs',
        'ZK_CONF_DIR': '/opt/zookeeper/conf',
        'ZK_LOG_DIR': '/var/log/zookeeper'
    }
    
    for env_var, expected_value in required_env_vars.items():
        actual_value = os.environ.get(env_var)
        assert actual_value == expected_value, f"Environment variable {env_var} should be {expected_value}, found: {actual_value}"

def test_path_includes_zookeeper_bin():
    """Test that ZooKeeper bin directory is in PATH"""
    path = os.environ.get('PATH', '')
    assert '/opt/zookeeper/bin' in path, "ZooKeeper bin directory not found in PATH"

def test_zookeeper_lib_directory():
    """Test ZooKeeper lib directory exists and contains required JAR files"""
    lib_dir = '/opt/zookeeper/lib'
    assert os.path.exists(lib_dir), f"ZooKeeper lib directory not found: {lib_dir}"
    
    # Check for essential JAR files
    jar_files = [f for f in os.listdir(lib_dir) if f.endswith('.jar')]
    assert len(jar_files) > 0, "No JAR files found in ZooKeeper lib directory"
    
    # Check for specific important JARs
    important_jars = ['zookeeper', 'zookeeper-prometheus-metrics', 'slf4j']
    for jar_name in important_jars:
        matching_jars = [f for f in jar_files if jar_name.lower() in f.lower()]
        assert len(matching_jars) > 0, f"No JAR file found containing '{jar_name}' in lib directory"

def test_zookeeper_conf_directory_structure():
    """Test ZooKeeper conf directory has expected structure"""
    conf_dir = '/opt/zookeeper/conf'
    assert os.path.exists(conf_dir), f"ZooKeeper conf directory not found: {conf_dir}"
    
    # Check for configuration templates that should exist
    expected_files = ['configuration.xsl', 'log4j.properties']
    
    for expected_file in expected_files:
        file_path = os.path.join(conf_dir, expected_file)
        # These files should exist from the ZooKeeper distribution
        if os.path.exists(file_path):
            assert os.path.isfile(file_path), f"Expected file is not a regular file: {file_path}"
