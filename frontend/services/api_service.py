import httpx

from utils.constants import API_BASE_URL


class ApiService:

    @staticmethod
    async def get_books():

        async with httpx.AsyncClient() as client:

            response = await client.get(
                f"{API_BASE_URL}/books/"
            )

            return response.json()