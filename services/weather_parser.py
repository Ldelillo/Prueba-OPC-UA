import csv
import os


class WeatherParser:

    def __init__(self):

        os.makedirs(
            "data",
            exist_ok=True
        )

    def save_measure(
        self,
        location_name,
        timestamp,
        latitude,
        longitude,
        temperature,
        humidity,
        pressure,
        wind
    ):

        filename = (
            f"data/{location_name}.csv"
        )

        file_exists = os.path.exists(
            filename
        )

        with open(
            filename,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            if not file_exists:

                writer.writerow([
                    "timestamp",
                    "latitude",
                    "longitude",
                    "temperature",
                    "humidity",
                    "pressure",
                    "wind"
                ])

            writer.writerow([
                timestamp,
                latitude,
                longitude,
                temperature,
                humidity,
                pressure,
                wind
            ])