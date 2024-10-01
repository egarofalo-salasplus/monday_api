import requests

class MondayAuth:
    def __init__(self, token):
        self.token = token
        self.headers = {
            "Authorization": self.token,
            "Content-Type": "application/json"
        }
    
    def get_headers(self):
        return self.headers
