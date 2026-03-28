# Databricks notebook source
dbutils.widgets.removeAll()

# COMMAND ----------

dbutils.widgets.text('src_base_dir', '', label='Enter Source Base Dir')
dbutils.widgets.text('bronze_base_dir', '', label='Enter Target Base Dir')
dbutils.widgets.text('ds', '', label='Enter Dataset Name')

# COMMAND ----------

src_base_dir = dbutils.widgets.get('src_base_dir')

# COMMAND ----------

bronze_base_dir = dbutils.widgets.get('bronze_base_dir')

# COMMAND ----------

ds = dbutils.widgets.get('ds')

# COMMAND ----------

import json

def get_columns(schemas_file, ds_name):
    schema_text = spark.read.text(schemas_file, wholetext=True).first().value
    schemas = json.loads(schema_text)
    column_details = schemas[ds_name]
    columns = [col['column_name'] for col in sorted(column_details, key=lambda col: col['column_position'])]
    return columns

# COMMAND ----------

ds

# COMMAND ----------

print(f'Processing {ds} data')
columns = get_columns(f'dbfs:{src_base_dir}/schemas.json', ds)
df = spark. \
    read. \
    csv(f'{src_base_dir}/{ds}', inferSchema=True). \
    toDF(*columns)

# COMMAND ----------

df.show()

# COMMAND ----------

df.write. \
    mode('overwrite'). \
    parquet(f'{bronze_base_dir}/{ds}')

# COMMAND ----------


