
resource "aws_s3_bucket" "dummy_data_bucket" {
  bucket = "${local.locals_cmn.resource_prefix}-dummy-data"

  tags = {
    Name = "${local.locals_cmn.resource_prefix}-dummy-data"
  }
}

resource "aws_s3_object" "dummy_data_object" {
  for_each = { for i, f in fileset("${path.module}../../../../dummy_data_source/demo_external_system/sample_data/03_split_data/output", "*.csv") : i => f }
  bucket   = aws_s3_bucket.s3.id
  #S3へアップロードするときのkey値
  key = each.value
  #ファイルのローカルパス
  source       = each.value
  content_type = "text/csv"
  etag         = filemd5(each.value)
}