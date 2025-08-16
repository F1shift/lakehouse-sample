# resource "aws_eip" "nat_eip" {

# }

# resource "aws_nat_gateway" "nat" {
#   allocation_id = aws_eip.nat_eip.id
#   subnet_id     = var.locals_env.sagemaker_unified_studio.network.ngw_subnet
# }

resource "aws_route_table" "private_subnet_route_table" {
  vpc_id = var.locals_env.sagemaker_unified_studio.network.vpcid
  tags = {
    Name = "lakehouse-sample-private-rt"
  }
  # route {
  #   cidr_block     = "0.0.0.0/0"
  #   nat_gateway_id = aws_nat_gateway.nat.id
  # }
}