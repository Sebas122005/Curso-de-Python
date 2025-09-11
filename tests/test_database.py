"""
Tests para la clase Database del módulo crud_cuentas_banco.
"""
import pytest
from unittest.mock import patch, Mock
import sys
import os

# Agregar el directorio padre al path para importar los módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'crud_cuentas_banco'))

from database import Database


class TestDatabase:
    """Clase de tests para la funcionalidad de Database."""
    
    def test_load_config_success(self, temp_config_file):
        """Test que verifica la carga exitosa de configuración."""
        with patch('database.configparser.ConfigParser') as mock_parser:
            mock_config = Mock()
            mock_config.get.return_value = 'test_value'
            mock_config.getint.return_value = 3306
            mock_parser.return_value = mock_config
            
            db = Database()
            db.load_config()
            
            assert db.config is not None
            assert 'user' in db.config
            assert 'password' in db.config
            assert 'host' in db.config
            assert 'database' in db.config
            assert 'port' in db.config
    
    def test_load_config_file_not_found(self):
        """Test que verifica el manejo de archivo de configuración no encontrado."""
        with patch('database.configparser.ConfigParser') as mock_parser:
            mock_parser.side_effect = FileNotFoundError()
            
            db = Database()
            db.load_config()
            
            assert db.config is None
    
    @patch('database.pymysql.connect')
    def test_connect_success(self, mock_connect, temp_config_file):
        """Test que verifica la conexión exitosa a la base de datos."""
        mock_connection = Mock()
        mock_connect.return_value = mock_connection
        
        db = Database()
        db.config = {
            'user': 'test_user',
            'password': 'test_password',
            'host': 'localhost',
            'database': 'test_db',
            'port': 3306
        }
        
        db.connect()
        
        assert db.connection == mock_connection
        mock_connect.assert_called_once()
    
    def test_connect_no_config(self):
        """Test que verifica el comportamiento cuando no hay configuración."""
        db = Database()
        db.config = None
        
        db.connect()
        
        assert db.connection is None
    
    def test_disconnect_with_connection(self):
        """Test que verifica el cierre de conexión cuando existe una conexión."""
        db = Database()
        mock_connection = Mock()
        mock_connection.open = True
        db.connection = mock_connection
        
        db.disconnect()
        
        mock_connection.close.assert_called_once()
    
    def test_disconnect_no_connection(self):
        """Test que verifica el comportamiento cuando no hay conexión."""
        db = Database()
        db.connection = None
        
        # No debería lanzar excepción
        db.disconnect()
