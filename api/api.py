from fastapi import FastAPI, HTTPException

from services.locations_manager import LocationsManager

app = FastAPI()

manager = LocationsManager()


@app.get("/")
async def root():

    return {
        "service": "OPC-UA Weather Server",
        "status": "running"
    }


@app.get("/locations")
async def get_locations():

    return manager.get_locations()


@app.post("/locations")
async def add_location(
    name: str,
    latitude: float,
    longitude: float
):

    try:

        manager.add_location(
            name,
            latitude,
            longitude
        )

        return {
            "message": f"{name} añadida correctamente"
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@app.delete("/locations/{name}")
async def delete_location(
    name: str
):

    if not manager.location_exists(name):

        raise HTTPException(
            status_code=404,
            detail=f"La ubicación '{name}' no existe"
        )

    manager.delete_location(name)

    return {
        "message": f"{name} eliminada correctamente"
    }