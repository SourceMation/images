import pytest
import subprocess
import os
from pathlib import Path


def test_go_version():
    result = subprocess.run(['go', 'version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Failed to retrieve Go version"
    version_output = result.stdout.strip()
    assert version_output.startswith("go version go"), f"Unexpected Go version: {version_output}"


def test_go_basic_compile():
    tmp_path = Path("/tmp/")
    go_file = tmp_path / "hello.go"
    go_file.write_text("""
package main

import "fmt"

func main() {
    fmt.Println("Hello, Go!")
}
""")
    os.chdir(tmp_path)
    result = subprocess.run(['go', 'build', str(go_file)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Failed to compile basic Go program"

    executable = tmp_path / "hello"

    assert executable.exists(), "Compiled executable not found"

    result = subprocess.run([str(executable)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Failed to run compiled Go program"
    assert result.stdout.strip() == "Hello, Go!", "Unexpected output from Go program"


def test_go_mod_init():
    tmp_path = Path("/tmp/") / "gomodtest"
    tmp_path.mkdir(exist_ok=True)
    os.chdir(tmp_path)
    result = subprocess.run(['go', 'mod', 'init', 'testmodule'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Failed to initialize Go module"
    assert (tmp_path / "go.mod").exists(), "go.mod file not created"


def test_go_get_module():
    tmp_path = Path("/tmp/") / "gomodgettest"
    tmp_path.mkdir(exist_ok=True)
    os.chdir(tmp_path)

    subprocess.run(['go', 'mod', 'init', 'testmodule2'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    result = subprocess.run(['go', 'get', 'rsc.io/quote'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Failed to get Go module"
    assert (tmp_path / "go.sum").exists(), "go.sum file not created"


def test_go_env():
    result = subprocess.run(['go', 'env', 'GOOS'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Failed to get GOOS from go env"
    assert result.stdout.strip(), "GOOS not set"


def test_go_list_packages():
    result = subprocess.run(['go', 'list', 'std'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Failed to list standard packages"
    assert "fmt" in result.stdout, "fmt package not found in standard packages"
