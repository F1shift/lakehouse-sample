terraform {
  backend "s3" {
    bucket = "mylakehouse-cmn-terraform-state"
    region = "ap-northeast-1"
    key    = "dev/stack02.tfstate"
  }
}