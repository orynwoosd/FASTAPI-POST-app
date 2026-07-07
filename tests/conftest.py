"""
conftest allows all fixtures to be automatically accessible within every file
test folder automatically, and no need for imports,
"""

from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, Base
from app import models
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.config import settings
import pytest
from sqlalchemy.orm import Session
from app.oauth2 import create_access_token

# SQLALCHEMY_DATABASE_URL = 
# a new database was created in postgress with name fasapi_test for testing purpose.
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)  
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
# Base = declarative_base()

# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# app.dependency_overrides[get_db] = override_get_db


# client = TestClient(app)



@pytest.fixture(scope="function")  # runs per function
def session() -> Session:
    """
    Overview
        - This fixture tears and creats a fresh database for each test
        - It creates a new session for each test.
        - A session is what helps us to communicate with our database.
          i.e., db.add(), db.commit()
    """
    # Before test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()  # Creates a new sqlalchemy session
    try:
        yield db  # test runs here, and db is passed into test as the argument named session
    finally:
        db.close()  # After test, tears down, runs even if test fails.


@pytest.fixture(scope="function")
def client(session: Session) -> TestClient:
    """
    Overview
        - Fixture makes FASTAPI use the test DB during the test
        - It recieves the session object created by sesion fixture
    """
    
    def override_get_db():
        yield session  # The test db

    # now when ever a route ask for get_db, its given override_get_db instead
    # WHich returns the test session.
    app.dependency_overrides[get_db] = override_get_db

    try:
        yield TestClient(app)
    finally:
        # Finally all overrides are removed.
        app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_user(client):
    user_data = {"email": "oryn1@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture(scope="function")
def test_user2(client):
    user_data = {"email": "oryn2@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [
        {
            "title": "first post",
            "content": "First content",
            "user_id": test_user["id"]
        },
        
        {
            "title": "second post",
            "content": "second content",
            "user_id": test_user["id"]
        },
        {
            "title": "third post",
            "content": "third content",
            "user_id": test_user["id"]
        },
        {
            "title": "fourth post",
            "content": "fourth content",
            "user_id": test_user["id"]
        },
        {
            "title": "fourth post",
            "content": "fourth content",
            "user_id": test_user2["id"]
        },
        {
            "title": "fourth post",
            "content": "fourth content",
            "user_id": test_user2["id"]
        },
        {
            "title": "fourth post",
            "content": "fourth content",
            "user_id": test_user2["id"]
        },

    ]

    # convert list into models
    def create_post_model(posts):
        return models.Post(**posts)
    
    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    session.add_all(posts)

    session.commit()
    posts = session.query(models.Post).all()

    return posts