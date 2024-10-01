import unittest
from monday_api.authentication import MondayAuth

class TestMondayAuth(unittest.TestCase):
    def test_auth_headers(self):
        # Crear autenticación
        api_token = os.getenv("MONDAY_API_TOKEN")
        auth = MondayAuth(token=api_token)
        headers = auth.get_headers()
        self.assertIn("Authorization", headers)
