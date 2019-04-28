import requests
from log import log as log
import time

class NikeCAUnidaysFarmer:
    def __init__(self, email, password):
        self.s = requests.session()
        self.s.headers = {
            "Origin": "https://www.myunidays.com",
            "ud-source": "www"
        }
        self.email = email
        self.password = password
        self.logged_in = False

    def login(self):
        # Login to UNIDAYS
        payload = {
            "QueuedPath": "/CA/en-CA/partners/nike/access/online",
            "EmailAddress": self.email,
            "Password": self.password,
            "Human": ""
        }

        r = self.s.post("https://account.myunidays.com/CA/en-CA/account/log-in", data=payload, verify=False)

        # Check if login was successful
        if(r.status_code == 200):
            self.logged_in = True
        else:
            log('e', "Error logging in. Please check your credentials.")

    def get_code(self):
        # Get the code
        payload = {
            "forceNew": "true"
        }

        r = self.s.post("https://perks.myunidays.com/access/nike/online", data=payload, verify=False)

        # Save the code
        if(r.status_code == 200):
            code = r.json()["code"]
            log('s', "Got code: " + code)
            file = open("unidays.txt", "a")
            file.write(code + "\n")
            file.close()
        else:
            log('e', "Error getting code")

    def start(self):
        # Login
        self.login()

        # Start farming codes
        while(self.logged_in):
            # Get a UNIDAYS code
            self.get_code()
            # Wait for cooldown to end
            time.sleep(3900)

if(__name__ == "__main__"):
    # Ignore insecure request warnings
    requests.packages.urllib3.disable_warnings()

    # Get username and password
    try:
        file = open("settings.txt", "r")
        settings = file.readlines()
        email = settings[0].strip()
        password = settings[1].strip()
        ready = True
    except Exception as e:
        log('e', "Settings file corrupted! Exiting...")
        ready = False

    # Start farming codes
    if(ready):
        NikeCAUnidaysFarmer(email, password).start()
