import pytest
# from myapp import create_app, db
# from myapp.models import User

# @pytest.fixture(scope='module')
# def test_client():
#     flask_app = create_app('testing')

#     # Create a test client using the Flask application configured for testing
#     with flask_app.test_client() as testing_client:
#         with flask_app.app_context():
#             yield testing_client  # this is where the testing happens!

# @pytest.fixture(scope='module')
# def init_database():
#     # Create the database and the database table(s)
#     db.create_all()

#     # Insert user data
#     user1 = User(username='testuser1', email='test1@example.com')
#     user2 = User(username='testuser2', email='test2@example.com')
#     db.session.add(user1)
#     db.session.add(user2)

#     # Commit the changes for the users
#     db.session.commit()

#     yield db  # this is where the testing happens!

#     db.drop_all()