import csv
import os


class WeatherParser:

    def __init__(self, filename="data/weather_history.csv"):

        self.filename = filename

        if not os.path.exists(filename):

            with open(
                filename,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(file)

                writer.writerow([
                    "timestamp",
                    "latitude",
                    "longitude",
                    "temperature",
                    "humidity",
                    "pressure",
                    "wind"
                ])

    def save_measure(
        self,
        timestamp,
        latitude,
        longitude,
        temperature,
        humidity,
        pressure,
        wind
    ):

        with open(
            self.filename,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                timestamp,
                latitude,
                longitude,
                temperature,
                humidity,
                pressure,
                wind
            ])