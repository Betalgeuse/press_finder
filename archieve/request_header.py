import requests
import time

response = requests.get('https://google.com')
if response.status_code == 429:
    retry_after = int(response.headers.get('Retry-After', 0))
    time.sleep(retry_after)
    response = requests.get('https://google.com')