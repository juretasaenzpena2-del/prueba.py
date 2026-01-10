"""
Tests para el ejercicio ej1a1.py
Este archivo contiene pruebas para verificar la correcta implementación
de la función get_user_ip usando el formato de texto plano.
"""

import pytest
import responses
from unittest.mock import patch, Mock

from ej1a1 import get_user_ip

@pytest.fixture
def mock_responses():
    """
    Fixture para configurar respuestas simuladas para las peticiones HTTP
    """
    with responses.RequestsMock() as rsps:
        # Configurar respuesta para la petición de IP en formato texto plano
        rsps.add(
            responses.GET,
            "https://api.ipify.org",
            body="98.207.254.136",
            status=200
        )
        yield rsps

def test_get_user_ip(mock_responses):
    """
    Prueba la función get_user_ip cuando la petición es exitosa.
    """
    result = get_user_ip()
    assert result == "98.207.254.136"

def test_get_user_ip_failure():
    """
    Prueba la función get_user_ip cuando la petición falla.
    """
    with patch('requests.get') as mock_get:
        # Configurar el mock para simular un error
        mock_get.side_effect = Exception("Connection error")
        result = get_user_ip()
        assert result is None

@patch('requests.get')
def test_get_user_ip_bad_status(mock_get):
    """
    Prueba la función get_user_ip cuando la petición devuelve un código de error.
    """
    # Configurar la respuesta del mock con un código de error
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    result = get_user_ip()
    assert result is None
