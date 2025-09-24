# test_openldap_image.py
import os
import subprocess
import time
import pytest

LDAP_URI = "ldap://127.0.0.1:389"
ADMIN_PASSWORD = os.getenv("LDAP_ADMIN_PASSWORD")
LDAP_DOMAIN = os.getenv("LDAP_DOMAIN", "example.org")
LDAP_BASE_DN = ",".join([f"dc={part}" for part in LDAP_DOMAIN.split('.')])
LDAP_ADMIN_DN = f"cn=admin,{LDAP_BASE_DN}"
LDAP_DATA_DIR = os.getenv("LDAP_DATA_DIR", "/var/lib/ldap")
LDAP_CONF_DIR = os.getenv("LDAP_CONF_DIR", "/etc/ldap")

@pytest.fixture(scope="session", autouse=True)
def wait_for_ldap_service():
    max_attempts = 15
    wait_seconds = 2

    for attempt in range(max_attempts):
        print(f"Attempting to connect to LDAP server... (Attempt {attempt + 1}/{max_attempts})")
        try:
            cmd = ["ldapsearch", "-x", "-H", LDAP_URI, "-b", "", "-s", "base", "(objectClass=*)"]
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            print("LDAP server is ready.")
            return
        except (subprocess.CalledProcessError, FileNotFoundError):
            time.sleep(wait_seconds)

    pytest.fail(f"LDAP server did not become ready after {max_attempts * wait_seconds} seconds.")

def test_binaries_exist():
    binaries = ["slapd", "slapadd", "slaptest", "ldapsearch"]
    for binary in binaries:
        subprocess.run(["which", binary], check=True, capture_output=True)

def test_slapd_process_is_running_as_openldap_user():
    pgrep_proc = subprocess.run(["pgrep", "-x", "slapd"], check=True, capture_output=True, text=True)
    pid = pgrep_proc.stdout.strip()
    assert pid, "slapd process not found"

    ps_proc = subprocess.run(["ps", "-o", "user=", "-p", pid], check=True, capture_output=True, text=True)
    user = ps_proc.stdout.strip()
    assert user == "openldap"

def test_ldap_port_is_listening():
    try:
        result = subprocess.run(['ss', '-tuln'], capture_output=True, text=True, check=True)
        
        port_is_listening = False
        for line in result.stdout.splitlines():
            if "LISTEN" in line and f":389" in line:
                port_is_listening = True
                break
        
        assert port_is_listening, f"Port 389 was not found in a 'LISTEN' state."

    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        pytest.fail(f"Failed to check listening ports with 'ss': {e}")

def test_directory_permissions():
    paths_to_check = [LDAP_DATA_DIR, LDAP_CONF_DIR, "/var/run/slapd"]
    for path in paths_to_check:
        stat_proc = subprocess.run(["stat", "-c", "%U:%G", path], check=True, capture_output=True, text=True)
        permissions = stat_proc.stdout.strip()
        assert permissions == "openldap:openldap"

def test_anonymous_root_dse_search():
    cmd = ["ldapsearch", "-x", "-H", LDAP_URI, "-b", "", "-s", "base", "(objectClass=*)", "namingContexts"]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    assert f"namingContexts: {LDAP_BASE_DN}" in result.stdout

@pytest.mark.skipif(not ADMIN_PASSWORD, reason="LDAP_ADMIN_PASSWORD env var is not set")
def test_authenticated_search_as_admin():
    cmd = [
        "ldapsearch", "-x",
        "-H", LDAP_URI,
        "-D", LDAP_ADMIN_DN,
        "-w", ADMIN_PASSWORD,
        "-b", LDAP_BASE_DN,
        "-s", "base"
    ]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    assert f"dn: {LDAP_BASE_DN}" in result.stdout