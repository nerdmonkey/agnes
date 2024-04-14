from app.services.user import UserService


def main(event, context):
    """
    Process and save user data from AWS Lambda event records.

    This function is designed to be used as an AWS Lambda handler for processing
    user data from an event triggered by an AWS service like SQS. It processes each
    record in the event and saves the user data using the UserService class.

    Parameters:
    - event (dict): The AWS Lambda event object containing records.
    - context (LambdaContext): The AWS Lambda context object.

    Returns:
    - dict: A dictionary indicating a successful execution with a status code of 200.
    """
    for item in event["Records"]:
        body = item["body"]
        user_service = UserService()
        user_service.save(body)

    return {"StatusCode": 200}
