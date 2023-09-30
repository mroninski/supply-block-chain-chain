import duckdb
from typing import List, Any, Optional


class DB:
    def __init__(self) -> None:
        self.database_file = "quack.duckdb"
        self.__init_connection()

    def __init_connection(self) -> None:
        self.cursor = duckdb.connect(database=self.database_file, read_only=False)

    def query(self, sql: str, query_args: Optional[List[Any]] = None) -> List[Any]:
        self.cursor.execute(sql, query_args)
        return self.cursor.fetchall()

    def save(self) -> None:
        self.cursor.commit()


db_obj = DB()
