import os
import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = os.environ["DATABASE_URL"]


def load_staging_tables():
    engine = create_engine(DATABASE_URL)
    processed_dir = "../data/processed"

    files_to_tables = {
        "orders_clean.csv": "stg_orders",
        "products_clean.csv": "stg_products",
        "customers_clean.csv": "stg_customers",
        "order_items_clean.csv": "stg_order_items",
        "order_payments_clean.csv": "stg_order_payments",
        "category_translation_clean.csv": "stg_category_translation",
        "order_reviews_clean.csv": "stg_order_reviews",
        "sellers_clean.csv": "stg_sellers",
        "geolocation_clean.csv": "stg_geolocation"
    }

    print("Starting data load from clean CSVs into PostgreSQL staging tables...\n")

    for csv_file, table_name in files_to_tables.items():
        file_path = os.path.join(processed_dir, csv_file)

        if os.path.exists(file_path):
            print(f"Loading {csv_file} -> table '{table_name}'...")

            df = pd.read_csv(file_path)

            df.to_sql(name=table_name, con=engine, if_exists="replace", index=False)

            print(f" Successfully loaded {len(df)} rows into '{table_name}'.\n")
        else:
            print(f" Error: File {csv_file} does not exist in {processed_dir}!\n")


load_staging_tables()
