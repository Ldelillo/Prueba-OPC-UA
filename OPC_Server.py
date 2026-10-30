import asyncio
import uvicorn

from api.api import app

from services.weather_parser import WeatherParser
from services.opc_service import OPCService
from services.weather_service import WeatherService
from services.locations_manager import LocationsManager


async def start_api():

    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=8000
    )

    server = uvicorn.Server(config)

    await server.serve()


async def main():

    parser = WeatherParser()

    opc = OPCService()

    weather = WeatherService()

    manager = LocationsManager()

    await opc.start()

    asyncio.create_task(
        start_api()
    )

    for location in manager.get_locations():

        await opc.create_location(
            location["name"]
        )

    ultima_hora = {}

    try:

        while True:

            locations = manager.get_locations()

            for location in locations:

                name = location["name"]

                data = await weather.get_weather(
                    location["latitude"],
                    location["longitude"]
                )

                current_time = data["current"]["time"]

                if (
                    name not in ultima_hora
                    or
                    current_time
                    != ultima_hora[name]
                ):

                    ultima_hora[name] = current_time

                    await opc.update_location(
                        name,
                        data["current"]["temperature_2m"],
                        data["current"]["relative_humidity_2m"],
                        data["current"]["surface_pressure"],
                        data["current"]["wind_speed_10m"]
                    )

                    parser.save_measure(
                        location["name"],
                        current_time,
                        location["latitude"],
                        location["longitude"],
                        data["current"]["temperature_2m"],
                        data["current"]["relative_humidity_2m"],
                        data["current"]["surface_pressure"],
                        data["current"]["wind_speed_10m"]
                    )

                    #print(
                    #    f"{name}: "
                    #    f"{data['current']['temperature_2m']} °C"
                    #)

            await asyncio.sleep(60)

    finally:

        await opc.stop()


asyncio.run(main())