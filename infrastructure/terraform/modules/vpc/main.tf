# VPC
resource "aws_vpc" "this" {
  cidr_block = var.cidr

  tags = merge(var.tags, tomap({
    "Name" = format("%s", var.name)
  }))
}

# Internet gateway
resource "aws_internet_gateway" "this" {
  vpc_id  = aws_vpc.this.id

  tags = merge(var.tags, tomap({
    "Name" = format("%s", var.name)
  }))
}

# Subnets
resource "aws_subnet" "public" {
  count = "${length(var.public_subnets)}"

  vpc_id                  = aws_vpc.this.id
  cidr_block              = var.public_subnets[count.index]
  availability_zone       = var.azs[count.index]
  map_public_ip_on_launch = true

  tags = merge(var.tags, tomap({
    "Name" = format("%s-public-%s", var.name, var.azs[count.index])
  }))
}

# Route tables
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.this.id

  route {
    cidr_block = local.all_ip
    gateway_id = aws_internet_gateway.this.id
  }

  tags = merge(var.tags, tomap({
    "Name" = format("%s-public", var.name)
  }))
}

# Route table associations
resource "aws_route_table_association" "public" {
  count = length(var.public_subnets)

  subnet_id       = aws_subnet.public.*.id[count.index]
  route_table_id  = aws_route_table.public.id
}

# Security group
resource "aws_security_group" "ssh" {
  name        = "ssh"
  description = "Allow ssh traffic"
  vpc_id      = aws_vpc.this.id

  ingress {
    description = "ssh connection"
    from_port   = local.ssh_port
    to_port     = local.ssh_port
    protocol    = local.tcp_protocol
    cidr_blocks = local.all_ips
  }

  egress {
    from_port   = local.any_port
    to_port     = local.any_port
    protocol    = local.any_protocol
    cidr_blocks = local.all_ips
  }

  tags = merge(var.tags, tomap({
    "Name" = format("%s-ssh", var.name)
  }))
}

# Key pair
resource "aws_key_pair" "main" {
  key_name   = var.key_name
  public_key = var.key_file
}
