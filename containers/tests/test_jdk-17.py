import subprocess
import os


def test_java_installed():
    result = subprocess.run(['java', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Java is not installed or not found in system PATH"
    assert "version" in result.stderr, "Unexpected output from 'java -version'"


def test_java_version():
    result = subprocess.run(['java', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Java is not installed or not found in system PATH"

    version_line = result.stderr.splitlines()[0]
    version_info = version_line.split(' ')[2].strip('"')
    assert version_info.startswith('17.'), f"Expected Java version to start with '17.', but got '{version_info}'"


def test_java_home_variable():
    java_home = os.getenv('JAVA_HOME')
    assert java_home, "JAVA_HOME environment variable is not set"
    assert os.path.isdir(java_home), f"JAVA_HOME path does not exist: {java_home}"
    exec_path = os.path.join(java_home, 'bin', 'java')
    assert os.path.isfile(exec_path), f"Java executable not found at {exec_path}"


def test_run_jar():
    jar_path = 'data/HelloWorld.jar'
    result = subprocess.run(['java', '-jar', jar_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, f"Failed to run JAR file: {result.stderr}"
    assert "Hello world from HelloWorld.jar" in result.stdout, "JAR file did not produce expected output"


def test_javac_installed():
    result = subprocess.run(['javac', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Java compiler (javac) is not installed or not found in system PATH"
    assert "javac" in result.stdout, "Unexpected output from 'javac -version'"


def test_compile_java_app():
    java_file = 'data/MyApp.java'
    output_dir = 'data'
    compile_command = ['javac', '-d', output_dir, java_file]
    result = subprocess.run(compile_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, f"Failed to compile Java application: {result.stderr}"
    assert os.path.isfile(os.path.join(output_dir, 'MyApp.class')), "Compiled class file not found"


def test_run_compiled_java_app():
    class_path = 'data'
    run_command = ['java', '-cp', class_path, 'MyApp']
    result = subprocess.run(run_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, f"Failed to run compiled Java application: {result.stderr}"
    assert "Hello from JAVA!" in result.stdout, "Compiled Java application did not produce expected output"
