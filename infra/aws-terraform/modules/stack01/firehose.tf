

resource "aws_iam_role" "firehose_role" {
  name = "${var.locals_env.resource_prefix}-role-firehose"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "firehose.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_policy" "firehose_policy" {
  name = "${var.locals_env.resource_prefix}-policy-firehose"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "glue:GetDatabase",
          "glue:GetPartitions",
          "glue:GetTable",
          "glue:UpdateTable",
          "glue:CreateTable"
        ],
        Resource = [
          "arn:aws:glue:*:${data.aws_caller_identity.current.account_id}:catalog",
          "arn:aws:glue:*:${data.aws_caller_identity.current.account_id}:catalog/*",
          "arn:aws:glue:*:${data.aws_caller_identity.current.account_id}:database/${var.locals_env.sagemaker_unified_studio.default_glue_database}/*",
          aws_glue_catalog_table.traffic_data.arn,
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "s3:AbortMultipartUpload",
          "s3:DeleteObject",
          "s3:GetBucketLocation",
          "s3:GetObject",
          "s3:ListBucket",
          "s3:ListBucketMultipartUploads",
          "s3:PutObject",
          "s3:PutObjectAcl"
        ]
        Resource = [
          "arn:aws:s3:::${var.locals_env.sagemaker_unified_studio.default_glue_s3_bucket}",
          "arn:aws:s3:::${var.locals_env.sagemaker_unified_studio.default_glue_s3_bucket}/*",
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
        ]
        Resource = "arn:aws:logs:*:${data.aws_caller_identity.current.account_id}:log-group:*"
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogStream",
          "logs:PutLogEvents",
        ]
        Resource = "arn:aws:logs:*:${data.aws_caller_identity.current.account_id}:log-group:*:log-stream:*"
      },
      {
        Sid    = "RequiredWhenDoingMetadataReadsANDDataAndMetadataWriteViaLakeformation",
        Effect = "Allow",
        Action = [
          "lakeformation:GetDataAccess"
        ],
        Resource = "*"
      },
    ]
  })
}

resource "aws_iam_policy_attachment" "firehost_policy_attachment" {
  name       = "firehost_policy_attachment"
  roles      = [aws_iam_role.firehose_role.name]
  policy_arn = aws_iam_policy.firehose_policy.arn
}

resource "aws_iam_policy_attachment" "debug_policy_attachment" {
  name       = "debug_policy_attachment"
  roles      = [aws_iam_role.firehose_role.name]
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
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

resource "aws_cloudwatch_log_group" "firehose_log_group" {
  name              = "${var.locals_env.resource_prefix}/firehose/"
  retention_in_days = 7
}

locals {
  firehose_name = "${var.locals_env.resource_prefix}-firehose"
}

resource "aws_cloudwatch_log_stream" "firehose_log_stream" {
  log_group_name = aws_cloudwatch_log_group.firehose_log_group.name
  name           = local.firehose_name
}

resource "aws_kinesis_firehose_delivery_stream" "firehose1" {
  depends_on = [
    aws_glue_catalog_table.traffic_data,
    aws_lakeformation_permissions.database_permissions,
    aws_lakeformation_permissions.traffic_data_table_permissions,
  ]
  name        = local.firehose_name
  destination = "iceberg"


  iceberg_configuration {
    role_arn           = aws_iam_role.firehose_role.arn
    catalog_arn        = "arn:aws:glue:${var.locals_cmn.region}:${data.aws_caller_identity.current.account_id}:catalog"
    buffering_size     = 128
    buffering_interval = 60

    s3_configuration {
      role_arn   = aws_iam_role.firehose_role.arn
      bucket_arn = "arn:aws:s3:::${var.locals_env.sagemaker_unified_studio.default_glue_s3_bucket}"
    }

    destination_table_configuration {
      database_name          = var.locals_env.sagemaker_unified_studio.default_glue_database
      table_name             = aws_glue_catalog_table.traffic_data.name
      s3_error_output_prefix = "${var.locals_env.sagemaker_unified_studio.default_glue_data_path}/traffic_data/firehose_error"
    }

    cloudwatch_logging_options {
      enabled         = true
      log_group_name  = aws_cloudwatch_log_group.firehose_log_group.name
      log_stream_name = aws_cloudwatch_log_stream.firehose_log_stream.name
    }
  }
}