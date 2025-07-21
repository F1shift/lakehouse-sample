CREATE TABLE "awsdatacatalog"."lakehouse_sample_glue_db"."traffic_data_2" (
  human_id string,
  timestamp timestamp,
  direction boolean,
  guessed_age int,
  guessed_gender boolean) 
PARTITIONED BY (year(timestamp), month(timestamp), day(timestamp)) 
LOCATION 's3://lakehouse-sample-s3-bucket/lakehouse_sample_glue_db.db/traffic_data_2' 
TBLPROPERTIES (
  'table_type'='ICEBERG',
  'format'='parquet',
  'write_compression'='snappy',
  'optimize_rewrite_delete_file_threshold'='10'
)