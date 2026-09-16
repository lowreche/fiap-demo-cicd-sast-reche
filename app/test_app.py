import sqlite3
import pytest
from app import app

@pytest.fixture(autouse=True)
def setup_db():
    conn = sqlite3.connect('users.db')
    # Cria a tabela users caso ela não exista
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
    # Insere um usuário para o teste não falhar por falta de dados
    conn.execute("INSERT OR IGNORE INTO users (id, name) VALUES (1, 'Luiz Teste')")
    conn.commit()
    conn.close()

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_safe_user_route(client):
    response = client.get('/user/safe?id=1')
    assert response.status_code == 200

def test_ping_route_exists(client):
    response = client.get('/ping?host=localhost')
    assert response.status_code in [200, 500]

def test_app_exists():
    assert app is not None