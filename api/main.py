from fastapi import BackgroundTasks, FastAPI
from fastapi.responses import RedirectResponse

from api.database import db_obj
from api.models import Asset, Part, TransactionHistory, model_from_args
from api.background_task import create_transaction_history

from datetime import datetime

app = FastAPI()

# Update the documentation to show the actual design for the workflow

# Nice to have

# Change the position of the lastport + lat + long


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
async def get_all_parts(background_tasks: BackgroundTasks):
    """
    Get all parts from the DuckDB database
    """

    response = db_obj.query("SELECT * FROM models.parts")

    if len(response) > 0:
        response_model = [model_from_args(Part, r) for r in response]
    else:
        response_model = None

    background_tasks.add_task(
        create_transaction_history,
        TransactionHistory(
            EndpointRequest="GET /parts",
            RequestTime=datetime.utcnow(),
            ResponseStatus=200,
        ),
    )

    return {"data": response_model}


@app.get("/parts/{part_id}")
async def get_part(part_id: str, background_tasks: BackgroundTasks):
    """
    Get all parts from the DuckDB database
    """

    response = db_obj.query(
        "SELECT * FROM models.parts WHERE PartID = ?", query_args=[part_id]
    )

    if len(response) > 0:
        response_model = model_from_args(Part, response[0])
    else:
        response_model = None

    background_tasks.add_task(
        create_transaction_history,
        TransactionHistory(
            EndpointRequest=f"GET /parts/{part_id}",
            RequestTime=datetime.utcnow(),
            ResponseStatus=200,
        ),
    )

    return {"data": response_model, "requestTimestamp": datetime.utcnow()}


@app.post("/parts/")
async def create_part(part: Part, background_tasks: BackgroundTasks):
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
    else:
        # Update the part
        response = db_obj.query(
            """
            UPDATE models.parts
            SET
                LastPort = ?,
                LastUpdateDate = ?,
                PartName = ?,
                Latitude = ?,
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

    background_tasks.add_task(
        create_transaction_history,
        TransactionHistory(
            EndpointRequest=f"POST /parts/{part.PartID}",
            RequestTime=datetime.utcnow(),
            ResponseStatus=200,
        ),
    )
    return {"dbResponse": response}


@app.get("/transactions/")
def get_all_transactions():
    """
    Get all transactions from the DuckDB database
    """

    response = db_obj.query("SELECT * FROM models.transaction_history")

    return {"ResponseDB": response}
