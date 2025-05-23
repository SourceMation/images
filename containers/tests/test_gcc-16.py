import pytest
import subprocess
import os

def test_gcc_installed():
    result = subprocess.run(['gcc', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "GCC is not installed or not found in system PATH"
    assert "free software foundation" in result.stdout.lower(), "Unexpected output from 'gcc --version'"

def test_gcc_version():
    result = subprocess.run(['gcc', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "GCC is not installed or not found in system PATH"

    version_line = result.stdout.splitlines()[0]
    version_info = version_line.split(' ')[2]
    major_version = int(version_info.split('.')[0])

    assert major_version == 16, f"GCC version is not 16: {version_info}"

def test_gpp_installed():
    result = subprocess.run(['g++', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "G++ is not installed or not found in system PATH"
    assert "free software foundation" in result.stdout.lower(), "Unexpected output from 'g++ --version'"

def test_gpp_version():
    result = subprocess.run(['g++', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "G++ is not installed or not found in system PATH"

    version_line = result.stdout.splitlines()[0]
    version_info = version_line.split(' ')[2]
    major_version = int(version_info.split('.')[0])

    assert major_version == 16, f"G++ version is not 16: {version_info}"

def test_compile_c_program():
    c_code = '''
    #include <stdio.h>

    int main() {
        printf("Hello from GCC!\\n");
        return 0;
    }
    '''
    with open("hello.c", "w") as f:
        f.write(c_code)

    compile_result = subprocess.run(['gcc', 'hello.c', '-o', 'hello'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert compile_result.returncode == 0, f"Failed to compile C program: {compile_result.stderr}"
    assert os.path.exists('hello'), "Compiled executable 'hello' not found"

    run_result = subprocess.run(['./hello'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    assert "Hello from GCC!" in run_result.stdout, "Compiled program did not produce expected output"

    os.remove("hello.c")
    os.remove("hello")

def test_compile_cpp_program():
    cpp_code = '''
    #include <iostream>

    int main() {
        std::cout << "Hello from G++!" << std::endl;
        return 0;
    }
    '''
    with open("hello.cpp", "w") as f:
        f.write(cpp_code)

    compile_result = subprocess.run(['g++', 'hello.cpp', '-o', 'hellopp'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert compile_result.returncode == 0, f"Failed to compile C++ program: {compile_result.stderr}"
    assert os.path.exists('hellopp'), "Compiled executable 'hellopp' not found"

    run_result = subprocess.run(['./hellopp'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    assert "Hello from G++!" in run_result.stdout, "Compiled program did not produce expected output"

    os.remove("hello.cpp")
    os.remove("hellopp")

def test_gccgo_installed():
    result = subprocess.run(['gccgo', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "gccgo is not installed or not found in system PATH"
    assert "free software foundation" in result.stdout.lower(), "Unexpected output from 'gccgo --version'"

def test_compile_go_program():
    go_code = '''
    package main

    import "fmt"

    func main() {
        fmt.Println("Hello from GCC Go!")
    }
    '''
    with open("hello.go", "w") as f:
        f.write(go_code)

    compile_result = subprocess.run(['gccgo', 'hello.go', '-o', 'hellogo'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert compile_result.returncode == 0, f"Failed to compile Go program: {compile_result.stderr}"
    assert os.path.exists('hellogo'), "Compiled executable 'hellogo' not found"

    run_result = subprocess.run(['./hellogo'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    assert "Hello from GCC Go!" in run_result.stdout, "Compiled Go program did not produce expected output"

    os.remove("hello.go")
    os.remove("hellogo")

# There were tests for gccrs - rust compiler, but oh boy it's not ready yet: Date: 11 April 2025
