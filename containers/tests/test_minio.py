import pytest
import subprocess
import requests
import time
import json
import os
import base64
import hashlib
from pathlib import Path
from xml.etree import ElementTree as ET

MINIO_HOST = "localhost"
MINIO_API_PORT = "9000"
MINIO_CONSOLE_PORT = "9001"
MINIO_API_URL = f"http://{MINIO_HOST}:{MINIO_API_PORT}"
MINIO_CONSOLE_URL = f"http://{MINIO_HOST}:{MINIO_CONSOLE_PORT}"

# Default credentials
MINIO_ROOT_USER = "minioadmin"
MINIO_ROOT_PASSWORD = "minioadmin"

def test_minio_binary_installed():
    """Test that MinIO binary is installed and accessible."""
    assert os.path.isfile("/usr/local/bin/minio"), "MinIO binary not found at /usr/local/bin/minio"
    assert os.access("/usr/local/bin/minio", os.X_OK), "MinIO binary is not executable"

def test_minio_version():
    """Test that MinIO returns version information."""
    result = subprocess.run(['/usr/local/bin/minio', '--version'], 
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Failed to get MinIO version"
    assert "minio version RELEASE" in result.stdout, f"Unexpected version output: {result.stdout}"
    assert "RELEASE.2025-09-07T16-13-09Z" in result.stdout, "Expected specific version not found"

def test_minio_help():
    """Test that MinIO help command works."""
    result = subprocess.run(['/usr/local/bin/minio', '--help'], 
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Failed to get MinIO help"
    assert "server" in result.stdout, "Server command not found in help"
    assert "High Performance Object Storage" in result.stdout, "Expected help text not found"

def test_data_directory_exists():
    """Test that the data directory exists and has correct permissions."""
    data_dir = "/data"
    assert os.path.exists(data_dir), f"Data directory {data_dir} does not exist"
    assert os.path.isdir(data_dir), f"{data_dir} exists but is not a directory"
    
    # Check permissions for nobody user
    stat_info = os.stat(data_dir)
    # Check that directory has write permissions for group or others
    group_write = bool(stat_info.st_mode & 0o020)
    other_write = bool(stat_info.st_mode & 0o002)
    assert group_write or other_write, f"Data directory {data_dir} is not writable by nobody user"

def test_license_files_exist():
    """Test that license files exist."""
    license_file = "/LICENSE"
    notice_file = "/NOTICE"
    
    assert os.path.exists(license_file), "LICENSE file not found"
    assert os.path.exists(notice_file), "NOTICE file not found"

def test_minio_server_help():
    """Test that MinIO server command shows help."""
    result = subprocess.run(['/usr/local/bin/minio', 'server', '--help'], 
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "Failed to get MinIO server help"
    assert "--address" in result.stdout, "Address flag not found in help"
    assert "--console-address" in result.stdout, "Console address flag not found in help"

def test_minio_service_running():
    """Test that MinIO service is running and accessible."""
    max_retries = 15
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            response = requests.get(f"{MINIO_API_URL}/minio/health/live", timeout=5)
            if response.status_code == 200:
                return
        except requests.exceptions.RequestException:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                pytest.fail(f"Failed to connect to MinIO service after {max_retries} attempts")
    
    pytest.fail("MinIO service is not responding to health checks")

def test_minio_health_endpoints():
    """Test MinIO health endpoints."""
    # Test liveness probe
    try:
        response = requests.get(f"{MINIO_API_URL}/minio/health/live", timeout=10)
        assert response.status_code == 200, f"Liveness check failed with status {response.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to liveness endpoint: {e}")
    
    # Test readiness probe
    try:
        response = requests.get(f"{MINIO_API_URL}/minio/health/ready", timeout=10)
        assert response.status_code == 200, f"Readiness check failed with status {response.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to readiness endpoint: {e}")

def test_minio_console_accessible():
    """Test that MinIO console web interface is accessible."""
    try:
        response = requests.get(f"{MINIO_CONSOLE_URL}/", timeout=10)
        assert response.status_code == 200, f"Console failed with status {response.status_code}"
        
        # Check for basic HTML content
        content = response.text.lower()
        assert "<html" in content, "Response should be valid HTML"
        # Console should redirect or show login page
        assert "minio" in content or "login" in content, "Console should contain MinIO or login references"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to access MinIO console: {e}")

def test_minio_s3_list_buckets():
    """Test S3 API list buckets operation."""
    try:
        response = requests.get(f"{MINIO_API_URL}/", 
                              auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD), 
                              timeout=10)
        
        # Should return XML with ListAllMyBucketsResult
        assert response.status_code == 200, f"List buckets failed with status {response.status_code}"
        assert "application/xml" in response.headers.get("Content-Type", ""), "Response should be XML"
        
        # Parse XML to verify structure
        root = ET.fromstring(response.text)
        assert root.tag.endswith("ListAllMyBucketsResult"), "Response should be ListAllMyBucketsResult"
        
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to list buckets: {e}")
    except ET.ParseError as e:
        pytest.fail(f"Failed to parse XML response: {e}")

def test_minio_s3_create_bucket():
    """Test S3 API bucket creation."""
    bucket_name = "test-bucket-12345"
    
    try:
        # Create bucket
        response = requests.put(f"{MINIO_API_URL}/{bucket_name}", 
                              auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD), 
                              timeout=10)
        
        # Should return 200 for successful creation
        assert response.status_code == 200, f"Bucket creation failed with status {response.status_code}"
        
        # Verify bucket exists by listing buckets
        response = requests.get(f"{MINIO_API_URL}/", 
                              auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD), 
                              timeout=10)
        
        assert bucket_name in response.text, f"Created bucket {bucket_name} not found in bucket list"
        
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to create bucket: {e}")
    finally:
        # Cleanup: delete test bucket
        try:
            requests.delete(f"{MINIO_API_URL}/{bucket_name}", 
                          auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD), 
                          timeout=5)
        except:
            pass  # Ignore cleanup failures

def test_minio_s3_put_get_object():
    """Test S3 API object upload and download."""
    bucket_name = "test-bucket-objects"
    object_name = "test-object.txt"
    test_data = b"Hello, MinIO! This is test data."
    
    try:
        # Create bucket first
        requests.put(f"{MINIO_API_URL}/{bucket_name}", 
                    auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD), 
                    timeout=10)
        
        # Upload object
        response = requests.put(f"{MINIO_API_URL}/{bucket_name}/{object_name}", 
                              data=test_data,
                              auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD), 
                              timeout=10)
        
        assert response.status_code == 200, f"Object upload failed with status {response.status_code}"
        
        # Download object
        response = requests.get(f"{MINIO_API_URL}/{bucket_name}/{object_name}", 
                              auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD), 
                              timeout=10)
        
        assert response.status_code == 200, f"Object download failed with status {response.status_code}"
        assert response.content == test_data, "Downloaded data doesn't match uploaded data"
        
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to upload/download object: {e}")
    finally:
        # Cleanup
        try:
            requests.delete(f"{MINIO_API_URL}/{bucket_name}/{object_name}", 
                          auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD))
            requests.delete(f"{MINIO_API_URL}/{bucket_name}", 
                          auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD))
        except:
            pass

def test_minio_metrics_endpoint():
    """Test MinIO Prometheus metrics endpoint."""
    try:
        response = requests.get(f"{MINIO_API_URL}/minio/v2/metrics/cluster", timeout=10)
        assert response.status_code == 200, f"Metrics endpoint failed with status {response.status_code}"
        
        metrics_text = response.text
        assert "minio_version_info" in metrics_text, "Version info metric not found"
        assert "minio_disk_storage_available_bytes" in metrics_text, "Storage metrics not found"
        
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to get metrics: {e}")

def test_minio_admin_info():
    """Test MinIO admin info endpoint."""
    try:
        response = requests.get(f"{MINIO_API_URL}/minio/admin/v3/info", 
                              auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD),
                              timeout=10)
        
        # Admin endpoints might require specific headers or authentication
        # Status code 200 or 403 both indicate the endpoint exists
        assert response.status_code in [200, 403, 401], f"Unexpected status code: {response.status_code}"
        
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to access admin info: {e}")

def test_minio_server_environment():
    """Test that MinIO server respects common environment variables."""
    # This test checks that the expected environment variable patterns exist
    # Note: In a container test, we can't easily change env vars and restart
    
    # Test that MINIO_ROOT_USER and MINIO_ROOT_PASSWORD are working
    # (implicitly tested by other S3 operations using these credentials)
    
    # Test server info to verify configuration
    try:
        response = requests.get(f"{MINIO_API_URL}/", 
                              auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD), 
                              timeout=10)
        assert response.status_code == 200, "Basic authentication with default credentials failed"
        
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Environment variable configuration test failed: {e}")

@pytest.mark.parametrize("endpoint", [
    "/minio/health/live",
    "/minio/health/ready",
    "/minio/v2/metrics/cluster"
])
def test_minio_operational_endpoints(endpoint):
    """Test various MinIO operational endpoints."""
    try:
        response = requests.get(f"{MINIO_API_URL}{endpoint}", timeout=10)
        # These endpoints should be accessible and return valid responses
        assert response.status_code in [200, 403], f"Endpoint {endpoint} failed with status {response.status_code}"
        
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to access endpoint {endpoint}: {e}")

def test_minio_cors_configuration():
    """Test CORS preflight request handling."""
    try:
        headers = {
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'PUT',
            'Access-Control-Request-Headers': 'Content-Type'
        }
        
        response = requests.options(f"{MINIO_API_URL}/test-bucket", 
                                  headers=headers,
                                  timeout=10)
        
        # CORS should be handled (200) or method not allowed (405)
        assert response.status_code in [200, 405, 403], f"CORS test failed with status {response.status_code}"
        
    except requests.exceptions.RequestException as e:
        pytest.fail(f"CORS configuration test failed: {e}")

def test_minio_multipart_upload_support():
    """Test that MinIO supports multipart upload initiation."""
    bucket_name = "test-multipart-bucket"
    object_name = "multipart-test.txt"
    
    try:
        # Create bucket
        requests.put(f"{MINIO_API_URL}/{bucket_name}", 
                    auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD))
        
        # Initiate multipart upload
        response = requests.post(f"{MINIO_API_URL}/{bucket_name}/{object_name}?uploads", 
                               auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD), 
                               timeout=10)
        
        assert response.status_code == 200, f"Multipart upload initiation failed with status {response.status_code}"
        assert "application/xml" in response.headers.get("Content-Type", ""), "Response should be XML"
        
        # Parse XML to get upload ID
        root = ET.fromstring(response.text)
        upload_id_element = root.find(".//{https://s3.amazonaws.com/doc/2006-03-01/}UploadId")
        assert upload_id_element is not None, "Upload ID not found in response"
        
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Multipart upload test failed: {e}")
    except ET.ParseError as e:
        pytest.fail(f"Failed to parse XML response: {e}")
    finally:
        # Cleanup
        try:
            requests.delete(f"{MINIO_API_URL}/{bucket_name}", 
                          auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD))
        except:
            pass

def test_minio_presigned_url_support():
    """Test MinIO's ability to handle presigned URL-style requests."""
    bucket_name = "test-presigned-bucket"
    
    try:
        # Create bucket
        requests.put(f"{MINIO_API_URL}/{bucket_name}", 
                    auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD))
        
        # Test a basic signed request (this tests the signature handling capability)
        # We'll use a simple HEAD request to test the infrastructure
        response = requests.head(f"{MINIO_API_URL}/{bucket_name}", 
                               auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD), 
                               timeout=10)
        
        assert response.status_code == 200, f"Bucket HEAD request failed with status {response.status_code}"
        
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Presigned URL support test failed: {e}")
    finally:
        # Cleanup
        try:
            requests.delete(f"{MINIO_API_URL}/{bucket_name}", 
                          auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD))
        except:
            pass

def test_minio_s3_compatibility():
    """Test S3 compatibility features."""
    try:
        # Test that MinIO responds with proper S3-compatible headers
        response = requests.head(f"{MINIO_API_URL}/", 
                               auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD), 
                               timeout=10)
        
        assert response.status_code == 200, f"S3 compatibility test failed with status {response.status_code}"
        
        # Check for S3-compatible server header
        server_header = response.headers.get("Server", "").lower()
        assert "minio" in server_header or "amazons3" in server_header.replace("-", "").replace(" ", ""), \
            f"Expected S3-compatible server header, got: {server_header}"
            
    except requests.exceptions.RequestException as e:
        pytest.fail(f"S3 compatibility test failed: {e}")

def test_minio_error_responses():
    """Test that MinIO returns proper error responses."""
    try:
        # Test accessing non-existent bucket
        response = requests.get(f"{MINIO_API_URL}/non-existent-bucket-12345", 
                              auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD), 
                              timeout=10)
        
        assert response.status_code == 404, f"Expected 404 for non-existent bucket, got {response.status_code}"
        
        # Test unauthorized access
        response = requests.get(f"{MINIO_API_URL}/", 
                              auth=("wrong-user", "wrong-password"), 
                              timeout=10)
        
        assert response.status_code in [401, 403], f"Expected 401/403 for wrong credentials, got {response.status_code}"
        
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Error response test failed: {e}")

def test_minio_content_types():
    """Test MinIO handles different content types correctly."""
    bucket_name = "test-content-types"
    
    try:
        # Create bucket
        requests.put(f"{MINIO_API_URL}/{bucket_name}", 
                    auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD))
        
        # Test different content types
        test_files = [
            ("test.txt", b"Hello World", "text/plain"),
            ("test.json", b'{"key": "value"}', "application/json"),
            ("test.xml", b"<root><item>value</item></root>", "application/xml")
        ]
        
        for filename, content, content_type in test_files:
            # Upload with specific content type
            headers = {"Content-Type": content_type}
            response = requests.put(f"{MINIO_API_URL}/{bucket_name}/{filename}", 
                                  data=content,
                                  headers=headers,
                                  auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD), 
                                  timeout=10)
            
            assert response.status_code == 200, f"Upload with content type {content_type} failed"
            
            # Verify content type is preserved
            response = requests.head(f"{MINIO_API_URL}/{bucket_name}/{filename}", 
                                   auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD), 
                                   timeout=10)
            
            returned_content_type = response.headers.get("Content-Type", "")
            assert content_type in returned_content_type, \
                f"Expected content type {content_type}, got {returned_content_type}"
        
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Content type test failed: {e}")
    finally:
        # Cleanup
        try:
            for filename, _, _ in test_files:
                requests.delete(f"{MINIO_API_URL}/{bucket_name}/{filename}", 
                              auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD))
            requests.delete(f"{MINIO_API_URL}/{bucket_name}", 
                          auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD))
        except:
            pass

def test_minio_storage_usage():
    """Test MinIO storage usage calculation."""
    bucket_name = "test-storage-usage"
    
    try:
        # Create bucket
        requests.put(f"{MINIO_API_URL}/{bucket_name}", 
                    auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD))
        
        # Upload a test file of known size
        test_data = b"A" * 1024  # 1KB file
        response = requests.put(f"{MINIO_API_URL}/{bucket_name}/test-file.txt", 
                              data=test_data,
                              auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD), 
                              timeout=10)
        
        assert response.status_code == 200, "Failed to upload test file for storage usage test"
        
        # Check if storage metrics are available
        response = requests.get(f"{MINIO_API_URL}/minio/v2/metrics/cluster", timeout=10)
        if response.status_code == 200:
            metrics = response.text
            assert "minio_disk_storage_used_bytes" in metrics, "Storage usage metrics not found"
        
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Storage usage test failed: {e}")
    finally:
        # Cleanup
        try:
            requests.delete(f"{MINIO_API_URL}/{bucket_name}/test-file.txt", 
                          auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD))
            requests.delete(f"{MINIO_API_URL}/{bucket_name}", 
                          auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD))
        except:
            pass

def test_minio_versioning_support():
    """Test that MinIO supports versioning configuration."""
    bucket_name = "test-versioning-bucket"
    
    try:
        # Create bucket
        requests.put(f"{MINIO_API_URL}/{bucket_name}", 
                    auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD))
        
        # Try to get versioning configuration
        response = requests.get(f"{MINIO_API_URL}/{bucket_name}?versioning", 
                              auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD), 
                              timeout=10)
        
        # Should return XML versioning configuration
        assert response.status_code == 200, f"Versioning endpoint failed with status {response.status_code}"
        assert "xml" in response.headers.get("Content-Type", "").lower(), "Versioning response should be XML"
        
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Versioning support test failed: {e}")
    finally:
        # Cleanup
        try:
            requests.delete(f"{MINIO_API_URL}/{bucket_name}", 
                          auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD))
        except:
            pass

def test_minio_lifecycle_support():
    """Test that MinIO supports lifecycle configuration."""
    bucket_name = "test-lifecycle-bucket"
    
    try:
        # Create bucket
        requests.put(f"{MINIO_API_URL}/{bucket_name}", 
                    auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD))
        
        # Try to get lifecycle configuration
        response = requests.get(f"{MINIO_API_URL}/{bucket_name}?lifecycle", 
                              auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD), 
                              timeout=10)
        
        # Should return 404 (no lifecycle config) or 200 (with config)
        assert response.status_code in [200, 404], \
            f"Lifecycle endpoint failed with status {response.status_code}"
        
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Lifecycle support test failed: {e}")
    finally:
        # Cleanup
        try:
            requests.delete(f"{MINIO_API_URL}/{bucket_name}", 
                          auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD))
        except:
            pass

def test_minio_encryption_support():
    """Test MinIO's encryption support capabilities."""
    bucket_name = "test-encryption-bucket"
    
    try:
        # Create bucket
        requests.put(f"{MINIO_API_URL}/{bucket_name}", 
                    auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD))
        
        # Test server-side encryption headers
        headers = {
            "x-amz-server-side-encryption": "AES256"
        }
        
        response = requests.put(f"{MINIO_API_URL}/{bucket_name}/encrypted-test.txt", 
                              data=b"Encrypted test data",
                              headers=headers,
                              auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD), 
                              timeout=10)
        
        # Should accept encryption headers (200) or ignore them gracefully
        assert response.status_code == 200, f"Encryption test failed with status {response.status_code}"
        
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Encryption support test failed: {e}")
    finally:
        # Cleanup
        try:
            requests.delete(f"{MINIO_API_URL}/{bucket_name}/encrypted-test.txt", 
                          auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD))
            requests.delete(f"{MINIO_API_URL}/{bucket_name}", 
                          auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD))
        except:
            pass

def test_minio_large_file_support():
    """Test MinIO's handling of larger files."""
    bucket_name = "test-large-file-bucket"
    object_name = "large-test-file.bin"
    
    try:
        # Create bucket
        requests.put(f"{MINIO_API_URL}/{bucket_name}", 
                    auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD))
        
        # Create a 1MB test file
        large_data = b"A" * (1024 * 1024)  # 1MB
        
        response = requests.put(f"{MINIO_API_URL}/{bucket_name}/{object_name}", 
                              data=large_data,
                              auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD), 
                              timeout=30)  # Longer timeout for large file
        
        assert response.status_code == 200, f"Large file upload failed with status {response.status_code}"
        
        # Verify we can retrieve file information
        response = requests.head(f"{MINIO_API_URL}/{bucket_name}/{object_name}", 
                               auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD), 
                               timeout=10)
        
        assert response.status_code == 200, "Failed to get large file metadata"
        
        content_length = int(response.headers.get("Content-Length", "0"))
        assert content_length == len(large_data), \
            f"Content-Length mismatch: expected {len(large_data)}, got {content_length}"
        
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Large file support test failed: {e}")
    finally:
        # Cleanup
        try:
            requests.delete(f"{MINIO_API_URL}/{bucket_name}/{object_name}", 
                          auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD))
            requests.delete(f"{MINIO_API_URL}/{bucket_name}", 
                          auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD))
        except:
            pass

def test_minio_concurrent_operations():
    """Test MinIO's handling of concurrent operations."""
    import threading
    import queue
    
    bucket_name = "test-concurrent-bucket"
    results = queue.Queue()
    
    def upload_test_file(file_index):
        try:
            object_name = f"concurrent-test-{file_index}.txt"
            test_data = f"Test data from thread {file_index}".encode()
            
            response = requests.put(f"{MINIO_API_URL}/{bucket_name}/{object_name}", 
                                  data=test_data,
                                  auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD), 
                                  timeout=10)
            
            results.put(("upload", file_index, response.status_code == 200))
            
            # Also test download
            response = requests.get(f"{MINIO_API_URL}/{bucket_name}/{object_name}", 
                                  auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD), 
                                  timeout=10)
            
            results.put(("download", file_index, response.status_code == 200 and response.content == test_data))
            
        except Exception as e:
            results.put(("error", file_index, str(e)))
    
    try:
        # Create bucket
        requests.put(f"{MINIO_API_URL}/{bucket_name}", 
                    auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD))
        
        # Start multiple concurrent uploads
        threads = []
        num_threads = 5
        
        for i in range(num_threads):
            thread = threading.Thread(target=upload_test_file, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join(timeout=30)
        
        # Check results
        upload_successes = 0
        download_successes = 0
        errors = []
        
        while not results.empty():
            try:
                operation, file_index, result = results.get_nowait()
                if operation == "upload" and result:
                    upload_successes += 1
                elif operation == "download" and result:
                    download_successes += 1
                elif operation == "error":
                    errors.append(f"Thread {file_index}: {result}")
            except queue.Empty:
                break
        
        assert len(errors) == 0, f"Concurrent operations had errors: {errors}"
        assert upload_successes == num_threads, f"Expected {num_threads} uploads, got {upload_successes}"
        assert download_successes == num_threads, f"Expected {num_threads} downloads, got {download_successes}"
        
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Concurrent operations test failed: {e}")
    finally:
        # Cleanup
        try:
            for i in range(num_threads):
                requests.delete(f"{MINIO_API_URL}/{bucket_name}/concurrent-test-{i}.txt", 
                              auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD))
            requests.delete(f"{MINIO_API_URL}/{bucket_name}", 
                          auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD))
        except:
            pass

@pytest.mark.parametrize("method,expected_codes", [
    ("GET", [200, 404]),
    ("HEAD", [200, 404]),
    ("PUT", [200, 201]),
    ("POST", [200, 405]),  # POST might not be allowed on all endpoints
    ("DELETE", [200, 204, 404])
])
def test_minio_http_methods(method, expected_codes):
    """Test that MinIO properly handles different HTTP methods."""
    bucket_name = "test-http-methods-bucket"
    
    try:
        if method in ["PUT", "POST", "DELETE"]:
            # First create the bucket for these operations
            requests.put(f"{MINIO_API_URL}/{bucket_name}", 
                        auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD))
        
        response = requests.request(method, f"{MINIO_API_URL}/{bucket_name}", 
                                  auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD), 
                                  timeout=10)
        
        assert response.status_code in expected_codes, \
            f"HTTP {method} returned unexpected status {response.status_code}, expected one of {expected_codes}"
            
    except requests.exceptions.RequestException as e:
        pytest.fail(f"HTTP method {method} test failed: {e}")
    finally:
        # Cleanup
        try:
            requests.delete(f"{MINIO_API_URL}/{bucket_name}", 
                          auth=(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD))
        except:
            pass
