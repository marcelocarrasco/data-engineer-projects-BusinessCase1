# data-engineer-projects-BusinessCase1
Global Data Optimization for a Multi-Category E-Commerce Retailer
# GlobalMart Automated ETL Pipeline & Executive Dashboard

## 🚀 Tech Stack
![Python](https://shields.io)
![SQL](https://shields.io)
![Pandas](https://shields.io)
![Google Cloud](https://shields.io)
![Power Bi](https://shields.io)

---

## 1. Company Context
**GlobalMart** is an international e-commerce platform with physical and digital branch operations across multiple countries in Latin America and Europe. The store sells a diverse catalog of consumer goods categorized into three main business lines:

* **Sports & Fitness**
* **Kitchenware**
* **Home & Bedding** (*Línea Blanca*)

> 💡 **Operational Note:** Due to local fiscal and tax regulations, each country operates its local digital infrastructure semi-autonomously.

---

## 2. Problem Statement
Currently, each country’s transactional system generates sales reports in a decentralized, isolated manner. At the end of every business day, each regional branch exports its transactions into unconsolidated flat files (a mix of CSV and JSON formats) stored on local servers or sent via email.

This fragmented model has created several critical business bottlenecks:

* 🚨 **Lack of Daily Visibility:** Executive managers do not know how much they sell daily. Consolidating global data manually takes between 7 and 10 days, completely blocking agile decision-making regarding inventory control, stock replenishment, and marketing promotions.
* 💱 **Heterogeneous Formats and Currencies:** The same kitchen product might be registered under different local currencies (Euros, Mexican Pesos, US Dollars), varying time zones, and slight structural discrepancies in the file schemas.
* ❌ **No Single Source of Truth:** Data is heavily duplicated, siloed, and highly prone to manual transcription errors during manual copy-pasting.

---

## 3. Technical Requirement: ETL Pipeline
To resolve this issue at its root, the engineering team needs to design and implement an automated, daily **ETL Pipeline** to centralize and homogenize the transactional data using **Python, SQL, and Cloud Architecture**.


### 📥 Extraction (Python + Cloud)
A scheduled Python script that automatically connects to local regional servers daily, fetches the raw, loose flat files (CSV/JSON), and uploads them to a central Cloud Landing Zone (e.g., **AWS S3**, **Google Cloud Storage**, or **Azure Blob Storage**).

### ⚙️ Transformation (Python)
Data cleaning and normalization utilizing libraries such as **Pandas** or **PySpark**. This phase must:
* Standardize dates into **UTC**.
* Handle currency conversion into a unified base currency (e.g., **USD**) using daily exchange rates.
* Map local product naming variations into unified global categories.

### 💾 Loading (SQL + Cloud)
Insert the cleaned, structured data into a cloud Data Warehouse (e.g., **Snowflake**, **Google BigQuery**, or **AWS Redshift**). **SQL** will be used to structure the analytical layers into optimized **Fact Tables** (sales metrics) and **Dimension Tables** (countries, products, time) ready for high-performance querying.

---

## 📂 Project Structure
Below is the directory layout for the codebase:

```text
globalmart-etl/
├── config/                 # Database and Cloud credentials configuration
│   └── settings.py
├── dwh_sql/                # SQL scripts for staging and analytical layers
│   ├── dimensions/
│   └── facts/
├── src/                    # Primary ETL Python codebase
│   ├── __init__.py
│   ├── extraction.py       # Pulls local CSV/JSON files to landing zone
│   ├── transformation.py   # Cleans, currency converts, and normalizes data
│   └── loading.py          # Populates Data Warehouse Fact/Dim tables
├── main.py                 # Core orchestration script execution entry point
├── requirements.txt         # Project software dependencies
└── README.md
```

---

## 🛠️ Prerequisites & Installation

### Prerequisites
Before running this project, ensure you have the following installed:
* Python 3.9 or higher
* Access keys for your Cloud provider (AWS/GCP/Azure)
* Connection credentials to your Data Warehouse

### Installation
1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com
   cd globalmart-etl
   ```

2. Create and activate a virtual environment:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required Python packages:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Configure your environment variables inside `config/settings.py` and run the core pipeline:
   ```bash
   python main.py
   ```

---

## 4. Business Intelligence Requirement: Interactive Dashboard
Once the clean data is centralized in the cloud Data Warehouse, the analytics team requires a connection to a Business Intelligence tool (such as **Power BI**, **Tableau**, or **Looker Studio**) to build an Executive Dashboard.

This interactive visual interface must answer the following operational questions instantly:

- [ ] What is the total global revenue generated today compared to yesterday?
- [ ] Which country or branch is currently leading sales in the **Home & Bedding** category?
- [ ] What are the top 5 best-selling products across all regions this week?
- [ ] What is the real profit margin per country after standardized currency conversion?

