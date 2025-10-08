import os
import pytest
import subprocess
import pwd
import time
from cassandra.cluster import Cluster, NoHostAvailable

CASSANDRA_HOME = "/opt/cassandra"
CASSANDRA_USER = "cassandra"
CQL_PORT = 9042
GOSSIP_PORT = 7000
CASSANDRA_LOG_FILE = '/var/log/cassandra/system.log'


def test_installation_and_permissions():
    """
    Tests that directories exist, have the correct owner,
    and that the container is running as the 'cassandra' user.
    """

    dirs_to_check = [
        CASSANDRA_HOME,
        '/var/lib/cassandra',
        '/var/log/cassandra'
    ]
    for d in dirs_to_check:
        assert os.path.isdir(d)
        stat_info = os.stat(d)
        owner_uid = stat_info.st_uid
        owner_user = pwd.getpwuid(owner_uid).pw_name
        assert owner_user == CASSANDRA_USER

@pytest.mark.parametrize("binary_name", ["cassandra", "cqlsh"])
def test_cassandra_binaries_exist(binary_name):
    """
    Tests that key binaries exist and are executable.
    """
    binary_path = os.path.join(CASSANDRA_HOME, 'bin', binary_name)
    assert os.path.isfile(binary_path), f"Binary not found: {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Binary is not executable: {binary_path}"

def test_cassandra_process_is_running():
    """
    Tests that the Cassandra Java server process is running.
    """
    try:
        result = subprocess.run(['ps', 'auxww'], capture_output=True, text=True, check=True)
        assert "org.apache.cassandra.service.CassandraDaemon" in result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        pytest.fail(f"Failed to check processes with 'ps auxww': {e}")

@pytest.mark.parametrize("port", [CQL_PORT, GOSSIP_PORT])
def test_cassandra_is_listening_on_ports(port):
    """
    Tests that Cassandra is listening on ports 9042 (CQL) and 7000 (Gossip).
    """
    try:
        result = subprocess.run(['ss', '-tuln'], capture_output=True, text=True, check=True)
        port_is_listening = False
        for _ in range(5):
            if f":{port}" in result.stdout and "LISTEN" in result.stdout:
                port_is_listening = True
                break
            time.sleep(1)
            result = subprocess.run(['ss', '-tuln'], capture_output=True, text=True, check=True)

        assert port_is_listening, f"Port {port} was not found in a 'LISTEN' state."
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        pytest.fail(f"Failed to check listening ports with 'ss': {e}")

def test_cqlsh_connection_and_query():
    """
    Waits for the server to start, connects to it via the CQL client,
    and executes a query to check the version and cluster name.
    """
    cluster = None
    try:
        for i in range(25):
            try:
                cluster = Cluster(['127.0.0.1'], port=CQL_PORT)
                session = cluster.connect()
                break
            except NoHostAvailable:
                print(f"Attempt {i+1}/25: Cassandra CQL port not yet available. Waiting...")
                time.sleep(5)
        else:
            pytest.fail("Cassandra server did not become available on port 9042 within the timeout period.")

        rows = session.execute("SELECT cluster_name, release_version FROM system.local")
        row = rows.one()
        
        assert row is not None
        assert row.cluster_name == "My Cassandra Cluster"

    finally:
        if cluster:
            cluster.shutdown()

def test_startup_log_messages():
    """
    Checks the system.log file for key messages indicating a successful startup.
    """
    log_contains_success = False
    for i in range(25):
        if os.path.isfile(CASSANDRA_LOG_FILE):
            with open(CASSANDRA_LOG_FILE, 'r') as f:
                log_content = f.read()
            if "Startup complete" in log_content:
                log_contains_success = True
                break
        print(f"Attempt {i+1}/25: Waiting for startup messages in log file...")
        time.sleep(5)
    
    assert log_contains_success, f"Log file did not contain 'Startup complete' within the timeout."

    with open(CASSANDRA_LOG_FILE, 'r') as f:
        log_content = f.read()

    assert "state jump to NORMAL" in log_content, "Log message for node joining ring not found."
    assert f"Starting listening for CQL clients on" in log_content, "Log message for CQL listener not found."