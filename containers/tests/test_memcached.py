import pytest
import subprocess
import socket
from pymemcache.client.base import Client
from pymemcache.exceptions import MemcacheUnexpectedCloseError


MEMCACHED_HOST = "localhost"
MEMCACHED_PORT = 11211

@pytest.fixture
def memcached_client():
    """Fixture to create and cleanup memcached client"""
    client = Client((MEMCACHED_HOST, MEMCACHED_PORT))
    yield client
    try:
        client.flush_all()
    except:
        pass
    client.close()

def test_memcached_installed():
    """Test if memcached binary is installed"""
    result = subprocess.run(
        ['which', 'memcached'], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        text=True
    )
    assert result.returncode == 0, "Memcached is not installed or 'memcached' command is not found."
    assert "/memcached" in result.stdout, "Memcached binary not found in PATH."

def test_memcached_version():
    """Test memcached version"""
    result = subprocess.run(
        ['memcached', '-h'], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        text=True
    )
    output = result.stdout + result.stderr
    assert "memcached" in output.lower(), "Unable to get memcached version information."

def test_memcached_port_listening():
    """Test if memcached is listening on the default port"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        result = sock.connect_ex((MEMCACHED_HOST, MEMCACHED_PORT))
        assert result == 0, f"Memcached is not listening on port {MEMCACHED_PORT}."
    finally:
        sock.close()

def test_memcached_connection(memcached_client):
    """Test basic connection to memcached"""
    try:
        stats = memcached_client.stats()
        assert stats is not None, "Failed to connect to memcached."
        assert b'version' in stats, "Memcached stats missing version information."
    except Exception as e:
        pytest.fail(f"Failed to connect to memcached: {str(e)}")

def test_memcached_set_value(memcached_client):
    """Test setting a value in memcached"""
    try:
        result = memcached_client.set('test_key', 'test_value')
        assert result is True, "Failed to set value in memcached."
    except Exception as e:
        pytest.fail(f"Failed to set value in memcached: {str(e)}")

def test_memcached_get_value(memcached_client):
    """Test getting a value from memcached"""
    try:
        memcached_client.set('test_key', 'test_value')
        value = memcached_client.get('test_key')
        assert value is not None, "Failed to retrieve value from memcached."
        assert value == b'test_value', f"Expected b'test_value', got {value}"
    except Exception as e:
        pytest.fail(f"Failed to get value from memcached: {str(e)}")

def test_memcached_get_nonexistent_key(memcached_client):
    """Test getting a non-existent key"""
    try:
        value = memcached_client.get('nonexistent_key')
        assert value is None, "Non-existent key should return None."
    except Exception as e:
        pytest.fail(f"Failed to get non-existent key: {str(e)}")

def test_memcached_delete_value(memcached_client):
    """Test deleting a value from memcached"""
    try:
        memcached_client.set('test_key', 'test_value')
        result = memcached_client.delete('test_key')
        assert result is True, "Failed to delete value from memcached."
        
        value = memcached_client.get('test_key')
        assert value is None, "Key still exists after deletion."
    except Exception as e:
        pytest.fail(f"Failed to delete value from memcached: {str(e)}")

def test_memcached_add_value(memcached_client):
    """Test adding a value (only if key doesn't exist)"""
    try:
        result = memcached_client.set('add_key', 'add_value')
        assert result is True, "Failed to set value to memcached."
        
        result = memcached_client.add('add_key', 'new_value')
        assert result is True, "Failed to add new_value on existing one."
        
        value = memcached_client.get('add_key')
        assert value == b'add_value', "Original value was changed by add operation."
    except Exception as e:
        pytest.fail(f"Failed to add value in memcached: {str(e)}")

def test_memcached_replace_value(memcached_client):
    """Test replacing a value (only if key exists)"""
    try:
        result = memcached_client.set('replace_key', 'original_value')
        assert result is True, "Faile to set replace_key."
                
        result = memcached_client.replace('replace_key', 'new_value')
        assert result is True, "Failed to replace existing value."
        
        value = memcached_client.get('replace_key')
        assert value == b'new_value', f"Expected b'new_value', got {value}"
    except Exception as e:
        pytest.fail(f"Failed to replace value in memcached: {str(e)}")

def test_memcached_increment(memcached_client):
    """Test incrementing a numeric value"""
    try:
        memcached_client.set('counter', '10')
        new_value = memcached_client.incr('counter', 5)
        assert new_value == 15, f"Expected 15, got {new_value}"
        
        value = memcached_client.get('counter')
        assert value == b'15', f"Expected b'15', got {value}"
    except Exception as e:
        pytest.fail(f"Failed to increment value in memcached: {str(e)}")

def test_memcached_decrement(memcached_client):
    """Test decrementing a numeric value"""
    try:
        memcached_client.set('counter', '20')
        new_value = memcached_client.decr('counter', 7)
        assert new_value == 13, f"Expected 13, got {new_value}"
        
        value = memcached_client.get('counter')
        assert value == b'13', f"Expected b'13', got {value}"
    except Exception as e:
        pytest.fail(f"Failed to decrement value in memcached: {str(e)}")

def test_memcached_expiration(memcached_client):
    """Test value expiration"""
    import time
    try:
        memcached_client.set('expire_key', 'expire_value', expire=2)
        
        value = memcached_client.get('expire_key')
        assert value == b'expire_value', "Value should exist immediately after setting."
        
        time.sleep(3)
        
        value = memcached_client.get('expire_key')
        assert value is None, "Value should have expired."
    except Exception as e:
        pytest.fail(f"Failed to test expiration in memcached: {str(e)}")

def test_memcached_flush_all(memcached_client):
    """Test flushing all values from memcached"""
    try:
        memcached_client.set('key1', 'value1')
        memcached_client.set('key2', 'value2')
        memcached_client.set('key3', 'value3')
        
        result = memcached_client.flush_all()
        assert result is True, "Failed to flush memcached."
        
        assert memcached_client.get('key1') is None, "key1 should be deleted after flush."
        assert memcached_client.get('key2') is None, "key2 should be deleted after flush."
        assert memcached_client.get('key3') is None, "key3 should be deleted after flush."
    except Exception as e:
        pytest.fail(f"Failed to flush memcached: {str(e)}")

def test_memcached_multiple_keys(memcached_client):
    """Test setting and getting multiple keys"""
    try:
        test_data = {
            'key1': 'value1',
            'key2': 'value2',
            'key3': 'value3',
            'key4': 'value4',
            'key5': 'value5'
        }
        
        for key, value in test_data.items():
            memcached_client.set(key, value)
        
        for key, expected_value in test_data.items():
            value = memcached_client.get(key)
            assert value == expected_value.encode(), f"Expected {expected_value.encode()}, got {value}"
    except Exception as e:
        pytest.fail(f"Failed to handle multiple keys in memcached: {str(e)}")

def test_memcached_large_value(memcached_client):
    """Test storing and retrieving a large value"""
    try:
        large_value = 'x' * 10000
        memcached_client.set('large_key', large_value)
        
        retrieved_value = memcached_client.get('large_key')
        assert retrieved_value == large_value.encode(), "Failed to retrieve large value correctly."
        assert len(retrieved_value) == 10000, f"Expected 10000 bytes, got {len(retrieved_value)}"
    except Exception as e:
        pytest.fail(f"Failed to handle large value in memcached: {str(e)}")

def test_memcached_binary_data(memcached_client):
    """Test storing and retrieving binary data"""
    try:
        binary_data = bytes([0, 1, 2, 3, 4, 5, 255, 254, 253])
        memcached_client.set('binary_key', binary_data)
        
        retrieved_data = memcached_client.get('binary_key')
        assert retrieved_data == binary_data, "Failed to retrieve binary data correctly."
    except Exception as e:
        pytest.fail(f"Failed to handle binary data in memcached: {str(e)}")

def test_memcached_stats(memcached_client):
    """Test getting memcached statistics"""
    try:
        stats = memcached_client.stats()
        assert stats is not None, "Failed to get memcached stats."
        assert b'curr_items' in stats, "Stats missing curr_items."
        assert b'total_items' in stats, "Stats missing total_items."
        assert b'bytes' in stats, "Stats missing bytes."
        assert b'cmd_get' in stats, "Stats missing cmd_get."
        assert b'cmd_set' in stats, "Stats missing cmd_set."
    except Exception as e:
        pytest.fail(f"Failed to get memcached stats: {str(e)}")
