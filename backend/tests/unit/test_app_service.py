import jsonpickle
import pytest
from boto3.exceptions import Boto3Error

from app.services.app import AppService


@pytest.fixture
def mock_dynamodb_resource(mocker):
    """Mock the DynamoDB resource."""
    mock_resource = mocker.patch("boto3.resource")
    mock_table = mock_resource.return_value.Table.return_value
    return mock_resource, mock_table


@pytest.fixture
def app_service(mock_dynamodb_resource):
    """Create an instance of AppService with mocked DynamoDB resource."""
    return AppService()


def test_set_state_success(app_service, mock_dynamodb_resource):
    _, mock_table = mock_dynamodb_resource
    mock_table.update_item.return_value = {
        "Attributes": {"Attr_Data": jsonpickle.encode("some value")}
    }
    returned_value = app_service.set_state("test_key", "some value")
    assert jsonpickle.decode(returned_value) == "some value"
    mock_table.update_item.assert_called()


def test_get_state_success(app_service, mock_dynamodb_resource):
    _, mock_table = mock_dynamodb_resource
    mock_table.get_item.return_value = {
        "Item": {"Attr_Data": jsonpickle.encode("some value")}
    }
    assert app_service.get_state("test_key") == "some value"
    mock_table.get_item.assert_called()


def test_remove_state_success(app_service, mock_dynamodb_resource):
    _, mock_table = mock_dynamodb_resource
    mock_table.delete_item.return_value = {
        "Attributes": {"Attr_Data": jsonpickle.encode("some value")}
    }
    returned_value = app_service.remove_state("test_key")
    assert jsonpickle.decode(returned_value) == "some value"


def test_dynamodb_error_handling(app_service, mock_dynamodb_resource):
    _, mock_table = mock_dynamodb_resource
    mock_table.get_item.side_effect = Boto3Error

    with pytest.raises(Boto3Error):
        app_service.get_state("test_key")
