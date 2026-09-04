-- Create the main dataset if it doesn't exist
CREATE SCHEMA IF NOT EXISTS globalmart_dwh;

-- 1. Dimension Table: Countries / Branches
CREATE OR REPLACE TABLE globalmart_dwh.dim_branches (
  branch_id STRING OPTIONS(description="Unique ID for each branch"),
  country STRING,
  region STRING,
  local_currency STRING
);

-- 2. Dimension Table: Products
CREATE OR REPLACE TABLE globalmart_dwh.dim_products (
  product_id STRING OPTIONS(description="Global unified product ID"),
  product_name STRING,
  global_category STRING OPTIONS(description="Mapped to Sports & Fitness, Kitchenware, or Home & Bedding")
);

-- 3. Fact Table: Core Sales Metrics
CREATE OR REPLACE TABLE globalmart_dwh.fact_sales (
  transaction_id STRING,
  transaction_timestamp TIMESTAMP,
  branch_id STRING,
  product_id STRING,
  units_sold INT64,
  local_amount NUMERIC,
  usd_amount NUMERIC OPTIONS(description="Standardized target currency for executive reporting"),
  exchange_rate_used NUMERIC
)
PARTITION BY DATE(transaction_timestamp)
CLUSTER BY branch_id, product_id;
