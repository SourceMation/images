import subprocess
import pytest

def test_postgres_exporter_yml_exists():
    result = subprocess.run(["test", "-f", "./postgres_exporter.yml"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Postgres-exporter.yml does not exists"

def test_postgres_exporter_executable():
    result = subprocess.run(["test", "-f", "/bin/postgres_exporter", "&&", "test", "-x", "/bin/postgres_exporter"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Postgres-exporter is not an executable file"

def test_postgres_exporter_listening_on_port_9187():
    try:
        # Check if postgres exporter is listening on port 9187
        result = subprocess.run(['ss', '-tuln'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        assert 'tcp' in result.stdout
        assert ':9187' in result.stdout, "Postgres exporter is not listening on port 9187."
    except FileNotFoundError:
        pytest.skip("ss command not found. Cannot verify listening ports.")