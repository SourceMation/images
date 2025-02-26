import os
import subprocess
import pytest

@pytest.fixture(scope="module")
def kafka_home():
    kafka_dir = "/opt/kafka"
    assert os.path.exists(kafka_dir), f"Kafka directory not found: {kafka_dir}"
    return kafka_dir

@pytest.fixture(scope="module")
def env(kafka_home):
    env = os.environ.copy()
    env["KAFKA_HOME"] = kafka_home
    env["PATH"] += f":{kafka_home}/bin"
    return env


def test_kafka_binaries(kafka_home):
    binaries = ["kafka-server-start.sh", "kafka-server-stop.sh", "zookeeper-server-start.sh", "zookeeper-server-stop.sh"]
    for binary in binaries:
        path = os.path.join(kafka_home, "bin", binary)
        assert os.path.isfile(path), f"Binary not found: {path}"

def test_start_zookeeper():
    result = subprocess.run(["pgrep", "-f", "zookeeper"], capture_output=True, text=True)
    assert result.returncode == 0, "Zookeeper process is not running."

def test_start_kafka():
    result = subprocess.run(["pgrep", "-f", "kafka.Kafka"], capture_output=True, text=True)
    assert result.returncode == 0, "Kafka process is not running."

def test_produce_and_consume_message(env):
    topic = "test-topic"

    # Create topic
    subprocess.run(
        ["kafka-topics.sh", "--create", "--topic", topic, "--bootstrap-server", "localhost:9092"],
        env=env,
        check=True,
    )

    # Produce message
    producer = subprocess.Popen(
        ["kafka-console-producer.sh", "--topic", topic, "--bootstrap-server", "localhost:9092"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        text=True,
    )
    producer_output, producer_error = producer.communicate("Hello, Kafka!\n")
    producer.wait()
    print(f"Producer stdout: {producer_output}")
    print(f"Producer stderr: {producer_error}")

    # Consume message
    consumer = subprocess.Popen(
        ["kafka-console-consumer.sh", "--topic", topic, "--from-beginning", "--bootstrap-server", "localhost:9092", "--max-messages", "1"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        text=True,
    )
    try:
        output, error = consumer.communicate(timeout=30)
        print(f"Consumer stdout: {output}")
        print(f"Consumer stderr: {error}")
        assert "Hello, Kafka!" in output, "Message not received by consumer"
    except subprocess.TimeoutExpired as e:
        consumer.kill()
        raise RuntimeError(f"Consumer timeout: {e}")
