from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from api.database import db_obj
from api.models import Asset, Part

app = FastAPI()

# Nice to have

# Build the model from the list so the response is nicer

# Have timestamp of when the event was requested for easier comparison

# Change the position of the lastport + lat + long

# TODO: Add a new endpoint to get the parts from a specific port

# TODO: Add to the database every time we receive a call from the DB


@app.get("/")
async def root():
    """
    Redirect to the docs
    """
    return RedirectResponse(url="./docs/")


@app.post("/assets")
async def create_asset(asset: Asset):
    """
    Populate the DuckDB database with the asset data
    """

    # Check if the asset already exists

    exists = False
    try:
        existance_check = db_obj.query(
            "SELECT VIN FROM models.assets WHERE VIN = ?", query_args=[asset.VIN]
        )

        exists = len(existance_check) > 0
    except Exception as e:
        return {"ResponseDB": e}

    if exists is False:
        response = db_obj.query(
            """
            INSERT INTO models.assets
            VALUES (
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?
            )
            """,
            query_args=[
                asset.VIN,
                asset.Make,
                asset.Model,
                asset.Year,
                asset.Owner,
                asset.AppraisedValue,
                asset.Accident,
            ],
        )
    else:
        # Update the asset
        response = db_obj.query(
            """
            UPDATE models.assets
            SET
                Make = ?,
                Model = ?,
                Year = ?,
                Owner = ?,
                AppraisedValue = ?,
                Accident = ?
            WHERE VIN = ?
            """,
            query_args=[
                asset.Make,
                asset.Model,
                asset.Year,
                asset.Owner,
                asset.AppraisedValue,
                asset.Accident,
                asset.VIN,
            ],
        )

    db_obj.save()

    return {"ResponseDB": response}


@app.get("/assets")
async def get_all_assets():
    """
    Get all assets from the DuckDB database
    """

    response = db_obj.query("SELECT * FROM models.assets")

    return {"ResponseDB": response}


@app.get("/assets/{vin}")
async def get_asset(vin: str):
    """
    Get all assets from the DuckDB database
    """

    try:
        response = db_obj.query(
            "SELECT * FROM models.assets WHERE VIN = ?", query_args=[vin]
        )
    except Exception as e:
        return {"ResponseDB": e}

    return {"ResponseDB": response}


# New structure, for the parts location
@app.get("/parts")
async def get_all_parts():
    """
    Get all parts from the DuckDB database
    """

    response = db_obj.query("SELECT * FROM models.parts")

    return {"ResponseDB": response}


@app.get("/parts/{part_id}")
async def get_part(part_id: str):
    """
    Get all parts from the DuckDB database
    """

    response = db_obj.query(
        "SELECT * FROM models.parts WHERE PartID = ?", query_args=[part_id]
    )

    positional_map = {
        "PartID": response[0][0],
        "LastPort": response[0][1],
        "LastUpdateDate": response[0][2],
        "PartName": response[0][3],
        "Latitude": response[0][4],
        "Longitude": response[0][5],
    }

    return {"ResponseDB": Part(**positional_map)}


@app.post("/parts/")
async def create_part(part: Part):
    """
    Populate the DuckDB database with the part data
    """

    # Check if the part already exists

    exists = False
    try:
        existance_check = db_obj.query(
            "SELECT PartID FROM models.parts WHERE PartID = ?", query_args=[part.PartID]
        )

        exists = len(existance_check) > 0
    except Exception as e:
        return {"ResponseDB": e}

    if exists is False:
        response = db_obj.query(
            """
            INSERT INTO models.parts
            VALUES (
                ?,
                ?,
                ?,
                ?,
                ?,
                ?
            )
            """,
            query_args=[
                part.PartID,
                part.LastPort,
                part.LastUpdateDate,
                part.PartName,
                part.Latitude,
                part.Longitude,
            ],
        )
        db_obj.save()
    else:
        # Update the part
        response = db_obj.query(
            """
            UPDATE models.parts
            SET
                LastPort = ?,
                LastUpdateDate = ?
                PartName = ?
                Latitude = ?
                Longitude = ?
            WHERE PartID = ?
            """,
            query_args=[
                part.LastPort,
                part.LastUpdateDate,
                part.PartName,
                part.Latitude,
                part.Longitude,
                part.PartID,
            ],
        )

    return {"ResponseDB": response}
