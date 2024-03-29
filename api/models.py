from pydantic import BaseModel
from typing import Optional, List, Any, Dict

from api.database import db_obj
from datetime import datetime
from uuid import UUID


def model_from_args(model, args):
    assert len(model.model_fields) == len(
        args
    ), "Number of arguments does not match number of fields in model"

    return model(**{field: arg for field, arg in zip(model.model_fields, args)})


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
    Accident: int = 0

    __sql_defition__: str = """
    CREATE TABLE IF NOT EXISTS models.assets (
        VIN VARCHAR(17) NOT NULL UNIQUE,
        Make VARCHAR(255) NOT NULL,
        Model VARCHAR(255) NOT NULL,
        Year INTEGER NOT NULL,
        Owner VARCHAR(255) NOT NULL,
        AppraisedValue INTEGER NOT NULL,
        Accident INTEGER NOT NULL
    );
    """


class Part(BaseModel):
    SupplierID: str
    ProductID: UUID
    LogisticsProviderID: str
    PartName: str
    PartQuantity: int
    RequiredArrivalDate: datetime
    # Options for shipment methods: "Air", "Sea", "Land"
    ShipmentMethods: str
    ShipmentDate: datetime
    PartLocation: str

    __sql_defition__: str = """
    CREATE TABLE IF NOT EXISTS models.parts (
        SupplierID VARCHAR(255) NOT NULL,
        ProductID UUID NOT NULL,
        LogisticsProviderID VARCHAR(255) NOT NULL,
        PartName VARCHAR(255) NOT NULL,
        PartQuantity INTEGER NOT NULL,
        RequiredArrivalDate TIMESTAMP NOT NULL,
        ShipmentMethods VARCHAR(255) NOT NULL,
        ShipmentDate TIMESTAMP NOT NULL,
        PartLocation VARCHAR(255) NOT NULL
    );
    """


class TransactionHistory(BaseModel):
    EndpointRequest: str
    RequestTime: datetime
    ResponseStatus: int

    __sql_defition__: str = """
    CREATE TABLE IF NOT EXISTS models.transaction_history (
        EndpointRequest VARCHAR(255) NOT NULL,
        RequestTime TIMESTAMP NOT NULL,
        ResponseStatus INTEGER NOT NULL
    );
    """


def post_import_process():
    """
    This function is called after the import of this module
    """

    db_obj.query("Create schema if not exists models;")
    db_obj.query(Asset.__sql_defition__)
    db_obj.query(Part.__sql_defition__)
    db_obj.query(TransactionHistory.__sql_defition__)
    db_obj.save()


post_import_process()
