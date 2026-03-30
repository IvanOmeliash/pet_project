import httpx
from fastapi import HTTPException

# Адреса іншого сервісу
USER_SERVICE_URL = "http://localhost:8001/api/v1/users"


async def get_remote_user(user_id: int):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{USER_SERVICE_URL}/{user_id}")

            if response.status_code == 404:
                return None

            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="User Service помилка")

            return response.json()  # Повертає дані юзера (username, weight тощо)
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="User Service недоступний")