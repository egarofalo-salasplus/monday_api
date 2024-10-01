from monday_api import MondayAuth, MondayBoards, MondayTasks, utils
import pandas as pd
import json
import os
import re

# Crear autenticación
api_token = os.getenv("MONDAY_API_TOKEN")
auth = MondayAuth(token=api_token)

# Obtener tableros
monday_boards = MondayBoards(auth)
boards = monday_boards.get_boards()

board_names = ["DM: Gobierno de Datos y Custodia", 
               "DM: Hoja de ruta",
               "DM: Proyectos",
               "Proyectos de automatización",
               "Pendientes (Enzo)"]

for board_name in board_names:
    board_id = ""
    for board in boards["data"]["boards"]:
        if board["name"] == board_name:
            board_id = board["id"]

    # Obtener tareas de un tablero
    tasks = MondayTasks(auth)
    all_tasks_board = tasks.get_all_items(int(board_id))

    tool = utils.Utils()

    # Limpiar nombre de caracteres especiales
    invalid_chars = r'[\/:*?"<>|]'
    export_name = f"V:\\SALAS_Arees\\Gestió de Dades\\INFORMES\\Control de rendimiento DM\\Data\\monday_{re.sub(invalid_chars, "", board_name)}.csv"

    df = tool.board_to_csv(all_tasks_board, path=export_name, sub_items=True)
