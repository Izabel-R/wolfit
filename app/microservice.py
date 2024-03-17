import requests

def microservice_request(method, endpoint, **kwargs):
    base_url = 'http://0.0.0.0:5001'  # Example base URL, adjust as needed
    url = f"{base_url}{endpoint}"
    response = requests.request(method, url, **kwargs)
    return response.json(), response.status_code
