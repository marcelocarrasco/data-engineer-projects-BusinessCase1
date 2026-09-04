import os
from dotenv import load_dotenv

# Import our custom module tasks
from src.extraction import run_extraction
from src.transformation import run_transformation
from src.loading import load_data_to_bigquery

def main():
    print("==================================================")
    print("🚀 STARTING GLOBALMART AUTOMATED DAILY ETL PIPELINE")
    print("==================================================")
    
    # 0. Load Configuration & Safe Credentials Verification Check
    load_dotenv()
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        print("❌ CRITICAL ERROR: GOOGLE_APPLICATION_CREDENTIALS environment variable is missing.")
        print("Please check your .env file setup before re-running.")
        return

    # 1. Run Extraction Phase
    try:
        run_extraction()
    except Exception as e:
        print(f"❌ Extraction Pipeline Step Failed: {str(e)}")
        return

    # 2. Run Transformation Phase
    try:
        transformed_df = run_transformation()
    except Exception as e:
        print(f"❌ Transformation Pipeline Step Failed: {str(e)}")
        return

    # 3. Run Loading Phase
    try:
        if transformed_df is not None:
            load_data_to_bigquery(transformed_df)
        else:
            print("❌ Pipeline stalled: Data payload missing or corrupted during mapping.")
            return
    except Exception as e:
        print(f"❌ Loading Warehouse Phase Step Failed: {str(e)}")
        return
    
    print("\n==================================================")
    print("🎉 ETL PIPELINE EXECUTED SUCCESSFULLY WITHOUT ERRORS")
    print("==================================================")

if __name__ == "__main__":
    main()
