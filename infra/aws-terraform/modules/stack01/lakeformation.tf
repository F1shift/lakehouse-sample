resource "aws_lakeformation_permissions" "iam_allowed_principals_database_permissions" {
  principal   = "IAM_ALLOWED_PRINCIPALS"
  permissions = ["ALL"]

  database {
    name       = aws_glue_catalog_table.traffic_data.database_name
    catalog_id = data.aws_caller_identity.current.account_id
  }
}

resource "aws_lakeformation_permissions" "iam_allowed_principals_table_permissions" {
  principal   = "IAM_ALLOWED_PRINCIPALS"
  permissions = ["ALL"]

  table {
    database_name = aws_glue_catalog_table.traffic_data.database_name
    name          = aws_glue_catalog_table.traffic_data.name
  }
}

# 既存のLake Formation設定を読み込む
data "aws_lakeformation_data_lake_settings" "existing" {}

# 既存の管理者にFirehoseロールを追加して、新しい管理者リストを作成
resource "aws_lakeformation_data_lake_settings" "this" {
  admins = toset(concat(
    tolist(data.aws_lakeformation_data_lake_settings.existing.admins),
    [aws_iam_role.firehose_role.arn]
  ))
}

resource "aws_lakeformation_permissions" "database_permissions" {
  principal   = aws_iam_role.firehose_role.arn
  permissions = ["ALL"]

  database {
    name       = aws_glue_catalog_table.traffic_data.database_name
    catalog_id = data.aws_caller_identity.current.account_id
  }
}

resource "aws_lakeformation_permissions" "traffic_data_table_permissions" {
  principal   = aws_iam_role.firehose_role.arn
  permissions = ["SELECT", "INSERT", "DELETE", "DESCRIBE"]

  table {
    database_name = aws_glue_catalog_table.traffic_data.database_name
    # name          = aws_glue_catalog_table.traffic_data.name
    wildcard = true
  }
}

resource "aws_lakeformation_permissions" "traffic_data_table_columns_permissions" {
  principal   = aws_iam_role.firehose_role.arn
  permissions = ["SELECT"]

  table_with_columns {
    database_name = aws_glue_catalog_table.traffic_data.database_name
    name          = aws_glue_catalog_table.traffic_data.name
    column_names  = ["id", "timestamp", "age", "gender", "direction"]
  }
}

resource "aws_lakeformation_resource" "s3" {
  arn = "arn:aws:s3:::${var.locals_env.sagemaker_unified_studio.default_glue_s3_bucket}"
}

resource "aws_lakeformation_permissions" "firehose_data_location_permissions" {
  principal   = aws_iam_role.firehose_role.arn
  permissions = ["DATA_LOCATION_ACCESS"]
  data_location {
    arn = aws_lakeformation_resource.s3.arn
  }
}