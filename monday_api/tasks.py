from .authentication import MondayAuth
import requests

class MondayTasks:
    """
    Clase para interactuar con la API de Monday.com y obtener tareas (items) de un tablero específico.

    Parameters
    ----------
    auth : MondayAuth
        Instancia de la clase `MondayAuth`, que contiene el token de autenticación y las cabeceras necesarias para las peticiones.

    Attributes
    ----------
    auth : MondayAuth
        Instancia de la clase `MondayAuth`.
    url : str
        La URL base de la API de Monday.com.
    headers : dict
        Cabeceras HTTP para las peticiones a la API, incluyendo el token de autenticación.
    """

    def __init__(self, auth: MondayAuth):
        """
        Inicializa la clase MondayTasks con la autenticación proporcionada.

        Parameters
        ----------
        auth : MondayAuth
            Instancia de autenticación que contiene las cabeceras necesarias para realizar peticiones a la API de Monday.
        """
        self.auth = auth
        self.url = "https://api.monday.com/v2"
        self.headers = auth.get_headers()
    
    def get_first_page_items(self, board_id):
        """
        Obtiene la primera página de items (tareas) de un tablero específico en Monday.com.

        Parameters
        ----------
        board_id : int
            El ID del tablero de Monday del cual se desean obtener los items.

        Returns
        -------
        tuple
            cursor : str
                El cursor devuelto por la API para obtener las siguientes páginas de items.
            items : list
                Una lista de diccionarios donde cada diccionario contiene la información de un item,
                incluyendo subitems y sus valores de columna.
        """
        query = f"""
        query {{
          boards (ids: {board_id}) {{
            items_page {{
              cursor
              items {{
                id 
                name
                column_values {{
                  id
                  type
                  text
                }}
                subitems {{
                  id
                  name
                  column_values {{
                    id
                    type
                    text
                  }}
                }}
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
        """
        Obtiene la siguiente página de items (tareas) utilizando el cursor.

        Parameters
        ----------
        cursor : str
            El cursor devuelto por la API para continuar la paginación de items en el tablero.

        Returns
        -------
        tuple
            cursor : str
                El nuevo cursor devuelto por la API para obtener la página siguiente (si existe).
            items : list
                Una lista de diccionarios donde cada diccionario contiene la información de un item,
                incluyendo subitems y sus valores de columna.
        """
        query = f"""
        query {{
          next_items_page (cursor: "{cursor}") {{
            cursor
            items {{
              id 
              name
              column_values {{
                id
                type
                text
              }}
              subitems {{
                id
                name
                column_values {{
                  id
                  type
                  text
                }}
              }}
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
        """
        Obtiene todos los items (tareas) de un tablero en Monday.com, iterando a través de todas las páginas disponibles.

        Parameters
        ----------
        board_id : int
            El ID del tablero de Monday del cual se desean obtener todos los items.

        Returns
        -------
        list
            Una lista de diccionarios donde cada diccionario contiene la información de un item,
                incluyendo subitems y sus valores de columna.
        """
        all_items = []

        # Obtener la primera página de items
        cursor, items = self.get_first_page_items(board_id)
        all_items.extend(items)
        
        # Seguir obteniendo las siguientes páginas hasta que el cursor sea None
        while cursor:
            cursor, items = self.get_next_page_items(cursor)
            all_items.extend(items)
        
        return all_items
    