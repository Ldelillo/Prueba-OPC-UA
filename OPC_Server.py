from asyncua import Server
import asyncio
import httpx as requests
from fastapi import FastAPI
import uvicorn
from parser import WeatherParser

#Busqueda de datos en la API de Open-Meteo
latitud = 40.398121
longitud = -3.791635
coordChange = False
#Actualización de coordenadas con FASTAPI
app = FastAPI() 
@app.put("/update_coordinates")
async def update_coordinates(lat: float, lon: float):
    global latitud, longitud, coordChange
    latitud = lat
    longitud = lon
    coordChange = True
    return {"message": "Coordenadas actualizadas correctamente"}

async def start_api():

    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=8000
    )

    server = uvicorn.Server(config)

    await server.serve()

async def main():
    global coordChange
    # Creación del servidor OPC-UA
    server = Server()
    await server.init()
    # Creación de la tarea para iniciar el servidor FastAPI
    api_task = asyncio.create_task(start_api())
    # Configuración del endpoint del servidor OPC-UA
    server.set_endpoint("opc.tcp://0.0.0.0:4840")

    uri = "http://lab-opcua"
    idx = await server.register_namespace(uri)

    objects = server.nodes.objects

    tiempo = await  objects.add_object(idx, "TiempoReal")

    coord = await tiempo.add_variable(idx, "Coordenadas", (latitud, longitud))
    temp = await tiempo.add_variable(idx, "Temperatura", 0.0)
    humedad = await tiempo.add_variable(idx, "Humedad", 0)
    presion = await tiempo.add_variable(idx, "Presion", 0.0)
    viento = await tiempo.add_variable(idx, "Viento", 0.0)

    await coord.set_writable()
    await temp.set_writable()
    await humedad.set_writable()
    await presion.set_writable()
    await viento.set_writable()

    await server.historize_node_data_change(temp, period=None, count=100)
    await server.historize_node_data_change(humedad, period=None, count=100)
    await server.historize_node_data_change(presion, period=None, count=100)
    await server.historize_node_data_change(viento, period=None, count=100)

    await server.start()

    print("Servidor OPC-UA arrancado")
    ultimaHora = None
    parser = WeatherParser()
    try:
        while True:
            async with requests.AsyncClient() as client:
                respuesta = await client.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitud}&longitude={longitud}&current=temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m", timeout=30)
            if respuesta.status_code == 200:
                datos = respuesta.json()
                if coordChange or datos["current"]["time"] != ultimaHora:
                    ultimaHora = datos["current"]["time"]
                    #Actualización de valores en el servidor OPC-UA
                    await coord.write_value((latitud, longitud))
                    await temp.write_value(datos["current"]["temperature_2m"])
                    await humedad.write_value(datos["current"]["relative_humidity_2m"])
                    await presion.write_value(datos["current"]["surface_pressure"])
                    await viento.write_value(datos["current"]["wind_speed_10m"])  
                    coordChange = False 
                    #Guardado de datos en CSV
                    parser.save_measure(
                        ultimaHora,
                        latitud,
                        longitud,
                        datos["current"]["temperature_2m"],
                        datos["current"]["relative_humidity_2m"],
                        datos["current"]["surface_pressure"],
                        datos["current"]["wind_speed_10m"]) 
            await asyncio.sleep(60)

    except asyncio.CancelledError:
        api_task.cancel()
        print("Tarea cancelada")

    finally:
        await server.stop()

asyncio.run(main())

