import requests
import os
import json
import random
import threading
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class boatnet:
    def __init__(self) -> None:
        while True:        
            time.sleep(0.1)
            
            requests.get(
                'https://google.ca',
                verify=False,
            )
    
if __name__ == "__main__":
    boatnet()