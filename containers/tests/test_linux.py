import time
import pytest
import subprocess


def test_uname_output():
    result = subprocess.run(['uname', '-a'], capture_output=True, text=True, check=True)
    assert 'Linux' in result.stdout, "Output of 'uname -a' does not contain 'Linux'"


def test_cpu_usage_with_retry():
    max_retries = 3
    retry_delays = [60, 120, 300]
    attempt = 0

    while attempt <= max_retries:
        try:
            result = subprocess.run(['grep', 'cpu ', '/proc/stat'],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, text=True,
                                    check=True)
            cpu_times = list(map(int, result.stdout.split()[1:]))
            idle_time = cpu_times[3]
            total_time = sum(cpu_times)
            cpu_usage = (1 - idle_time / total_time) * 100
            assert cpu_usage < 90, f"High CPU usage: {cpu_usage:.2f}%"
            return  # Test passed, exit the function
        except (AssertionError, subprocess.CalledProcessError) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            attempt += 1
            if attempt <= max_retries:
                wait_time = retry_delays[attempt - 1]
                print(f"Test failed on attempt {attempt}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise  # All retries failed, raise the last exception


def test_disk_usage():
    result = subprocess.run(['df', '-h', '/'], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True)
    lines = result.stdout.splitlines()
    root_info = lines[1].split()
    used_percent = int(root_info[4].replace('%', ''))
    assert used_percent < 90, f"High disk usage on the root partition: {used_percent}%"
