from .authentication import MondayAuth
import requests

class MondayBoards:
    def __init__(self, auth: MondayAuth):
        self.auth = auth
        self.url = "https://api.monday.com/v2"
    
    def get_boards(self):
        
        query = '{"query": "{ boards { id name } }"}'
        
        response = requests.post(self.url, headers=self.auth.get_headers(), data=query)
        return response.json()

    def get_board(self, board_id):
        query = f'{{"query": "{{ boards(ids: {board_id}) {{ id name items {{ id name }} }} }}"}}'
        
        response = requests.post(self.url, headers=self.auth.get_headers(), data=query)
        return response.json()
