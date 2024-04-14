import boto3
from moto import mock_sqs

from app.services.queue import (
    QueueService,
)  # Replace 'your_module' with the actual module name


@mock_sqs
def test_send_message_to_standard_queue():
    # Setup
    sqs = boto3.resource("sqs", region_name="us-east-1")
    sqs.create_queue(QueueName="TestQueue")
    queue_url = sqs.get_queue_by_name(QueueName="TestQueue").url
    queue_service = QueueService()
    message = {"key": "value"}

    # Test
    response = queue_service.send_message(queue_url, message, str(1), str(1))

    # Assert
    assert "MessageId" in response


@mock_sqs
def test_send_message_to_fifo_queue():
    # Mock the SQS service
    sqs = boto3.resource("sqs", region_name="us-east-1")

    # Create a FIFO queue
    queue = sqs.create_queue(
        QueueName="TestQueue.fifo",
        Attributes={
            "FifoQueue": "true",
            "ContentBasedDeduplication": "true",  # Enable if you want automatic deduplication
        },
    )
    queue_url = queue.url

    # Test sending a message to the FIFO queue
    queue_service = QueueService()  # Assuming QueueService is defined elsewhere
    queue_service.send_message(queue_url, {"key": "value"}, "group1", "dedup1")


@mock_sqs
def test_receive_message():
    # Setup
    sqs = boto3.resource("sqs", region_name="us-east-1")
    queue = sqs.create_queue(QueueName="TestQueue")
    queue_url = queue.url
    queue_service = QueueService()
    message = {"key": "value"}
    queue_service.send_message(queue_url, message, 1, 1)

    # Test
    response = queue_service.receive_message(queue_url)

    # Assert
    assert "Messages" in response
    assert response["Messages"][0]["Body"] == '{"key": "value"}'


@mock_sqs
def test_delete_message():
    # Setup
    sqs = boto3.resource("sqs", region_name="us-east-1")
    queue = sqs.create_queue(QueueName="TestQueue")
    queue_url = queue.url
    queue_service = QueueService()
    message = {"key": "value"}
    queue_service.send_message(queue_url, message, "1", "1")

    # Receive the message to get the correct receipt handle
    receive_response = queue_service.receive_message(queue_url)
    receipt_handle = receive_response["Messages"][0]["ReceiptHandle"]

    # Test
    delete_response = queue_service.delete_message(queue_url, receipt_handle)

    # Assert
    assert delete_response["ResponseMetadata"]["HTTPStatusCode"] == 200


0
