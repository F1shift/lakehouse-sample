resource "aws_kinesis_firehose_delivery_stream" "example" {
    name        = "example-firehose"
    destination = "s3"

    s3_configuration {
        bucket_arn = aws_s3_bucket.example.arn
        role_arn   = aws_iam_role.firehose_role.arn

        buffering {
        interval = 300
        size     = 5
        }

        compression_format = "UNCOMPRESSED"
    }
}

resource "aws_s3_bucket" "example" {
    bucket = "example-bucket"
}

resource "aws_iam_role" "firehose_role" {
    name = "firehose_role"

    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
        {
            Action = "sts:AssumeRole"
            Principal = {
            Service = "firehose.amazonaws.com"
            }
            Effect = "Allow"
            Sid    = ""
        },
        ]
    })
}

resource "aws_iam_policy" "firehose_policy" {
    name        = "firehose_policy"
    description = "Policy for Firehose to access S3"

    policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
        {
            Effect = "Allow"
            Action = [
            "s3:PutObject",
            "s3:PutObjectAcl"
            ]
            Resource = "${aws_s3_bucket.example.arn}/*"
        },
        ]
    })
}

resource "aws_iam_role_policy_attachment" "firehose_policy_attachment" {
    policy_arn = aws_iam_policy.firehose_policy.arn
    role       = aws_iam_role.firehose_role.name
}