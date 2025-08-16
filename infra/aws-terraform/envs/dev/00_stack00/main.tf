terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.4"
    }
  }
  required_version = "~> 1.12.2"
}

# Configure the AWS Provider
provider "aws" {
  region = local.locals_cmn.region

  default_tags {
    tags = {
      project    = local.locals_cmn.project_name
      env        = local.locals_env.env
      created_by = "terraform"
    }
  }
}

module "stack00" {
  source     = "../../../modules/stack00"
  locals_cmn = local.locals_cmn
  locals_env = local.locals_env
}