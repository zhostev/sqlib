import os
import duckdb

class DuckDBManager:
    def __init__(self, db_folder, db_name):
        self.db_name = db_name
        self.db_folder = db_folder
        self.con = None
        self.db_path = os.path.join(self.db_folder, self.db_name)

    def __enter__(self):
        self.con = duckdb.connect(self.db_path)
        return self.con

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()

def save_to_db(db_folder, db_name, table_name, data):
    with DuckDBManager(db_folder, db_name) as con:
        con.execute(f"DROP TABLE IF EXISTS {table_name}")
        con.sql(f"CREATE TABLE {table_name} AS SELECT * FROM data")
        con.sql(f"SELECT * FROM {table_name}").show()
