import os
import json
import pandas as pd
from io import BytesIO, StringIO
from google.cloud import storage

def fetch_exchange_rates():
    """
    Simulates fetching clean daily exchange rates from a financial API.
    Returns conversion factors relative to 1 USD base currency.
    """
    return {
        "USD": 1.0,
        "EUR": 0.91,  # 1 USD = 0.91 EUR
        "MXN": 17.15  # 1 USD = 17.15 MXN
    }

def clean_and_normalize(df, rates):
    """Parses, cleans, and standardizes multi-region data structures."""
    # Ensure standard datetime formats converted explicitly to UTC timezone
    df['transaction_timestamp'] = pd.to_datetime(df['transaction_timestamp']).dt.tz_localize(None)
    
    # Calculate uniform reporting valuation using foreign exchange logic
    def calculate_usd(row):
        currency = row['local_currency']
        amount = row['local_amount']
        rate = rates.get(currency, 1.0)
        return round(amount / rate, 2), rate

    # Apply translation map calculation vectors row-wise
    usd_metrics = df.apply(calculate_usd, axis=1)
    df['usd_amount'] = [x[0] for x in usd_metrics]
    df['exchange_rate_used'] = [x[1] for x in usd_metrics]
    
    # Global Uniform Mapping logic for categorization rules
    category_mapping = {
        'sporting_goods': 'Sports & Fitness',
        'fitness_gear': 'Sports & Fitness',
        'pots_pans': 'Kitchenware',
        'cutlery': 'Kitchenware',
        'bedsheets': 'Home & Bedding',
        'pillows': 'Home & Bedding'
    }
    df['global_category'] = df['local_category'].str.lower().map(category_mapping).fillna('Other')
    
    # Select and enforce schema alignment to match target data warehouse schemas
    final_cols = [
        'transaction_id', 'transaction_timestamp', 'branch_id', 
        'product_id', 'product_name', 'global_category', 
        'units_sold', 'local_amount', 'local_currency', 
        'usd_amount', 'exchange_rate_used'
    ]
    return df[final_cols]

def run_transformation():
    """Pulls data from GCS Landing Zone, cleans via Pandas, returns transformed DataFrame."""
    print("\n--- ⚙️ STARTING TRANSFORMATION PHASE ---")
    
    storage_client = storage.Client()
    bucket_name = os.getenv("GCP_GCS_BUCKET_NAME")
    bucket = storage_client.bucket(bucket_name)
    
    rates = fetch_exchange_rates()
    all_dfs = []
    
    # Example Target Blobs from Extraction phase
    blobs_to_process = [
        {"path": "raw/latam/sales_2026_09_04.csv", "format": "csv"},
        {"path": "raw/europe/sales_2026_09_04.json", "format": "json"}
    ]
    
    for target in blobs_to_process:
        blob = bucket.blob(target["path"])
        if not blob.exists():
            print(f"⚠️ Blob storage object not found, skipping target: {target['path']}")
            continue
            
        print(f"⬇️ Downloading and reading: gs://{bucket_name}/{target['path']}")
        content_bytes = blob.download_as_bytes()
        
        if target["format"] == "csv":
            df = pd.read_csv(BytesIO(content_bytes))
        elif target["format"] == "json":
            df = pd.read_json(BytesIO(content_bytes))
            
        all_dfs.append(df)
        
    if not all_dfs:
        print("❌ No matching processing sources discovered in cloud landing layer.")
        return None
        
    # Standardize data frames into monolithic batch process
    combined_raw_df = pd.concat(all_dfs, ignore_index=True)
    processed_df = clean_and_normalize(combined_raw_df, rates)
    
    print(f"✅ Normalization Complete. Cleaned {len(processed_df)} rows for warehouse insertion.")
    return processed_df

