import logging
import os

import boto3
import jsonpickle


class AppService:
    """
    A service class to interact with an AWS DynamoDB table.
    Provides methods to set, get, and remove a state in a DynamoDB table.
    """

    def __init__(self):
        """
        Initializes the AppService class.
        Sets up the DynamoDB resource and table.
        """
        self.logger = logging.getLogger(__name__)
        self.dynamodb_resource, self.table = self._setup_dynamodb()

    @staticmethod
    def _load_config():
        """Load configuration from environment variables."""
        table_name = os.environ.get("GSM_TABLE", "GlobalStateTable")
        region_name = os.environ.get("AWS_REGION", "us-east-1")
        return table_name, region_name

    @staticmethod
    def _setup_dynamodb():
        """Set up the DynamoDB resource and table."""
        table_name, region_name = AppService._load_config()
        dynamodb_resource = boto3.resource("dynamodb", region_name=region_name)
        table = dynamodb_resource.Table(table_name)
        return dynamodb_resource, table

    @staticmethod
    def _serialize(value):
        """Serialize a Python object to JSON."""
        return jsonpickle.encode(value)

    @staticmethod
    def _deserialize(value):
        """Deserialize a JSON string to a Python object."""
        return jsonpickle.decode(value)

    def _handle_dynamodb_error(self, error, action):
        """Handle DynamoDB errors."""
        self.logger.error(f"Error {action} state: {error}")
        raise error

    def set_state(self, key, value):
        """Sets or updates a state in the DynamoDB table."""
        try:
            value_json = self._serialize(value)
            response = self.table.update_item(
                Key={"Key": key},
                UpdateExpression="SET Attr_Data = :val",
                ExpressionAttributeValues={":val": value_json},
                ReturnValues="UPDATED_NEW",
            )
            return response["Attributes"]["Attr_Data"]
        except boto3.exceptions.Boto3Error as e:
            self._handle_dynamodb_error(e, "setting")

    def get_state(self, key):
        """Retrieves a state from the DynamoDB table."""
        try:
            response = self.table.get_item(Key={"Key": key})
            item = response.get("Item", {})
            return self._deserialize(item["Attr_Data"]) if "Attr_Data" in item else None
        except boto3.exceptions.Boto3Error as e:
            self._handle_dynamodb_error(e, "getting")

    def remove_state(self, key):
        """Removes a state from the DynamoDB table."""
        try:
            response = self.table.delete_item(Key={"Key": key})
            return response.get("Attributes", {}).get("Attr_Data")
        except boto3.exceptions.Boto3Error as e:
            self._handle_dynamodb_error(e, "removing")
