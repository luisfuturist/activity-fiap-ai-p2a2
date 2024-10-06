import math
import dotenv
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy import text
import pandas as pd

from db import engine

dotenv.load_dotenv()

SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()


import math


def calculate_distance_meters(lat1: float, lon1: float, lat2: float, lon2: float):
    R = 6371000.0  # Radius of the Earth in meters

    # Convert degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Differences in coordinates
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # Haversine formula
    a = (math.sin(dlat / 2) ** 2) + (
        math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distance in meters
    distance = R * c

    return distance


def fetch_data(analysis_date: str = datetime.now().strftime("%d-%m-%Y")):
    print("Fetching data for date:", analysis_date)
    analysis_date = datetime.strptime(analysis_date, "%d-%m-%Y")

    query = f"""
        SELECT 
            id_datalog as id_datalog,
            species.id_species as id_species,
            species.name as species_name,
            breeds.id_breed as id_breed,
            breeds.name as breed_name,
            animals.id_animal as id_animal,
            animals.name as animal_name,
            cast(datalog.temperature as float) as temperature,
            cast(datalog.heartrate as float) as heartrate,
            cast(datalog.latitude as float) as latitude,
            cast(datalog.longitude as float) as longitude,
            datalog.created_at as created_at,
            datalog.updated_at as updated_at,
            datalog.is_outlier as is_outlier
        FROM t_wc_datalog datalog
        LEFT JOIN t_wc_animals_collars animal_collars ON datalog.id_animal_collar = animal_collars.id_animal_collar
        LEFT JOIN t_wc_animals animals ON animal_collars.id_animal = animals.id_animal
        LEFT JOIN t_wc_species species ON animals.id_species = species.id_species
        LEFT JOIN t_wc_breeds breeds ON animals.id_breed = breeds.id_breed
        WHERE cast(datalog.created_at as Date) = '{analysis_date}'
    """

    result = session.execute(text(query)).fetchall()

    df = pd.DataFrame(
        result,
        columns=[
            "id_datalog",
            "id_species",
            "species_name",
            "id_breed",
            "breed_name",
            "id_animal",
            "animal_name",
            "temperature",
            "heartrate",
            "latitude",
            "longitude",
            "created_at",
            "updated_at",
            "is_outlier",
        ],
    )

    df["delta_distance_meters"] = df.apply(
        lambda row: (
            calculate_distance_meters(
                float(row["latitude"]),
                float(row["longitude"]),
                float(df["latitude"].shift(1).loc[row.name]),
                float(df["longitude"].shift(1).loc[row.name]),
            )
            if row.name > 0
            else 0
        ),
        axis=1,
    )

    animal_distance_traveled = df.groupby("id_animal")["delta_distance_meters"].sum()

    data = {}

    for species_id, species_group in df.groupby("id_species"):
        species_name = species_group["species_name"].iloc[0]
        data[species_name] = {}

        for breed_id, breed_group in species_group.groupby("id_breed"):
            breed_name = breed_group["breed_name"].iloc[0]

            animal_distance_traveled = breed_group.groupby("id_animal")[
                "delta_distance_meters"
            ].sum()

            data[species_name][breed_name] = {
                "count": breed_group["id_animal"].nunique(),
                "mean_temperature": round(float(breed_group["temperature"].mean()), 2),
                "max_temperature": round(float(breed_group["temperature"].max()), 2),
                "min_temperature": round(float(breed_group["temperature"].min()), 2),
                "mean_heartrate": round(float(breed_group["heartrate"].mean()), 2),
                "max_heartrate": round(float(breed_group["heartrate"].max()), 2),
                "min_heartrate": round(float(breed_group["heartrate"].min()), 2),
                "total_distance_traveled_meters": round(
                    float(animal_distance_traveled.sum()), 2
                ),
                "mean_distance_traveled_meters": round(
                    float(animal_distance_traveled.mean()), 2
                ),
                "max_distance_traveled_meters": round(
                    float(animal_distance_traveled.max()), 2
                ),
                "min_distance_traveled_meters": round(
                    float(animal_distance_traveled.min()), 2
                ),
            }

    return data