import pytest
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
    version_integerized = int(version_info.replace('.', '0'))
    
    assert version_integerized >= 10800, f"Java version is too old: {version_info}. Requires Java 1.8.0 or higher."

def test_java_home_variable():
    java_home = os.getenv('JAVA_HOME')
    assert java_home, "JAVA_HOME environment variable is not set"
    assert os.path.isdir(java_home), f"JAVA_HOME path does not exist: {java_home}"
    assert os.path.isfile(os.path.join('/bin', 'java')), f"Java executable not found"

def test_run_jar():
    jar_path = 'data/HelloWorld.jar'
    result = subprocess.run(['java', '-jar', jar_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, f"Failed to run JAR file: {result.stderr}"
    assert "Hello world from HelloWorld.jar" in result.stdout, "JAR file did not produce expected output"
