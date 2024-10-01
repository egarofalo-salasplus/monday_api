from monday_api import MondayAuth, MondayTasks
import pandas as pd
import os

# Crear autenticación
api_token = os.getenv("MONDAY_API_TOKEN")
auth = MondayAuth(token=api_token)

class Utils:
    """ Clase que facilita la interacción con los datos obtenidos desde la API de Monday.com
    """

    def __init__(self):
        """
        Inicializa la clase Utils con la autenticación proporcionada.
        """
        api_token = os.getenv("MONDAY_API_TOKEN")
        self.auth = MondayAuth(token=api_token)

    def board_to_csv(self, items, path="items.csv", sub_items=True):
        """
        Obtiene todos los items (tareas) de un tablero en Monday.com, y crea una archivo csv
        con items y sub-items. Devuelve un Pandas.DataFrame con los datos consolidados.
        Este método asume que los elementos y sub-elementos contienen la misma cantidad y tipo
        de columnas.

        Parameters
        ----------
        items: list
            Una lista de diccionarios donde cada diccionario contiene la información de un item,
                incluyendo subitems y sus valores de columna.
        path: string
            Camino para guardar el archivo csv proveniente del DataFrame
        sub_items: boolean
            Booleano para activar al extracción de sub-items del tablero
            
        Returns
        -------
        DataFrame
            Una lista de diccionarios donde cada diccionario contiene la información de un
                item (id y name).
        """
        
        tasks = []
        columns = {}
        for item in items:
            task = []
            task.append(item["id"])
            columns["id"] = ""
            task.append(item["name"])
            columns["name"] = ""
            for column in item["column_values"]:
                if column["id"] != "subelementos__1":
                    task.append(column["text"])
                    columns[column["id"]] = ""
            task.append("None")
            columns["Father"] = ""
            tasks.append(task)
            if item["subitems"] != [] and sub_items:
                for sub_item in item["subitems"]:
                    task = []
                    task.append(sub_item["id"])
                    task.append(sub_item["name"])
                    for sub_column in sub_item["column_values"]:
                        task.append(sub_column["text"])
                    task.append(item["id"])
                    tasks.append(task)
        
        # Crear el DataFrame
        df = pd.DataFrame(data=tasks, columns=list(columns.keys()))

        df.to_csv(path)

        return df


    