class ApiService:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get(self, path: str):
        return f"GET {self.base_url}/{path}"
