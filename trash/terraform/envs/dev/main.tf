terraform {
  backend "s3" {
    bucket = "f1shift-terraform-state"
    key = "lakehouse-sample-dev.tfstate"
    region = "ap-northeast-1"
  }
}

provider "aws" {
  region = local.MAIN_REGION
}