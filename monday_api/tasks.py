from .authentication import MondayAuth
import requests

class MondayTasks:
    def __init__(self, auth: MondayAuth):
        self.auth = auth
        self.url = "https://api.monday.com/v2"
        self.headers = auth.get_headers()
    
    def get_first_page_items(self, board_id):
        """Obtiene la primera página de items de un tablero y devuelve el cursor y los items."""
        query = f"""
        query {{
        boards (ids: {board_id}) {{
            items_page {{
            cursor
            items {{
                id 
                name 
            }}
            }}
        }}
        }}
        """
        response = requests.post(self.url, headers=self.headers, json={'query': query})
        data = response.json()

        cursor = data['data']['boards'][0]['items_page']['cursor']
        items = data['data']['boards'][0]['items_page']['items']
        return cursor, items
        
    def get_next_page_items(self, cursor):
        """Obtiene la siguiente página de items utilizando el cursor."""
        query = f"""
        query {{
          next_items_page (cursor: "{cursor}") {{
            cursor
            items {{
              id 
              name 
            }}
          }}
        }}
        """
        
        response = requests.post(self.url, headers=self.headers, json={'query': query})
        data = response.json()

        cursor = data['data']['next_items_page']['cursor']
        items = data['data']['next_items_page']['items']
        return cursor, items
    
    def get_all_items(self, board_id):
        """Obtiene todos los items de un tablero iterando sobre todas las páginas."""
        all_items = []

        # Obtener la primera página de items
        cursor, items = self.get_first_page_items(board_id)
        all_items.extend(items)
        
        # Seguir obteniendo las siguientes páginas hasta que el cursor sea None
        while cursor:
            cursor, items = self.get_next_page_items(cursor)
            all_items.extend(items)
        
        return all_items
