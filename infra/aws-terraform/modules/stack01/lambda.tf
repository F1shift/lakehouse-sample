# IAM role for Lambda execution
data "aws_iam_policy_document" "assume_role_policy" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "lambda_role" {
  name               = "lambda_execution_role"
  assume_role_policy = data.aws_iam_policy_document.assume_role_policy.json
}

# Package the Lambda function code
data "archive_file" "src" {
  type        = "zip"
  source_file = "${path.module}/lambda/dummy_data_generator/src"
  output_path = "${path.module}/lambda/dummy_data_generator/src.zip"
}

# Lambda function
resource "aws_lambda_function" "example" {
  filename         = data.archive_file.src.output_path
  function_name    = "${var.locals_env.resource_prefix}-lambda-dummy-data-generator}"
  role             = aws_iam_role.lambda_role.arn
  handler          = "lambda_function.lambda_handler"
  source_code_hash = data.archive_file.src.output_base64sha256

  runtime = "python3.12"

  environment {
    variables = {
      DELIVERY_STREAM_NAME = aws_kinesis_firehose_delivery_stream.firehose1.name
      S3_BUCKET            = var.locals_env.sagemaker_unified_studio.default_glue_s3_bucket

    }
  }

  tags = {
    Name = "${var.locals_env.resource_prefix}-lambda-dummy-data-generator}"
  }
}