import pytest
import subprocess
import pika
import requests

RABBITMQ_ADMIN_PORT = 15672
RABBITMQ_USER = "guest"
RABBITMQ_PASSWORD = "guest"
RABBITMQ_HOST = "localhost"
RABBITMQ_ADMIN_URL = f"http://{RABBITMQ_HOST}:{RABBITMQ_ADMIN_PORT}"


def test_rabbitmq_installed():
    result = subprocess.run(['rabbitmqctl', 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "RabbitMQ is not installed or 'rabbitmqctl' command is not found."
    assert "Status of node" in result.stdout, "Unexpected output from 'rabbitmqctl status'."


def test_rabbitmq_connection():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)

    try:
        connection = pika.BlockingConnection(parameters)
        assert connection.is_open, "Failed to open a connection to RabbitMQ."
    except Exception as e:
        pytest.fail(f"Failed to connect to RabbitMQ: {str(e)}")
    finally:
        if connection.is_open:
            connection.close()


def test_rabbitmq_send_message():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    try:
        channel.queue_declare(queue='test_queue')

        message = 'Hello, RabbitMQ!'
        channel.basic_publish(exchange='', routing_key='test_queue', body=message)
        
        assert channel.is_open, "Failed to send message to RabbitMQ."

    except Exception as e:
        pytest.fail(f"Failed to send message to RabbitMQ: {str(e)}")
    
    finally:
        connection.close()


def test_rabbitmq_receive_message():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    try:
        channel.queue_declare(queue='test_queue')

        method_frame, header_frame, body = channel.basic_get(queue='test_queue', auto_ack=True)
        assert body is not None, "No message received from RabbitMQ."
        assert body.decode() == 'Hello, RabbitMQ!', f"Expected 'Hello, RabbitMQ!', got {body.decode()}"

    except Exception as e:
        pytest.fail(f"Failed to receive message from RabbitMQ: {str(e)}")

    finally:
        connection.close()


def test_rabbitmq_delete_queue():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    try:
        channel.queue_declare(queue='test_queue')

        channel.queue_delete(queue='test_queue')

        result = channel.queue_declare(queue='test_queue', passive=True)
        pytest.fail("Queue 'test_queue' still exists after deletion.")

    except pika.exceptions.ChannelClosedByBroker as e:
        assert "NOT_FOUND" in str(e), "Queue should not exist after deletion."

    finally:
        connection.close()


def test_rabbitmq_redeclare_queue():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    try:
        channel.queue_declare(queue='test_queue')
        with pytest.raises(pika.exceptions.ChannelClosedByBroker):
            channel.queue_declare(queue='test_queue', durable=True)
    finally:
        connection.close()


def test_rabbitmq_purge_queue():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    try:
        channel.queue_declare(queue='test_queue')
        channel.basic_publish(exchange='', routing_key='test_queue', body='Message to purge')
        channel.queue_purge(queue='test_queue')

        method_frame, header_frame, body = channel.basic_get(queue='test_queue', auto_ack=True)
        assert body is None, "Queue was not purged successfully."
    except Exception as e:
        pytest.fail(f"Failed to purge queue in RabbitMQ: {str(e)}")
    finally:
        connection.close()


def test_rabbitmq_admin_interface_accessible():
    """Tests if the RabbitMQ management interface is accessible."""
    try:
        auth = (RABBITMQ_USER, RABBITMQ_PASSWORD)
        response = requests.get(RABBITMQ_ADMIN_URL, auth=auth)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        assert "RabbitMQ Management" in response.text, "RabbitMQ Management interface not found in the response."
    except requests.exceptions.ConnectionError as e:
        pytest.fail(f"Failed to connect to RabbitMQ Admin Interface at {RABBITMQ_ADMIN_URL}: {str(e)}")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Error accessing RabbitMQ Admin Interface: {str(e)}")
