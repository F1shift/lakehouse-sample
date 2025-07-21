resource "aws_s3_bucket" "terraform_state" {
  bucket = "${local.locals_cmn.resource_prefix}-terraform-state"

  tags = {
    Name = "${local.locals_cmn.resource_prefix}-terraform-state"
  }
}