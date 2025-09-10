import os
import subprocess
import pytest
import time
import socket

def test_postgres_user_and_group_exist():
    """Checks if the 'postgres' user and group were created."""
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
    result = subprocess.run(["test", "-f", "/opt/pgpool-II/bin/pgpool", "-a", "-x", "/opt/pgpool-II/bin/pgpool"])
    assert result.returncode == 0, "binary file is not executable."

def test_entrypoint_and_start_scripts_exist():
    result = subprocess.run(["test", "-f", "/opt/pgpool-II/bin/entrypoint.sh", "&&", "test", "-f", "/opt/pgpool-II/bin/start.sh"])
    assert result.returncode == 0, "entrypoint or/and start script are not executable."
    