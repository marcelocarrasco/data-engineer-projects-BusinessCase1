import os
import pandas as pd
from google.cloud import bigquery

def load_data_to_bigquery(df: pd.DataFrame):
    """Splits transformed flat data and loads it into BigQuery Dimension and Fact Tables."""
    print("\n--- 💾 STARTING LOADING PHASE ---")
    
    if df is None or df.empty:
        print("⚠️ No data available to load. Aborting phase.")
        return

    project_id = os.getenv("GCP_PROJECT_ID")
    dataset_id = "globalmart_dwh"
    
    # 1. Isolate and Load Product Dimension Elements
    print("📦 Extracting and updating Product Dimension records...")
    dim_products = df[['product_id', 'product_name', 'global_category']].drop_duplicates()
    
    # 2. Isolate and Load Core Fact Table Data Metrics
    print("📊 Extracting and routing Sales Fact transaction metrics...")
    fact_sales = df[[
        'transaction_id', 'transaction_timestamp', 'branch_id', 
        'product_id', 'units_sold', 'local_amount', 
        'usd_amount', 'exchange_rate_used'
    ]]

    # Configuration for BigQuery API append requests
    client = bigquery.Client(project=project_id)
    
    # Mapping staging items into target destination strings
    tables_to_load = {
        f"{project_id}.{dataset_id}.dim_products": dim_products,
        f"{project_id}.{dataset_id}.fact_sales": fact_sales
    }
    
    for table_ref, table_df in tables_to_load.items():
        print(f"📤 Appending {len(table_df)} rows to target table: {table_ref}...")
        
        job_config = bigquery.LoadJobConfig(
            write_disposition="WRITE_APPEND"  # Keeps historical logs intact daily
        )
        
        # Batch upload DataFrame using pyarrow high-efficiency pipeline conversion
        job = client.load_table_from_dataframe(table_df, table_ref, job_config=job_config)
        job.result()  # Blocks evaluation execution and waits for completion
        
    print("✅ BigQuery Data Warehouse load complete.")

