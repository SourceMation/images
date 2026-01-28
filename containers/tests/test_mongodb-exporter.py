import pytest
import subprocess

def test_mongodb_exporter_installed():
    result = subprocess.run(
        ['mongodb_exporter', '--version'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    # The command might fail if it tries to connect to mongodb by default or just print version and exit 0
    # But often exporters print version and exit 0.
    # percona mongodb_exporter usually prints version to stdout/stderr
    assert result.returncode == 0 or "version" in result.stdout or "version" in result.stderr, "mongodb_exporter is not installed or failed to print version"

def test_mongodb_exporter_help():
    result = subprocess.run(
        ['mongodb_exporter', '--help'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    assert result.returncode == 0, "mongodb_exporter --help failed"
    assert "usage" in result.stdout.lower() or "usage" in result.stderr.lower() or "flags" in result.stderr.lower(), "Did not find expected text in help output"
