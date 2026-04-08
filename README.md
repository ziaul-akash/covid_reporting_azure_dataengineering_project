# covid_reporting_azure_dataengineering_project


Here's a full breakdown of every service used, organized by pipeline phase:

Data Sources
The project pulls from two sources: ECDC COVID-19 data fetched via an HTTP connector (a public REST endpoint), and Population Data stored in Azure Blob Storage. Blob Storage is Azure's object storage for unstructured data, used here as a landing zone for reference datasets.

Ingestion — Azure Data Factory (ADF)
ADF is the core orchestration engine. It runs the pipelines that pull data from both sources and land them into the data lake. I used ADF's built-in HTTP and Blob linked services to connect to the sources, then Copy Activities to move the raw data downstream.

Staging — Azure Data Lake Storage Gen2 (ADLS Gen2)
Raw ingested data lands in ADLS Gen2, which acts as the staging/raw layer. ADLS Gen2 combines the scalability of Azure Blob Storage with a hierarchical namespace optimized for big data analytics.

Transformation — Three tools working together

Azure Data Factory (ADF) — used again here for lighter, flow-based transformations via Mapping Data Flows and Copy Activities.
Azure Databricks (DBX) — Apache Spark-based platform for heavier, notebook-driven transformations (Python/PySpark). Ideal for complex aggregations and joins across large COVID datasets.
Azure HDInsight (HDI) — managed Hadoop/Hive cluster used for SQL-style transformations on the data lake files.


Serving Layer — Azure SQL Database
Transformed, clean data is written to Azure SQL Database, which acts as the relational serving layer — structured and query-ready for downstream consumption.

Publishing

Power BI — connects to Azure SQL Database to build interactive COVID reporting dashboards (case counts, trends, population ratios, etc.).
