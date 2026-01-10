import pytest
import threading
import requests
import json
import time
from ej1a3 import create_server

@pytest.fixture
def server():
    """
    Fixture para iniciar y detener el servidor HTTP durante las pruebas
    """
    # Crear el servidor en un puerto específico para pruebas
    server = create_server(host="localhost", port=8888)

    # Iniciar el servidor en un hilo separado
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

    # Esperar un momento para que el servidor se inicie
    time.sleep(0.5)

    yield server

    # Detener el servidor después de las pruebas
    server.shutdown()
    server.server_close()
    thread.join(1)

def test_ip_endpoint(server):
    """
    Prueba el endpoint /ip para validar que devuelve la IP del cliente en formato JSON.
    """
    response = requests.get("http://localhost:8888/ip")
    assert response.status_code == 200, "El código de estado debe ser 200."
    assert response.headers['Content-Type'] == 'application/json', "El tipo de contenido debe ser application/json."

    # Convertir la respuesta a JSON
    data = json.loads(response.text)

    # Verificar que la respuesta contiene el campo 'ip'
    assert 'ip' in data, "La respuesta debe contener el campo 'ip'."
    # Verificar que el campo 'ip' no está vacío
    assert data['ip'], "El campo 'ip' no debe estar vacío."
    # Verificar formato básico de IP (podría ser IPv4 o IPv6)
    assert isinstance(data['ip'], str), "El campo 'ip' debe ser una cadena de texto."

def test_nonexistent_endpoint(server):
    """
    Prueba un endpoint que no existe para validar que devuelve un código de error 404.
    """
    response = requests.get("http://localhost:8888/nonexistent")
    assert response.status_code == 404, "El código de estado debe ser 404 para rutas inexistentes."
