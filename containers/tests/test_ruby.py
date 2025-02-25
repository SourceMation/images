import pytest
import subprocess
import os

def test_ruby_installed():
    result = subprocess.run(['ruby', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Ruby is not installed or not found in system PATH"
    assert "ruby" in result.stdout, f"Unexpected output from 'ruby -v': {result.stdout}"

def test_ruby_version():
    result = subprocess.run(['ruby', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Ruby is not installed or not found in system PATH"
    
    version_info = result.stdout.split()[1]
    major_version = int(version_info.split('.')[0])
    minor_version = int(version_info.split('.')[1])
    
    assert (major_version == 2 and minor_version >= 7) or (major_version > 2), \
        f"Ruby version is too old: {version_info}. Requires Ruby 2.7 or higher."

def test_bundler_installed():
    result = subprocess.run(['gem', 'list', 'bundler'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Failed to check installed gems"
    assert "bundler" in result.stdout, "Bundler is not installed"

def test_install_gem():
    install_result = subprocess.run(['gem', 'install', 'sinatra'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    assert install_result.returncode == 0, f"Failed to install gem 'sinatra': {install_result.stderr}"
    
    list_result = subprocess.run(['gem', 'list', 'sinatra'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert list_result.returncode == 0, "Failed to list installed gems"
    assert "sinatra" in list_result.stdout, "Gem 'sinatra' was not installed successfully"
    
    subprocess.run(['gem', 'uninstall', 'sinatra', '-a', '-x'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def test_run_simple_ruby_program():
    ruby_program = """
    puts 'Ruby is working!'
    """
    with open('testRuby.rb', 'w') as f:
        f.write(ruby_program)
    
    result = subprocess.run(['ruby', 'testRuby.rb'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    assert result.returncode == 0, f"Failed to run Ruby program: {result.stderr}"
    assert "Ruby is working!" in result.stdout, "Ruby program did not produce expected output"

    os.remove('testRuby.rb')

def test_irb():
    irb_command = "echo 'puts \"IRB is working!\"; exit' | irb --simple-prompt -r irb/completion"
    result = subprocess.run(irb_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    assert result.returncode == 0, f"Failed to run IRB: {result.stderr}"
    assert "IRB is working!" in result.stdout, "IRB did not produce expected output"

def test_gemspec_processing():
    gemspec_content = """
    Gem::Specification.new do |s|
      s.name        = 'test_gem'
      s.version     = '0.1.0'
      s.summary     = 'A simple test gem'
      s.authors     = ['Jan Kowalski']
      s.email       = ['jan.kowalski@example.com']
      s.files       = []
    end
    """
    with open('test_gem.gemspec', 'w') as f:
        f.write(gemspec_content)
    
    result = subprocess.run(['gem', 'build', 'test_gem.gemspec'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    assert result.returncode == 0, f"Failed to build gem from gemspec: {result.stderr}"
    assert "Successfully built RubyGem" in result.stdout, "Gemspec did not build as expected"

    os.remove('test_gem.gemspec')
    os.remove('test_gem-0.1.0.gem')

def test_ruby_unicode():
    ruby_program = """
    puts "Unicode test: Ω α ω"
    """
    with open('testUnicodeRuby.rb', 'w') as f:
        f.write(ruby_program)
    
    result = subprocess.run(['ruby', 'testUnicodeRuby.rb'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    assert result.returncode == 0, f"Failed to run Ruby program: {result.stderr}"
    assert "Unicode test: Ω α ω" in result.stdout, "Ruby program did not produce expected Unicode output"

    os.remove('testUnicodeRuby.rb')
