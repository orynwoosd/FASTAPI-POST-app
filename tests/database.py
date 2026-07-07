# from fastapi.testclient import TestClient
# from app.main import app
# from app.database import get_db, Base

# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine
# from app.config import settings
# import pytest
# from sqlalchemy.orm import Session


# # SQLALCHEMY_DATABASE_URL = 
# # a new database was created in postgress with name fasapi_test for testing purpose.
# SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
# engine = create_engine(SQLALCHEMY_DATABASE_URL)  
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base.metadata.create_all(bind=engine)
# # Base = declarative_base()

# # def override_get_db():
# #     db = TestingSessionLocal()
# #     try:
# #         yield db
# #     finally:
# #         db.close()

# # app.dependency_overrides[get_db] = override_get_db


# # client = TestClient(app)



# @pytest.fixture(scope="module")  # runs per function
# def session() -> Session:
#     """
#     Overview
#         - This fixture tears and creats a fresh database for each test
#         - It creates a new session for each test.
#         - A session is what helps us to communicate with our database.
#           i.e., db.add(), db.commit()
#     """
#     # Before test
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)

#     db = TestingSessionLocal()  # Creates a new sqlalchemy session
#     try:
#         yield db  # test runs here, and db is passed into test as the argument named session
#     finally:
#         db.close()  # After test, tears down, runs even if test fails.


# @pytest.fixture(scope="module")
# def client(session: Session) -> TestClient:
#     """
#     Overview
#         - Fixture makes FASTAPI use the test DB during the test
#         - It recieves the session object created by sesion fixture
#     """
    
#     def override_get_db():
#         yield session  # The test db

#     # now when ever a route ask for get_db, its given override_get_db instead
#     # WHich returns the test session.
#     app.dependency_overrides[get_db] = override_get_db

#     try:
#         yield TestClient(app)
#     finally:
#         # Finally all overrides are removed.
#         app.dependency_overrides.clear()

       