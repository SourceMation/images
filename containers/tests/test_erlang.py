import pytest
import subprocess
from pathlib import Path


def test_erlang_executable():
    result = subprocess.run(['erl', '-noshell', '-eval', 'halt().'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Erlang executable 'erl' not found or not working"


def test_erlang_otp_available():
    tmp_path = Path("/tmp/")
    script_content = """
    -module(test_otp).
    -export([start/0]).

    start() ->
        io:format("~s~n", [erlang:system_info(otp_release)]),
        init:stop().
    """
    script_file = tmp_path / "test_otp.erl"
    script_file.write_text(script_content)

    compile_result = subprocess.run(['erlc', str(script_file)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=tmp_path)
    assert compile_result.returncode == 0, f"Failed to compile Erlang script: {compile_result.stderr}"

    result = subprocess.run(['erl', '-noshell', '-s', script_file.stem, 'start'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=tmp_path)
    assert result.returncode == 0, "Failed to run Erlang script to check OTP"
    assert result.stdout.strip(), "OTP release information not found"


def test_erlang_basic_functionality():
    tmp_path = Path("/tmp/")
    script_content = """
    -module(hello_erlang).
    -export([start/0]).

    start() ->
        io:format("Hello from Erlang script!~n", []),
        init:stop().
    """
    script_file = tmp_path / "hello_erlang.erl"
    script_file.write_text(script_content)

    compile_result = subprocess.run(['erlc', str(script_file)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=tmp_path)
    assert compile_result.returncode == 0, f"Failed to compile Erlang script: {compile_result.stderr}"

    result = subprocess.run(['erl', '-noshell', '-s', script_file.stem, 'start'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=tmp_path)
    assert result.returncode == 0, "Failed to run basic Erlang script from file"
    assert "Hello from Erlang script!" in result.stdout.strip(), "Unexpected output from basic Erlang script"


def test_erlang_run_script_file():
    tmp_path = Path("/tmp/")
    script_content = """
    -module(another_script).
    -export([start/0]).

    start() ->
        io:format("This is another Erlang script.~n", []),
        init:stop().
    """
    script_file = tmp_path / "another_script.erl"
    script_file.write_text(script_content)

    compile_result = subprocess.run(['erlc', str(script_file)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=tmp_path)
    assert compile_result.returncode == 0, f"Failed to compile Erlang script: {compile_result.stderr}"

    result = subprocess.run(['erl', '-noshell', '-s', script_file.stem, 'start'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=tmp_path)
    assert result.returncode == 0, "Failed to run another Erlang script from file"
    assert "This is another Erlang script." in result.stdout.strip(), "Unexpected output from another Erlang script"

