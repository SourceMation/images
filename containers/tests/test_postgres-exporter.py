import subprocess
import pytest
import os

def test_postgres_exporter_yml_exists():
    yml_file = '/postgres_exporter.yml'
    assert os.path.isfile(yml_file), f"Config file not found: {yml_file}"

def test_postgres_exporter_executable():
    binary = "/bin/postgres_exporter"
    assert os.path.isfile(binary), f"Binary not found: {binary}"
    assert os.access(binary, os.X_OK), f"Binary is not executable: {binary}"

def test_postgres_exporter_listening_on_port_9187():
    try:
        result = subprocess.run(['ss', '-tuln'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        assert 'tcp' in result.stdout
        assert ':9187' in result.stdout, "Postgres exporter is not listening on port 9187."
    except FileNotFoundError:
        pytest.skip("ss command not found. Cannot verify listening ports.")