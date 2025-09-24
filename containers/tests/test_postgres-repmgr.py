import os
import pytest
import subprocess
import time
import shutil

REPMGR_CONFIG_FILE = "/etc/repmgr/repmgr.conf"

postgres_executable_path = shutil.which('postgres')
assert postgres_executable_path, "Could not find 'postgres' executable in system PATH"
PG_BIN_DIR = os.path.dirname(postgres_executable_path)


def test_installation_files_exist():
    assert os.path.isfile(os.path.join(PG_BIN_DIR, "repmgr")), f"Binary not found: {PG_BIN_DIR}/repmgr"
    assert os.access(os.path.join(PG_BIN_DIR, "repmgr"), os.X_OK)
    
    assert os.path.isfile(os.path.join(PG_BIN_DIR, "repmgrd")), f"Binary not found: {PG_BIN_DIR}/repmgrd"
    assert os.access(os.path.join(PG_BIN_DIR, "repmgrd"), os.X_OK)
    
    assert os.path.isfile(REPMGR_CONFIG_FILE), f"Config file not found: {REPMGR_CONFIG_FILE}"

def test_postgres_and_repmgrd_processes_are_running():
    try:
        result = subprocess.run(['ps', 'auxww'], capture_output=True, text=True, check=True)
        assert "postgres: checkpointer" in result.stdout
        assert "repmgrd" in result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        pytest.fail(f"Failed to check processes with 'ps auxww': {e}")

def test_postgres_is_listening_on_port():
    try:
        result = subprocess.run(['ss', '-tuln'], capture_output=True, text=True, check=True)
        port_is_listening = False
        for line in result.stdout.splitlines():
            if "LISTEN" in line and ":5432" in line:
                port_is_listening = True
                break
        assert port_is_listening, "Port 5432 was not found in a 'LISTEN' state."
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        pytest.fail(f"Failed to check listening ports with 'ss': {e}")

def test_cluster_show_has_primary_and_standby():
    repmgr_command_str = f"repmgr -f {REPMGR_CONFIG_FILE} cluster show"
    command = ['su', 'postgres', '-c', repmgr_command_str]
    
    result = None
    output_ok = False
    for i in range(10):
        result = subprocess.run(command, capture_output=True, text=True, timeout=10)
        
        lines = result.stdout.strip().splitlines()
        if len(lines) >= 3:
            output_ok = True
            break
        time.sleep(5)
    
    if not output_ok:
        pytest.fail(
            f"Command '{' '.join(command)}' did not produce expected output in time.\n"
            f"Exit Code: {result.returncode}\n"
            f"Stderr: {result.stderr}\n"
            f"Stdout: {result.stdout}"
        )

    node_lines = [line for line in result.stdout.splitlines() if "primary" in line or "standby" in line]
    
    assert len(node_lines) == 2, f"Expected 2 nodes, but found {len(node_lines)} in output:\n{result.stdout}"
    
    primary_found = any("primary" in line and "running" in line for line in node_lines)
    standby_found = any("standby" in line and "running" in line for line in node_lines)
    
    assert primary_found, "A running primary node was not found in 'repmgr cluster show' output."
    assert standby_found, "A running standby node was not found in 'repmgr cluster show' output."