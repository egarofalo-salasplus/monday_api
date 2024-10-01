from monday_api import MondayAuth, MondayBoards, MondayTasks
import os

# Crear autenticación
api_token = os.getenv("MONDAY_API_TOKEN")
auth = MondayAuth(token=api_token)

# Obtener tableros
# boards = MondayBoards(auth)
# print(boards.get_boards())

# Obtener tareas de un tablero
tasks = MondayTasks(auth)
all_tasks_board = tasks.get_all_items(board_id=1620167066)
for task in all_tasks_board:
    print(f"Tarea: {task['name']} (id:{task['id']})")
