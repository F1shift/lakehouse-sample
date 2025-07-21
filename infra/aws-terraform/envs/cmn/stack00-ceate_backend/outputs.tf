output "outputs" {
  value = {
    terraform_bucket = aws_s3_bucket.terraform_state
  }
}