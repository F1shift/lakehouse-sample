data "aws_availability_zones" "main_region_availability_zones" {
  state = "available"
}


module "main_vpc" {
  source             = "../../modules/vpc"
  vpc                = local.MAIN.VPC
  subnets            = local.MAIN.SUBNETS
  availability_zones = data.aws_availability_zones.main_region_availability_zones.names
}