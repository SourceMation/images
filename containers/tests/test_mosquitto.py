import pytest
import subprocess
import time
import os

def test_mosquitto_installed():
    result = subprocess.run(["mosquitto", "-h"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # older mosquitto returned 3 newer versions return 0
    assert result.returncode == 0, "Mosquitto is not installed"

def test_mosquitto_running():
    result = subprocess.run(["pgrep", "mosquitto"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert result.returncode == 0, "Mosquitto is not running"

def test_publish_and_subscribe():
    topic = "test/topic"
    message = "Hello, Mosquitto!"
    sub_proc = subprocess.Popen(["mosquitto_sub", "-t", topic], stdout=subprocess.PIPE, text=True)
    time.sleep(1)
    pub_result = subprocess.run(["mosquitto_pub", "-t", topic, "-m", message], capture_output=True, text=True)
    assert pub_result.returncode == 0, "Failed to publish the message."
    output = sub_proc.stdout.readline()
    assert message in output, "The published message was not received."
    sub_proc.terminate()

def test_publish_with_qos():
    topic = "test/qos"
    message = "QoS test"
    for qos in ["0", "1", "2"]:
        sub_proc = subprocess.Popen(["mosquitto_sub", "-t", topic, "-q", qos], stdout=subprocess.PIPE, text=True)
        time.sleep(1)
        pub_result = subprocess.run(["mosquitto_pub", "-t", topic, "-m", message, "-q", qos], capture_output=True, text=True)
        assert pub_result.returncode == 0, f"Failed to publish the message with QoS {qos}."
        output = sub_proc.stdout.readline()
        assert message in output, f"The message with QoS {qos} was not received."
        sub_proc.terminate()

def test_multiple_subscriptions():
    topics = ["multi/topic1", "multi/topic2"]
    messages = ["Message1", "Message2"]
    sub_proc = subprocess.Popen(["mosquitto_sub", "-t", "multi/#"], stdout=subprocess.PIPE, text=True)
    time.sleep(1)
    for topic, message in zip(topics, messages):
        pub_result = subprocess.run(["mosquitto_pub", "-t", topic, "-m", message], capture_output=True, text=True)
        assert pub_result.returncode == 0, f"Failed to publish the message to topic {topic}."
        output = sub_proc.stdout.readline()
        assert message in output, f"The message for topic {topic} was not received."
    sub_proc.terminate()
