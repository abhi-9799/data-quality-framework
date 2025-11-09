from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine

def load_sqlite(db_path="dq_local.db"):
    engine = create_engine(f"sqlite:///{db_path}")
    data_dir = Path(__file__).parent.parent / "sample_data"

    for csv_file in data_dir.glob("*.csv"):
        table_name = csv_file.stem  # e.g., "orders" -> table "orders"
        df = pd.read_csv(csv_file)
        df.to_sql(table_name, con=engine, if_exists="replace", index=False)
    return engine

if __name__ == "__main__":
    load_sqlite()
    print("Loaded all CSVs in sample_data/ into dq_local.db")
