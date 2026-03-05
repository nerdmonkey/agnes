from unittest.mock import MagicMock, patch

from handlers.user import main


def test_user_lambda_function():
    """
    Test the AWS Lambda function to ensure it processes the event records correctly.

    This test simulates an AWS Lambda event and context, mocking the UserService
    and its save method. It verifies that the Lambda function processes each record
    in the event and calls the UserService save method with the correct data.
    """
    # Mock the UserService and its save method
    mock_user_service = MagicMock()
    mock_save = MagicMock()
    mock_user_service.return_value.save = mock_save

    # Patch the UserService with the mock
    with patch("handlers.user.UserService", new=mock_user_service):
        # Simulate Lambda event and context
        event = {"Records": [{"body": "user1"}, {"body": "user2"}]}
        context = {}  # Context can be an empty dictionary if not used in the function

        # Call the Lambda function
        response = main(event, context)

        # Assert the Lambda function response
        assert response == {"StatusCode": 200}

        # Assert the save method was called correctly
        assert mock_save.call_count == len(event["Records"])
        mock_save.assert_any_call("user1")
        mock_save.assert_any_call("user2")
