import pytest
import subprocess
import psycopg2
import locale


def test_postgresql_executables_in_path():
    executables = ["initdb", "postgres", "pg_ctl", "pg_controldata", "pg_basebackup"]
    for exe in executables:
        result = subprocess.run(['which', exe], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        assert result.returncode == 0, f"{exe} is not in PATH"


def test_barman_cloud_executables_in_path():
    executables = [
        "barman-cloud-backup",
        "barman-cloud-backup-delete",
        "barman-cloud-backup-list",
        "barman-cloud-check-wal-archive",
        "barman-cloud-restore",
        "barman-cloud-wal-archive",
        "barman-cloud-wal-restore",
    ]
    for exe in executables:
        result = subprocess.run(['which', exe], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        assert result.returncode == 0, f"{exe} is not in PATH"


def test_pgaudit_package_installed():
    """Checks if the pgaudit package is installed."""
    result = subprocess.run(
        ["apt", "list", "--installed", "postgresql-16-pgaudit"],  # Adjust version if needed
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert "postgresql-16-pgaudit" in result.stdout, "pgaudit package is not installed"


def test_locale_settings():
    try:
        current_locale = locale.getlocale()
        assert current_locale == ('pl_PL', 'UTF-8'), f"Locale is not pl_PL.UTF-8, but {current_locale}"
    except locale.Error as e:
        pytest.fail(f"Locale error: {e}")


def test_du_in_path():
    result = subprocess.run(['which', 'du'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "du command not found in PATH"


def test_postgresql_locale():
    connection = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="localhost")
    cursor = connection.cursor()
    try:
        cursor.execute("SHOW lc_messages")
        messages = cursor.fetchone()[0]
        cursor.execute("SHOW server_encoding")
        encoding = cursor.fetchone()[0]
        assert messages == "pl_PL.UTF-8", f"PostgreSQL messages is not pl_PL.UTF-8, but {messages}"
        assert encoding == "UTF8", f"PostgreSQL encoding is not UTF8, but {encoding}"
    finally:
        cursor.close()
        connection.close()
