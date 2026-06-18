import os
import pytest
from fastapi.testclient import TestClient

# Garante a URL de teste antes de carregar a aplicação
os.environ["DATABASE_URL"] = "postgresql://postgres:password@localhost:5433/ecom_test"

from main import app
from app.database import engine, Base, get_db, SessionLocal
from app.models import ProductModel

@pytest.fixture(scope="function", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    def _get_db_override():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_db_override
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def produto_existente(client):
    payload = {"nome": "Teclado Mecânico", "preco": 349.90, "estoque": 15, "ativo": True}
    response = client.post("/produtos", json=payload)
    return response.json()