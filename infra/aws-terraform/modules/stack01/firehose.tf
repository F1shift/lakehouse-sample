

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
          "arn:aws:glue:*:${data.aws_caller_identity.current.account_id}:database/${var.locals_env.sagemaker_unified_studio.default_glue_database}*",
          # "arn:aws:glue:*:${data.aws_caller_identity.current.account_id}:catalog/${var.locals_env.sagemaker_unified_studio.default_glue_database}*",
          aws_glue_catalog_table.traffic_data.arn,
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "s3:ListBucket",
        ]
        Resource = "arn:aws:s3:::${var.locals_env.sagemaker_unified_studio.default_glue_s3_bucket}"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:DeleteObject",
          "s3:PutObjectAcl"
        ]
        Resource = "arn:aws:s3:::${var.locals_env.sagemaker_unified_studio.default_glue_s3_bucket}/*"
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
    ]
  })
}

resource "aws_iam_policy_attachment" "firehost_policy_attachment" {
  name       = "firehost_policy_attachment"
  roles      = [aws_iam_role.firehose_role.name]
  policy_arn = aws_iam_policy.firehose_policy.arn
}

resource "aws_lakeformation_permissions" "database_permissions" {
  principal   = aws_iam_role.firehose_role.arn
  permissions = ["DESCRIBE"]

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
    name          = aws_glue_catalog_table.traffic_data.name
  }
}

resource "aws_kinesis_firehose_delivery_stream" "firehose1" {
  depends_on = [
    aws_glue_catalog_table.traffic_data,
    aws_lakeformation_permissions.database_permissions,
    aws_lakeformation_permissions.traffic_data_table_permissions,
  ]
  name        = "${var.locals_env.resource_prefix}-firehose"
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
      database_name = var.locals_env.sagemaker_unified_studio.default_glue_database
      table_name    = aws_glue_catalog_table.traffic_data.name
    }
  }
}