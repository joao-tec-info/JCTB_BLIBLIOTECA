import httpx
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.environ.get(
    "API_BASE_URL"
)


class APIService:

    # ---------------- BOOKS ----------------

    @staticmethod
    async def list_books():

        async with httpx.AsyncClient() as client:

            response = await client.get(
                f"{API_BASE_URL}/books/"
            )

            return response.json()

    @staticmethod
    async def create_book(data: dict):

        async with httpx.AsyncClient() as client:

            response = await client.post(
                f"{API_BASE_URL}/books/",
                json=data
            )

            return response.json()

    @staticmethod
    async def update_book(book_id: str, data: dict):

        async with httpx.AsyncClient() as client:

            response = await client.put(
                f"{API_BASE_URL}/books/{book_id}",
                json=data
            )

            return response.json()

    @staticmethod
    async def delete_book(book_id: str):

        async with httpx.AsyncClient() as client:

            response = await client.delete(
                f"{API_BASE_URL}/books/{book_id}"
            )

            return response.json()

    # ---------------- STUDENTS ----------------

    @staticmethod
    async def list_students():

        async with httpx.AsyncClient() as client:

            response = await client.get(
                f"{API_BASE_URL}/students/"
            )

            return response.json()

    @staticmethod
    async def create_student(data: dict):

        async with httpx.AsyncClient() as client:

            response = await client.post(
                f"{API_BASE_URL}/students/",
                json=data
            )

            return response.json()

    @staticmethod
    async def update_student(student_id: str, data: dict):

        async with httpx.AsyncClient() as client:

            response = await client.put(
                f"{API_BASE_URL}/students/{student_id}",
                json=data
            )

            return response.json()

    @staticmethod
    async def delete_student(student_id: str):

        async with httpx.AsyncClient() as client:

            response = await client.delete(
                f"{API_BASE_URL}/students/{student_id}"
            )

            return response.json()

    # ---------------- LOANS ----------------

    @staticmethod
    async def list_loans():

        async with httpx.AsyncClient() as client:

            response = await client.get(
                f"{API_BASE_URL}/loans/"
            )

            return response.json()

    @staticmethod
    async def create_loan(data: dict):

        async with httpx.AsyncClient() as client:

            response = await client.post(
                f"{API_BASE_URL}/loans/",
                json=data
            )

            return response.json()
        
    @staticmethod
    async def return_loan(loan_id: str):

        async with httpx.AsyncClient() as client:

            response = await client.put(
                f"{API_BASE_URL}/loans/{loan_id}/return"
            )

            return response.json()


api = APIService()