import requests

session = requests.Session()

def fetch(url, body):
    try:
        result = session.put(url, json=body)
        return result.json()
    except Exception:
        return {}

