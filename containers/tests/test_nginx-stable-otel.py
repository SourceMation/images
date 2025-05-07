import pytest
import subprocess
import os


def test_nginx_opentelemetry_module_available():
    """
    Checks if the Nginx OpenTelemetry module is available by attempting to load
    it in the Nginx configuration. This test verifies the presence of the
    module by including its directives in a test configuration and checking
    if Nginx can load the configuration without errors.
    """
    nginx_config_test = """
    load_module modules/ngx_otel_module.so; # Important: Load the module

    events {
    }

    http {
        otel_exporter {
            endpoint localhost:4317;
        }
        server {
                    otel_trace         on;
            otel_trace_context inject;
            listen 8080;
            location / {
                return 200 "OK";
            }
        }
    }
    """
    config_file = "/tmp/nginx_opentelemetry_test.conf"
    try:
        with open(config_file, "w") as f:
            f.write(nginx_config_test)
        result = subprocess.run(['nginx', '-t', '-c', config_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        assert "syntax is ok" in result.stderr, f"Nginx configuration test failed. Error: {result.stderr}"
        assert "test is successful" in result.stderr, f"Nginx configuration test was not fully successful. Output: {result.stderr}"
    finally:
        if os.path.exists(config_file):
            os.remove(config_file)

