import httpx


class WeatherService:

    async def get_weather(
        self,
        latitude,
        longitude
    ):

        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={latitude}"
            f"&longitude={longitude}"
            f"&current=temperature_2m,"
            f"relative_humidity_2m,"
            f"surface_pressure,"
            f"wind_speed_10m"
        )

        async with httpx.AsyncClient() as client:

            response = await client.get(
                url,
                timeout=30
            )

        return response.json()