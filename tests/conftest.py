"""
Configuración global para pytest.
Contiene fixtures y configuraciones compartidas entre tests.
"""
import pytest
import tempfile
import os
from unittest.mock import Mock


@pytest.fixture
def temp_config_file():
    """Fixture que crea un archivo de configuración temporal para testing."""
    config_content = """
[mysql_config]
host = localhost
port = 3306
user = test_user
password = test_password
db = test_db
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as f:
        f.write(config_content)
        temp_file = f.name
    
    yield temp_file
    
    # Cleanup
    os.unlink(temp_file)


@pytest.fixture
def mock_database_connection():
    """Fixture que proporciona una conexión mock para testing."""
    mock_conn = Mock()
    mock_conn.cursor.return_value.__enter__.return_value = Mock()
    mock_conn.open = True
    return mock_conn


@pytest.fixture
def sample_cliente_data():
    """Fixture que proporciona datos de ejemplo para testing de clientes."""
    return {
        'codigo': 1,
        'nombre': 'Juan Pérez',
        'apellido': 'García',
        'email': 'juan@example.com',
        'telefono': '123456789'
    }
