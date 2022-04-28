import requests
import json
from .singletons import logger

session = requests.Session()

headers = {'Content-Type': "application/json", 'Accept': "application/json"}

def fetch_put(url, body):
    logger.info("put: "+str(url))
    logger.info(body)
    try:
        result = session.put(url, headers = headers, json=body)           
        return result.json()
    except Exception:
        return {}

def fetch_post(url, body):
    logger.info("post: "+str(url))
    logger.info(body)
    try:
        result = session.post(url, headers = headers, json=body)           
        return result.json()
    except Exception:
        return {}




