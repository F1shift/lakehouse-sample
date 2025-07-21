

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
        Action = [
          "s3:ListBucket",
        ]
        Effect   = "Allow"
        Resource = "arn:aws:s3:::${var.locals_env.sagemaker_unified_studio.default_glue_s3_bucket}"
      },
      {
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:DeleteObject",
          "s3:PutObjectAcl"
        ]
        Effect   = "Allow"
        Resource = "arn:aws:s3:::${var.locals_env.sagemaker_unified_studio.default_glue_s3_bucket}/*"
      },
      {
        Action = [
          "logs:CreateLogGroup",
        ]
        Effect   = "Allow"
        Resource = "arn:aws:logs:*:${data.aws_caller_identity.current.account_id}:log-group:*"
      },
      {
        Action = [
          "logs:CreateLogStream",
          "logs:PutLogEvents",
        ]
        Effect   = "Allow"
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

resource "aws_lakeformation_permissions" "traffic_data_table_permissions" {
  principal   = aws_iam_role.firehose_role.arn
  permissions = ["SELECT", "INSERT", "DELETE", "DESCRIBE"]

  table {
    database_name = aws_glue_catalog_table.traffic_data.database_name
    name          = aws_glue_catalog_table.traffic_data.name
  }
}

resource "aws_kinesis_firehose_delivery_stream" "test_stream" {
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