import requests

def get_dolar():
    # URL de la API (aquí utilizamos Exchange Rates API como ejemplo)
    url = f"https://api.exchangerate-api.com/v4/latest/USD"
    
    # Realizar la solicitud GET
    response = requests.get(url)
    data = response.json()

    # Obtener el valor del dólar en pesos colombianos
    tasa_cop = data["rates"].get("COP")

    # Pasar la tasa a la plantilla
    return tasa_cop