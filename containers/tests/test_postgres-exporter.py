import subprocess

def test_postgres_exporter_yml_exists():
    result = subprocess.run(["test", "-f", "./postgres_exporter.yml"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Postgres-exporter.yml is not exists"

def test_postgres_exporter_executable():
    result = subprocess.run(["test", "-f", "/bin/postgres_exporter", "&&", "test", "-x", "/bin/postgres_exporter"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Postgres-exporter is not an executable file"
