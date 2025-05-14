import pytest
import subprocess
import os


def test_maven_installed():
    result = subprocess.run(['mvn', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Maven is not installed or not found in system PATH"
    assert "Apache Maven" in result.stdout, "Unexpected output from 'mvn --version'"


def test_maven_home_variable():
    maven_home = os.getenv('MAVEN_HOME')
    assert maven_home, "MAVEN_HOME environment variable is not set"
    assert os.path.isdir(maven_home), f"MAVEN_HOME path does not exist: {maven_home}"
    exec_path = os.path.join(maven_home, 'bin', 'mvn')
    assert os.path.isfile(exec_path), f"Maven executable not found at {exec_path}"


def test_maven_help_command():
    result = subprocess.run(['mvn', 'help:help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, f"'mvn help:help' command failed: {result.stderr}"
    assert "help:help" in result.stdout, "Help command did not produce expected output"


def test_maven_create_simple_project(tmp_path):
    group_id = "com.example"
    artifact_id = "simple-app"
    subprocess.run(['mvn', 'archetype:generate',
                      f'-DgroupId={group_id}',
                      f'-DartifactId={artifact_id}',
                      '-DarchetypeArtifactId=maven-archetype-quickstart',
                      '-DinteractiveMode=false'],
                     cwd=tmp_path, check=True)
    project_path = tmp_path / artifact_id
    assert os.path.isdir(project_path), f"Project directory not created at {project_path}"
    assert os.path.isfile(project_path / 'pom.xml'), "pom.xml not found in the created project"
