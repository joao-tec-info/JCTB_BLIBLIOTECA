import requests

from utils.constants import API_URL


class ApiService:

    @staticmethod
    def get_books():

        response = requests.get(
            f"{API_URL}/books/"
        )

        return response.json()

    @staticmethod
    def create_book(data):

        response = requests.post(
            f"{API_URL}/books/",
            json=data
        )

        return response.json()
