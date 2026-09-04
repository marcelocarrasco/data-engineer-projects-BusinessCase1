import os
from google.cloud import storage

def upload_to_gcs(local_file_path, bucket_name, destination_blob_name):
    """ Uploads a local file to a Google Cloud Storage bucket."""
    print(f"🔄 Initializing GCS upload for {local_file_path}...")
    
    # Implicitly looks for GOOGLE_APPLICATION_CREDENTIALS environment variable
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(local_file_path)
    print(f"✅ Successfully uploaded {local_file_path} to gs://{bucket_name}/{destination_blob_name}")

def run_extraction():
    """Simulates grabbing daily regional branch files and uploading them to GCS."""
    print("\n--- 📥 STARTING EXTRACTION PHASE ---")
    
    bucket_name = os.getenv("GCP_GCS_BUCKET_NAME", "globalmart-landing-zone")
    
    # Example dictionary representing discovered files from local regional servers
    daily_files = {
        "data/raw/latam_sales_2026_09_04.csv": "raw/latam/sales_2026_09_04.csv",
        "data/raw/europe_sales_2026_09_04.json": "raw/europe/sales_2026_09_04.json"
    }
    
    for local_path, gcs_path in daily_files.items():
        if os.path.exists(local_path):
            upload_to_gcs(local_path, bucket_name, gcs_path)
        else:
            print(f"⚠️ Local file not found, skipping: {local_path}")
            
    print("🏁 Extraction phase complete.")

