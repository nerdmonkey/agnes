from sqlalchemy import Integer, String

from app.models.user import User


def test_user_model():
    """
    Test to ensure that the User model is defined correctly.

    This test verifies that the User model, which inherits from the SQLAlchemy Base,
    is defined with the correct table name and columns. It checks the types of the
    'id', 'username', 'email', and 'password' columns. The test does not interact
    with a database, but ensures that the model's structure aligns with the expected
    schema.
    """
    assert User.__tablename__ == "users"
    assert isinstance(User.id.property.columns[0].type, Integer)
    assert isinstance(User.username.property.columns[0].type, String)
    assert isinstance(User.email.property.columns[0].type, String)
    assert isinstance(User.password.property.columns[0].type, String)
