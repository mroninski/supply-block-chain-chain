import duckdb
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from api.database import db_obj
from api.models import Asset

app = FastAPI()


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
            ],
        )
        db_obj.save()
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
                AppraisedValue = ?
            WHERE VIN = ?
            """,
            query_args=[
                asset.Make,
                asset.Model,
                asset.Year,
                asset.Owner,
                asset.AppraisedValue,
                asset.VIN,
            ],
        )

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
