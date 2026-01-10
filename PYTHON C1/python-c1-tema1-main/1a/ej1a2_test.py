"""
Tests para el ejercicio ej1a2.py
Este archivo contiene pruebas para verificar la correcta implementación
de las funciones para trabajar con respuestas en formato JSON.
"""

import pytest
import responses
from unittest.mock import patch, Mock
import time

from ej1a2 import get_user_ip_json, get_response_info

@pytest.fixture
def mock_responses():
    """
    Fixture para configurar respuestas simuladas para las peticiones HTTP
    """
    with responses.RequestsMock() as rsps:
        # Configurar respuesta para la petición de IP en formato JSON
        rsps.add(
            responses.GET,
            "https://api.ipify.org?format=json",
            json={"ip": "98.207.254.136"},
            status=200,
            headers={"Content-Type": "application/json"}
        )
        yield rsps

def test_get_user_ip_json(mock_responses):
    """
    Prueba la función get_user_ip_json cuando la petición es exitosa.
    """
    result = get_user_ip_json()
    assert result == "98.207.254.136"

def test_get_user_ip_json_failure():
    """
    Prueba la función get_user_ip_json cuando la petición falla.
    """
    with patch('requests.get') as mock_get:
        # Configurar el mock para simular un error
        mock_get.side_effect = Exception("Connection error")
        result = get_user_ip_json()
        assert result is None

@patch('requests.get')
def test_get_user_ip_json_bad_status(mock_get):
    """
    Prueba la función get_user_ip_json cuando la petición devuelve un código de error.
    """
    # Configurar la respuesta del mock con un código de error
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response
    
    result = get_user_ip_json()
    assert result is None

@patch('requests.get')
def test_get_response_info(mock_get):
    """
    Prueba la función get_response_info cuando la petición es exitosa.
    """
    # Configurar la respuesta del mock
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.elapsed = Mock()
    mock_response.elapsed.total_seconds = lambda: 0.2  # 200ms
    mock_response.content = b'{"ip":"98.207.254.136"}'
    mock_get.return_value = mock_response
    
    result = get_response_info()
    
    assert result is not None
    assert result["content_type"] == "application/json"
    assert result["elapsed_time"] > 0  # Tiempo de respuesta en ms
    assert result["response_size"] == len(b'{"ip":"98.207.254.136"}')  # Tamaño en bytes

def test_get_response_info_failure():
    """
    Prueba la función get_response_info cuando la petición falla.
    """
    with patch('requests.get') as mock_get:
        # Configurar el mock para simular un error
        mock_get.side_effect = Exception("Connection error")
        result = get_response_info()
        assert result is None
