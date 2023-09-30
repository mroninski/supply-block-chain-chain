import duckdb
from pydantic import BaseModel, SecretStr

from api.database import db_obj


class Asset(BaseModel):
    """
    Example model for a vehicle's details
    """

    VIN: str
    Make: str
    Model: str
    Year: int
    Owner: str
    AppraisedValue: int

    __sql_defition__: str = """
    CREATE TABLE IF NOT EXISTS models.assets (
        VIN VARCHAR(17) NOT NULL UNIQUE,
        Make VARCHAR(255) NOT NULL,
        Model VARCHAR(255) NOT NULL,
        Year INTEGER NOT NULL,
        Owner VARCHAR(255) NOT NULL,
        AppraisedValue INTEGER NOT NULL
    );
    """


def post_import_process():
    """
    This function is called after the import of this module
    """

    db_obj.query("Create schema if not exists models;")
    db_obj.query(Asset.__sql_defition__)
    db_obj.save()


post_import_process()
