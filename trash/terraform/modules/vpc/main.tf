terraform {
    required_providers {
        aws = {
            source  = "hashicorp/aws"
        }
    }
}

resource "aws_vpc" "vpc" {
  cidr_block = var.vpc.CIDR
  tags = {
    Name = var.vpc.NAME
  }
}

resource "aws_subnet" "subnets" {
    count = length(var.subnets)
    vpc_id     = aws_vpc.vpc.id
    cidr_block = var.subnets[count.index].CIDR
    availability_zone = var.availability_zones[var.subnets[count.index].AZ_ORDER]

    tags = {
        Name = var.subnets[count.index].NAME
    }
}