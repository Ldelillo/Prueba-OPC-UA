from opcua import ua, Server
import time
import requests
from fastapi import FastAPI
from datetime import datetime


ultimaHora = None

#Busqueda de datos en la API de Open-Meteo
latitud = 40.435
longitud = -3.813

#Actualización de coordenadas con FASTAPI
app = FastAPI() 
@app.put("/update_coordinates")
async def update_coordinates(lat: float, lon: float):
    global latitud, longitud
    latitud = lat
    longitud = lon
    return {"message": "Coordenadas actualizadas correctamente"}

# Creación del servidor OPC-UA
server = Server()

server.set_endpoint("opc.tcp://0.0.0.0:4840")

uri = "http://lab-opcua"
idx = server.register_namespace(uri)

objects = server.get_objects_node()

tiempo = objects.add_object(idx, "TiempoReal")

hora = tiempo.add_variable(idx, "Hora", "00:00")
temp = tiempo.add_variable(idx, "Temperatura", 0.0)
humedad = tiempo.add_variable(idx, "Humedad", 0)
presion = tiempo.add_variable(idx, "Presion", 0.0)
viento = tiempo.add_variable(idx, "Viento", 0.0)

hora.set_writable()
temp.set_writable()
humedad.set_writable()
presion.set_writable()
viento.set_writable()

server.start()

print("Servidor OPC-UA arrancado")

try:
    while True:
        respuesta = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitud}&longitude={longitud}&current=temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m")
        if respuesta.status_code == 200:
            datos = respuesta.json()
            if datos["current"]["time"] != ultimaHora:
                ultimaHora = datos["current"]["time"]
                hora.set_value(datetime.fromisoformat(ultimaHora).strftime("%H:%M"))
                temp.set_value(datos["current"]["temperature_2m"])
                humedad.set_value(datos["current"]["relative_humidity_2m"])
                presion.set_value(datos["current"]["surface_pressure"])
                viento.set_value(datos["current"]["wind_speed_10m"])
        time.sleep(60)

except KeyboardInterrupt:
    pass

finally:
    server.stop()