import pytest
import subprocess
import redis
import time

def test_redis_installed():
    result = subprocess.run(['redis-server', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Redis is not installed or redis-server command is not found."
    assert "Redis" in result.stdout, "Redis version output does not contain expected string."

def test_redis_connection():
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
    except redis.ConnectionError:
        pytest.fail("Failed to connect to Redis server.")
    assert r.ping() == True, "Ping to Redis server failed."

def test_redis_set_get():
    r = redis.Redis(host='localhost', port=6379, db=0)
    set_result = r.set('test_key', 'test_value')
    assert set_result == True, "Failed to set key in Redis."

    get_result = r.get('test_key')
    assert get_result == b'test_value', f"Expected 'test_value', got {get_result}."

def test_redis_flushdb():
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.set('test_key', 'test_value')
    assert r.get('test_key') == b'test_value', "Failed to add key before flush."

    r.flushdb()
    assert r.get('test_key') is None, "Key still exists after FLUSHDB operation."

def test_redis_expire_ttl():
    r = redis.Redis(host='localhost', port=6379, db=0)
    
    r.set('temp_key', 'temp_value')
    
    r.expire('temp_key', 1)
    
    ttl = r.ttl('temp_key')
    assert ttl == 1, f"Expected TTL of 1 second, but got {ttl}"
    
    time.sleep(2)
    
    assert r.get('temp_key') is None, "Key was not deleted after expiration."

def test_redis_list_operations():
    r = redis.Redis(host='localhost', port=6379, db=0)
    
    r.delete('my_list')
    
    r.lpush('my_list', 'element1')
    r.lpush('my_list', 'element2')
    r.lpush('my_list', 'element3')
    
    list_items = r.lrange('my_list', 0, -1)
    
    assert list_items == [b'element3', b'element2', b'element1'], f"Expected list ['element3', 'element2', 'element1'], but got {list_items}"

def test_redis_configuration():
    r = redis.Redis(host='localhost', port=6379, db=0)
    
    maxmemory = r.config_get('maxmemory')
    
    assert maxmemory['maxmemory'] == '0', f"Expected maxmemory to be '0', but got {maxmemory['maxmemory']}"
