import subprocess
import os

OPENAPI_SPEC_FILE = "openapi.yaml"
OUTPUT_DIR = "generated-client"

def test_openapi_generator_version():
    result = subprocess.run(["openapi-generator-cli", "version"], capture_output=True, text=True, timeout=90)
    assert result.returncode == 0, "Failed to retrieve OpenAPI Generator version."
    assert result.stdout.strip(), "Empty version output from OpenAPI Generator."

def test_generate_client():
    # Example OpenAPI specification
    openapi_spec = """openapi: 3.0.0
info:
  title: Test API
  version: 1.0.0
paths:
  /test:
    get:
      responses:
        '200':
          description: OK
"""

    # Saving the specification to a file
    with open(OPENAPI_SPEC_FILE, "w") as f:
        f.write(openapi_spec)

    # Removing old generated files
    if os.path.exists(OUTPUT_DIR):
        subprocess.run(["rm", "-rf", OUTPUT_DIR])

    # Running OpenAPI Generator CLI
    result = subprocess.run(
        ["openapi-generator-cli", "generate", "-i", OPENAPI_SPEC_FILE, "-g", "python", "-o", OUTPUT_DIR],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, "Failed to generate client."
    assert os.path.exists(os.path.join(OUTPUT_DIR, "README.md")), "Client generation failed - missing README.md."
    assert os.path.isdir(os.path.join(OUTPUT_DIR, "openapi_client")), "Client package was not created."

def test_cleanup():
    if os.path.exists(OUTPUT_DIR):
        subprocess.run(["rm", "-rf", OUTPUT_DIR])
    if os.path.exists(OPENAPI_SPEC_FILE):
        os.remove(OPENAPI_SPEC_FILE)
