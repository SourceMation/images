import pytest
import subprocess
import pika

RABBITMQ_USER = "guest"
RABBITMQ_PASSWORD = "guest"
RABBITMQ_HOST = "localhost"

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
