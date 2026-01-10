"""
Enunciado:
Continuando con la biblioteca requests de Python.
En este ejercicio, aprenderás a trabajar con respuestas en formato JSON.

En este ejercicio, aprenderás a:
1. Realizar una petición GET a una API pública
2. Interpretar una respuesta en formato JSON
3. Extraer información específica de un objeto JSON

Tu tarea es completar la función indicada para realizar una consulta a la API
de ipify.org usando el formato JSON, que es más estructurado que el texto plano.
"""

import requests

def get_user_ip_json():
    """
    Realiza una petición GET a api.ipify.org para obtener la dirección IP pública
    en formato JSON.
    """
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("ip")
            return None
    except Exception:
        return None


def get_response_info():
    """
    Obtiene información adicional sobre la respuesta HTTP al consultar la API.
    """
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=5)

        if response.status_code == 200:
            return {
                "content_type": response.headers.get("Content-Type"),
                "elapsed_time": response.elapsed.total_seconds() * 1000,
                "response_size": len(response.content)
            }
            return None

    except Exception:
        return None


if __name__ == "__main__":
    ip = get_user_ip_json()
    if ip:
        print(f"Tu dirección IP pública es: {ip}")

        info = get_response_info()
        if info:
            print("\nInformación de la respuesta:")
            print(f"Tipo de contenido: {info['content_type']}")
            print(f"Tiempo de respuesta: {info['elapsed_time']} ms")
            print(f"Tamaño de la respuesta: {info['response_size']} bytes")
    else:
        print("No se pudo obtener la dirección IP")
