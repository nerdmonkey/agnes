import json
from typing import Any, Dict

import boto3


class QueueService:
    """
    A service class to interact with AWS Simple Queue Service (SQS).

    This class provides methods to send, receive, and delete messages from
    an SQS queue. It uses the boto3 library to communicate with AWS services.
    """

    def __init__(self, region_name: str = "us-east-1") -> None:
        """
        Initializes the QueueService class.

        Creates an SQS client using boto3 which is used to interact with the AWS SQS.
        """
        self.sqs_client = boto3.client("sqs", region_name=region_name)

    def _prepare_message(self, message: Dict[str, Any]) -> str:
        """
        Prepares a message for sending to the SQS queue by converting it to JSON.

        Args:
            message (Dict[str, Any]): The message to be sent.

        Returns:
            str: The JSON representation of the message.
        """
        return json.dumps(message)

    def send_message(
        self,
        queue_url: str,
        message: dict,
        group_id: str = None,
        deduplication_id: str = None,
    ) -> dict:
        """
        Sends a message to an SQS queue.

        This method automatically determines if the queue is a FIFO queue by
        checking if the queue URL ends with '.fifo'. It adds the 'MessageGroupId'
        and 'MessageDeduplicationId' parameters only if it's a FIFO queue.

        Args:
            queue_url (str): The URL of the SQS queue.
            message (dict): The message to send.
            group_id (str, optional): The group ID of the message, used for FIFO queues.
            deduplication_id (str, optional): The deduplication ID of the message, used for FIFO queues.

        Returns:
            dict: The response from the SQS service after sending the message.
        """
        send_params = {"QueueUrl": queue_url, "MessageBody": json.dumps(message)}

        # Check if the queue is a FIFO queue
        if queue_url.endswith(".fifo"):
            if group_id is not None:
                send_params["MessageGroupId"] = group_id
            if deduplication_id is not None:
                send_params["MessageDeduplicationId"] = deduplication_id

        return self.sqs_client.send_message(**send_params)

    def receive_message(self, queue_url: str) -> Dict[str, Any]:
        """
        Receives a message from an SQS queue.

        Args:
            queue_url (str): The URL of the SQS queue.

        Returns:
            Dict[str, Any]: The response from the SQS service containing the message(s) received.
        """
        return self.sqs_client.receive_message(
            QueueUrl=queue_url, AttributeNames=["All"], MessageAttributeNames=["All"]
        )

    def delete_message(self, queue_url: str, receipt_handle: str) -> dict:
        """
        Deletes a message from an SQS queue.

        Args:
            queue_url (str): The URL of the SQS queue.
            receipt_handle (str): The receipt handle of the message to be deleted.

        Returns:
            dict: The response from the SQS service after deleting the message.
        """
        return self.sqs_client.delete_message(
            QueueUrl=queue_url, ReceiptHandle=receipt_handle
        )
