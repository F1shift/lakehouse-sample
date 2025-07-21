terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.4"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = local.locals_cmn.region

  default_tags {
    tags = {
      project    = local.locals_cmn.project_name
      created_by = "terraform"
      env        = local.locals_cmn.env
    }
  }
}