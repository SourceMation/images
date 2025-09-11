import subprocess
import os

def test_postgres_user_and_group_exist():
    result = subprocess.run([" id", "postgres"], capture_output=True, text=True)
    assert result.returncode == 0, "id postgres command failed."
    assert "(postgres)" in result.stdout, "group postgres not found."

def test_ownership_main_pgpool_directory():
    result = subprocess.run(["stat", "-c", "%U", "/opt/pgpool-II"])
    assert result.returncode == 0, "stat command failed."
    assert result.stdout == "postgres", "ownership of the main pgpool directory is invalid"

def test_ownership_run_pgpool_directory():
    result = subprocess.run(["stat", "-c", "%U", "/var/run/pgpool"])
    assert result.returncode == 0, "stat command failed."
    assert result.stdout == "postgres", "ownership of the run pgpool directory is invalid"

def test_pgpool_binary_is_executable():
    binary = "/opt/pgpool-II/bin/pgpool"
    assert os.path.isfile(binary), f"Binary not found: {binary}"
    assert os.access(binary, os.X_OK), f"Binary is not executable: {binary}"

def test_entrypoint_script_exist():
    entrypoint = '/opt/pgpool-II/bin/entrypoint.sh'
    assert os.path.isfile(entrypoint), f"Config file not found: {entrypoint}"

def test_start_script_exist():
    start = '/opt/pgpool-II/bin/start.sh'
    assert os.path.isfile(start), f"Config file not found: {start}"