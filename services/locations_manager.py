import csv
import os


class LocationsManager:

    def __init__(self, filename="data/locations.csv"):

        self.filename = filename

        if not os.path.exists(self.filename):

            with open(
                self.filename,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(file)

                writer.writerow([
                    "name",
                    "latitude",
                    "longitude"
                ])

    def get_locations(self):

        locations = []

        with open(
            self.filename,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                locations.append({
                    "name": row["name"],
                    "latitude": float(row["latitude"]),
                    "longitude": float(row["longitude"])
                })

        return locations

    def add_location(
        self,
        name,
        latitude,
        longitude
    ):

        locations = self.get_locations()

        for location in locations:

            if location["name"].lower() == name.lower():

                raise ValueError(
                    f"La ubicación '{name}' ya existe"
                )

            if (
                location["latitude"] == latitude
                and
                location["longitude"] == longitude
            ):

                raise ValueError(
                    "Ya existe una ubicación con esas coordenadas"
                )

        with open(
            self.filename,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                name,
                latitude,
                longitude
            ])

    def delete_location(
        self,
        name
    ):

        locations = self.get_locations()

        locations = [
            location
            for location in locations
            if location["name"].lower()
            != name.lower()
        ]

        with open(
            self.filename,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "name",
                "latitude",
                "longitude"
            ])

            for location in locations:

                writer.writerow([
                    location["name"],
                    location["latitude"],
                    location["longitude"]
                ])

    def location_exists(
        self,
        name
    ):

        locations = self.get_locations()

        return any(
            location["name"].lower()
            == name.lower()
            for location in locations
        )