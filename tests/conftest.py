# @pytest.fixture(scope="session", autouse=True)
# def setup_db():
#     Base.metadata.create_all(bind=engine)
#     yield
#     Base.metadata.drop_all(bind=engine)


import os
import pytest
from alembic.config import Config
from alembic import command
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.orm import sessionmaker
from app.database import get_db_context
from fastapi.testclient import TestClient
from main import app
from dotenv import load_dotenv
import logging
logging.basicConfig(level=logging.INFO)


load_dotenv()
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")


engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    os.environ["TEST_DATABASE_URL"] = TEST_DATABASE_URL

    if not database_exists(TEST_DATABASE_URL):
        create_database(TEST_DATABASE_URL)

    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)
    print("ALEMBIC URL:", alembic_cfg.get_main_option("sqlalchemy.url"))

    command.upgrade(alembic_cfg, "head")

    yield


@pytest.fixture(scope="session")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="session")
def client(db_session):
    def override_get_db():
        yield db_session
    app.dependency_overrides[get_db_context] = override_get_db
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def admin_token(client):
    login_data = {
        "username": "fa_admin",
        "password": "Password01"
    }
    r = client.post(
        "auth/token",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert r.status_code == 200
    return r.json()["access_token"]


@pytest.fixture(scope="session")
def created_company(client: TestClient, admin_token):
    data = {
        "name": "Acme Corp",
        "description": "Test company",
        "mode": "startup",
        "rating": 4
    }
    r = client.post(
        "/companies",
        json=data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert r.status_code == 201
    return r.json()


@pytest.fixture(scope="session")
def create_company_to_be_deleted(client: TestClient, admin_token):
    data = {
        "name": "To be deleted",
        "description": "Test company will be deleted",
        "mode": "to be deleted",
        "rating": 2
    }
    r = client.post(
        "/companies",
        json=data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert r.status_code == 201
    return r.json()


@pytest.fixture(scope="session")
def created_user(client: TestClient, admin_token, created_company):
    data = {
        "email": "testcreated@example.com",
        "username": "tester created",
        "first_name": "Test Create",
        "last_name": "User",
        "password": "Password123",
        "company_id": created_company['id']
    }
    r = client.post(
        "/users",
        json=data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert r.status_code == 201
    return r.json()


@pytest.fixture(scope="session")
def create_user_to_be_deleted(
    client: TestClient,
    admin_token,
    create_company_to_be_deleted
):
    data = {
        "email": "testdeleted@example.com",
        "username": "tester to be deleted",
        "first_name": "Test to be deleted",
        "last_name": "User to be deleted",
        "password": "Password123!",
        "company_id": create_company_to_be_deleted['id']
    }
    r = client.post(
        "/users",
        json=data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert r.status_code == 201
    return r.json()


@pytest.fixture(scope="session")
def created_task(client: TestClient, admin_token, created_user):
    data = {
        "summary": "Test Task",
        "description": "Task description",
        "status": "TODO",
        "priority": 3,
        "owner_id": created_user['id']
    }
    r = client.post(
        "/tasks",
        json=data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert r.status_code == 201
    return r.json()


@pytest.fixture(scope="session")
def create_task_to_be_deleted(
    client: TestClient,
    admin_token,
    create_user_to_be_deleted
):
    data = {
        "summary": "Test Task to be deleted",
        "description": "Task description",
        "status": "TOBEDELETED",
        "priority": 4,
        "owner_id": create_user_to_be_deleted['id']
    }
    r = client.post(
        "/tasks",
        json=data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert r.status_code == 201
    return r.json()
