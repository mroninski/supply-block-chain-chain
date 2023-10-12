from api.models import TransactionHistory
from api.database import db_obj

from datetime import datetime


def create_transaction_history(transaction_history: TransactionHistory):
    """
    Create a transaction history entry in the DuckDB database
    """

    response = db_obj.query(
        "INSERT INTO models.transaction_history VALUES (?, ?, ?)",
        query_args=[
            transaction_history.EndpointRequest,
            transaction_history.RequestTime,
            transaction_history.ResponseStatus,
        ],
    )

    print(response)

    db_obj.save()
    return
