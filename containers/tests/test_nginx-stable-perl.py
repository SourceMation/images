import pytest
import subprocess
import os


def test_nginx_perl_modules_available():
    """
    Checks if the Nginx Perl module is available by attempting to load it
    in the Nginx configuration. This test assumes that if Nginx can be
    configured to use a Perl module without errors, then the module is likely
    available.
    """
    nginx_config_test = f"""
    load_module modules/ngx_http_perl_module.so;

    events{{}}

    http {{
        perl_set $message 'Hello from Perl!';
        server {{
            listen 8080;
            location /perl {{
                return 200 $message;
            }}
        }}
    }}
    """
    config_file = "/tmp/nginx_perl_test.conf"
    try:
        with open(config_file, "w") as f:
            f.write(nginx_config_test)
        result = subprocess.run(['nginx', '-t', '-c', config_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        assert "syntax is ok" in result.stderr, f"Nginx configuration test failed. Error: {result.stderr}"
        assert "test is successful" in result.stderr, f"Nginx configuration test was not fully successful. Output: {result.stderr}"
    finally:
        if os.path.exists(config_file):
            os.remove(config_file)
