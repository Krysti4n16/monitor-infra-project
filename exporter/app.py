import time
import requests
import os
from prometheus_client import start_http_server, Gauge, Counter

TARGET_URL = os.getenv("TARGET_URL", "http://localhost:8080")

WEB_STATUS = Gauge('website_up', 'Web status: 1<->UP, 0 <-> DOWN')
RESPONSE_TIME = Gauge('website_response_seconds', 'Response time')
CHECK_COUNT = Counter('website_check_total', 'How many times we checked the server')

def check_website():
    CHECK_COUNT.inc()
    try:
        start_time = time.time()
        response = requests.get(TARGET_URL, timeout=2)
        duration = time.time() - start_time
        
        RESPONSE_TIME.set(duration)
        
        if response.status_code == 200:
            WEB_STATUS.set(1)
            print(f"Status OK. Time: {duration:.2f}s")
        else:
            WEB_STATUS.set(0)
            print(f"Error HTTP: {response.status_code}")
            
    except Exception as e:
        WEB_STATUS.set(0)
        print(f"CRITICAL ERROR: {e}")

if __name__ == '__main__':
    print("Starting SERVER on port:8000")
    start_http_server(8000)
    
    while True:
        check_website()
        time.sleep(5)
