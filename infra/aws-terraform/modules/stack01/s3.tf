
resource "aws_s3_bucket" "dummy_data_bucket" {
  bucket = "${var.locals_env.resource_prefix}-dummy-data"

  tags = {
    Name = "${var.locals_env.resource_prefix}-dummy-data"
  }
}

locals {
  dummy_data_dir = "${path.module}/../../../../dummy_data_source/demo_external_system/sample_data/03_split_data/output"
}

resource "aws_s3_object" "dummy_data_object" {
  for_each = { for i, f in fileset(local.dummy_data_dir, "*.csv") : i => f }
  bucket   = aws_s3_bucket.dummy_data_bucket.id
  #S3へアップロードするときのkey値
  key = "${var.locals_cmn.dummy_data_prefix}/${each.value}"
  #ファイルのローカルパス
  source       = "${local.dummy_data_dir}/${each.value}"
  content_type = "text/csv"
  etag         = filemd5("${local.dummy_data_dir}/${each.value}")
}