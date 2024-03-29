import json
import requests
from random import randrange
from datetime import datetime, timedelta
from uuid import uuid4

# Assets
assets_examples = [
    {
        "VIN": "ZFF75VFA4F0568999",
        "Make": "Dodge",
        "Model": "Durango",
        "Year": 2002,
        "Owner": "Koch Inc",
        "AppraisedValue": 37374,
    },
    {
        "VIN": "5UXWX9C55F0775600",
        "Make": "Plymouth",
        "Model": "Neon",
        "Year": 2000,
        "Owner": "Torp-Schultz",
        "AppraisedValue": 156837,
    },
    {
        "VIN": "1C4RDHDG9EC756661",
        "Make": "Hummer",
        "Model": "H1",
        "Year": 2003,
        "Owner": "Schaden-Wolf",
        "AppraisedValue": 347705,
    },
    {
        "VIN": "4F2CY0C74BK131969",
        "Make": "Infiniti",
        "Model": "EX",
        "Year": 2009,
        "Owner": "Veum, Von and Hirthe",
        "AppraisedValue": 191936,
    },
    {
        "VIN": "JTHBW1GG6D2577253",
        "Make": "Hyundai",
        "Model": "Accent",
        "Year": 2010,
        "Owner": "Paucek and Sons",
        "AppraisedValue": 161588,
    },
    {
        "VIN": "KNAFT4A23D5651086",
        "Make": "Acura",
        "Model": "Integra",
        "Year": 1992,
        "Owner": "Yundt-Rice",
        "AppraisedValue": 435357,
    },
    {
        "VIN": "1FTEW1CM7EF694891",
        "Make": "Dodge",
        "Model": "Stealth",
        "Year": 1996,
        "Owner": "Windler-Friesen",
        "AppraisedValue": 153573,
    },
    {
        "VIN": "3VW8S7AT6FM437969",
        "Make": "Audi",
        "Model": "A4",
        "Year": 2001,
        "Owner": "Marquardt Inc",
        "AppraisedValue": 384953,
    },
    {
        "VIN": "5N1AR2MMXEC941296",
        "Make": "Ford",
        "Model": "Escort",
        "Year": 1985,
        "Owner": "Pfannerstill, Rowe and Roob",
        "AppraisedValue": 220131,
    },
    {
        "VIN": "WVWED7AJ2BW059402",
        "Make": "BMW",
        "Model": "5 Series",
        "Year": 2001,
        "Owner": "Erdman-Kohler",
        "AppraisedValue": 434162,
    },
    {
        "VIN": "JM3ER2A50B0876210",
        "Make": "Ford",
        "Model": "Explorer",
        "Year": 1991,
        "Owner": "Beatty and Sons",
        "AppraisedValue": 392457,
    },
    {
        "VIN": "2C4RDGCG9ER602809",
        "Make": "Volkswagen",
        "Model": "Jetta",
        "Year": 2003,
        "Owner": "DuBuque and Sons",
        "AppraisedValue": 396879,
    },
    {
        "VIN": "WBSWL9C51AP235294",
        "Make": "Toyota",
        "Model": "Camry",
        "Year": 1994,
        "Owner": "Hilpert Inc",
        "AppraisedValue": 451119,
    },
    {
        "VIN": "KM8NU4CC7AU670965",
        "Make": "Buick",
        "Model": "Century",
        "Year": 2003,
        "Owner": "Kunde, Bahringer and Kassulke",
        "AppraisedValue": 192005,
    },
    {
        "VIN": "3FADP0L39CR086146",
        "Make": "Chevrolet",
        "Model": "Cavalier",
        "Year": 2000,
        "Owner": "Jenkins, Wiza and Glover",
        "AppraisedValue": 206718,
    },
    {
        "VIN": "WBANE73516C578636",
        "Make": "Ford",
        "Model": "E250",
        "Year": 2005,
        "Owner": "Schiller-Hamill",
        "AppraisedValue": 40413,
    },
    {
        "VIN": "WAUBFAFL8DA892414",
        "Make": "Jeep",
        "Model": "Liberty",
        "Year": 2005,
        "Owner": "D'Amore, Donnelly and Hegmann",
        "AppraisedValue": 184448,
    },
    {
        "VIN": "1D4PU5GK7AW501122",
        "Make": "Toyota",
        "Model": "Land Cruiser",
        "Year": 2000,
        "Owner": "Torphy and Sons",
        "AppraisedValue": 407921,
    },
    {
        "VIN": "1GD12ZCG8CF213416",
        "Make": "Nissan",
        "Model": "Altima",
        "Year": 1993,
        "Owner": "Fay-Gislason",
        "AppraisedValue": 149168,
    },
    {
        "VIN": "1FTSX2B57AE918760",
        "Make": "Eagle",
        "Model": "Talon",
        "Year": 1998,
        "Owner": "Marquardt Group",
        "AppraisedValue": 135895,
    },
]

parts_example = [
    {
        "SupplierID": "supplier123",
        "ProductID": uuid4(),
        "LogisticsProviderID": "logistics123",
        "PartName": "Brake Pad",
        "PartQuantity": 100,
        "RequiredArrivalDate": datetime.utcnow() + timedelta(days=10),
        "ShipmentMethods": "Air",
        "ShipmentDate": datetime.utcnow() + timedelta(days=5),
        "PartLocation": "Melbourne",
    },
    {
        "SupplierID": "supplier456",
        "ProductID": uuid4(),
        "LogisticsProviderID": "logistics123",
        "PartName": "Oil Filter",
        "PartQuantity": 200,
        "RequiredArrivalDate": datetime.utcnow() + timedelta(days=15),
        "ShipmentMethods": "Ground",
        "ShipmentDate": datetime.utcnow() + timedelta(days=7),
        "PartLocation": "Sydney",
    },
    {
        "SupplierID": "supplier789",
        "ProductID": uuid4(),
        "LogisticsProviderID": "logistics123",
        "PartName": "Spark Plug",
        "PartQuantity": 300,
        "RequiredArrivalDate": datetime.utcnow() + timedelta(days=20),
        "ShipmentMethods": "Air",
        "ShipmentDate": datetime.utcnow() + timedelta(days=3),
        "PartLocation": "Wellington",
    },
    {
        "SupplierID": "supplier123",
        "ProductID": uuid4(),
        "LogisticsProviderID": "logistics123",
        "PartName": "Brake Pad",
        "PartQuantity": 100,
        "RequiredArrivalDate": datetime.utcnow() + timedelta(days=10),
        "ShipmentMethods": "Air",
        "ShipmentDate": datetime.utcnow() + timedelta(days=5),
        "PartLocation": "Auckland",  # Should be provider's warehouse location
    },
]


def main():
    for asset in assets_examples:
        if asset.get("Accident") is None:
            asset["Accident"] = randrange(0, 4)
        x = requests.post("http://localhost:8000/assets/", json=asset)
        print(x.text)

    for part in parts_example:
        part = json.loads(json.dumps(part, default=str))
        x = requests.post("http://localhost:8000/parts/", json=part)
        print(x.text)


if __name__ == "__main__":
    main()
