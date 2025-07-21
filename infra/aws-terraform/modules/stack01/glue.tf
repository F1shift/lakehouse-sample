resource "aws_glue_catalog_table" "traffic_data" {
  name          = "${var.locals_env.table_prefix}_traffic_data"
  database_name = var.locals_env.sagemaker_unified_studio.default_glue_database

  table_type = "EXTERNAL_TABLE"

  parameters = {
    EXTERNAL              = "TRUE"
    "parquet.compression" = "SNAPPY"
  }

  storage_descriptor {
    location      = "s3://${var.locals_env.sagemaker_unified_studio.default_glue_s3_bucket}/${var.locals_env.sagemaker_unified_studio.default_glue_data_path}/traffic_data"
    input_format  = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat"

    ser_de_info {
      name                  = "traffic_data"
      serialization_library = "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"

      parameters = {
        "serialization.format" = 1
      }
    }

    columns {
      name = "id"
      type = "string"
    }

    columns {
      name = "timestamp"
      type = "timestamp"
    }

    columns {
      name    = "age"
      type    = "int"
      comment = "just age"
    }

    columns {
      name    = "gender"
      type    = "string"
      comment = "male or female"
    }

    columns {
      name    = "direction"
      type    = "int"
      comment = "entry is 1, exit is -1."
    }
  }
}