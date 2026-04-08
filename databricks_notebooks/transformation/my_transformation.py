# Databricks notebook source
from pyspark.sql.functions import split, regexp_replace, col

# COMMAND ----------

path = "/Volumes/covid_reporting_databricks_workspace_01/population_by_age/raw/population_by_age.tsv"
df_raw_population= spark.read.format("csv").options( header = True, delimiter = '\t', inferSchema= True ).load(path)

# COMMAND ----------

df_raw_population= df_raw_population.withColumn('age_group', regexp_replace(split(df_raw_population['indic_de,geo\\time'], ',')[0], 'PC_', ''))\
.withColumn('country_code_2_digit', split(df_raw_population['indic_de,geo\\time'], ',')[1])\
    
df_raw_population= df_raw_population.select(
                            col("country_code_2_digit"),
                            col("age_group"),
                            col("2019 ").alias('percentage_2019'))

df_raw_population.createOrReplaceTempView("raw_population")

# COMMAND ----------


df_raw_population_pivot = spark.sql("""
    SELECT 
        country_code_2_digit, 
        age_group, 
        cast(
            regexp_replace(
                regexp_replace(percentage_2019, ':', '0'),
            '[a-z]', '') 
        AS decimal(4,2)) AS percentage_2019 
    FROM raw_population 
    WHERE length(country_code_2_digit) = 2
""").groupBy('country_code_2_digit').pivot('age_group').sum('percentage_2019').orderBy('country_code_2_digit')

df_raw_population_pivot.createOrReplaceTempView("raw_population_pivot")

# COMMAND ----------

df_country=spark.read.format('csv').option('header' , True).load("/Volumes/covid_reporting_databricks_workspace_01/population_by_age/lookup/country_lookup.csv")
df_country.createOrReplaceTempView("lookup_country")

# COMMAND ----------

df_processed_population= spark.sql("""
                                   SELECT 
                                   t.country, 
                                   t.country_code_2_digit,
                                   t.country_code_3_digit,
                                   t.population,
                                   s.Y0_14, s.Y15_24,s.Y25_49, s.Y50_64, s.Y65_79, s.Y80_MAX
                                   FROM raw_population_pivot s
                                   JOIN lookup_country t
                                   ON s.country_code_2_digit = t.country_code_2_digit
                                   ORDER BY t.country
                                   """)

# COMMAND ----------

df_processed_population.display()

# COMMAND ----------

df_processed_population.write.format('csv').option('header', True).option('delimiter', ',').mode('overwrite').save('/Volumes/covid_reporting_databricks_workspace_01/population_by_age/processed/population_by_age_processed')