output "vpc" {
    description = "VPC ID."
    value = aws_vpc.vpc
}

output "subnets" {
    description = "Subnets."
    value = aws_subnet.subnets
}