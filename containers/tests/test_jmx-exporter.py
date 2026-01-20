import pytest
import subprocess

def test_jmx_exporter_help():
    result = subprocess.run(
        ['java', '-jar', '/opt/jmx_exporter/jmx_prometheus_httpserver.jar'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    # It returns non-zero when no args provided but prints usage.
    assert "Usage" in result.stdout or "Usage" in result.stderr, "Did not find expected usage text"

def test_jmx_agent_jar_exists():
    result = subprocess.run(
        ['ls', '/opt/jmx_exporter/jmx_prometheus_javaagent.jar'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    assert result.returncode == 0, "jmx_prometheus_javaagent.jar not found"
