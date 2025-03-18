resource "aws_security_group" "msk" {
  name        = "msk"
  description = "Allow msk traffic"
  vpc_id      = var.vpc_id

  ingress {
    description = "all ingress traffic allowed"
    from_port   = local.any_port
    to_port     = local.any_port
    protocol    = local.tcp_protocol
    cidr_blocks = local.all_ips
  }

  egress {
    description = "all egress traffic allowed"
    from_port   = local.any_port
    to_port     = local.any_port
    protocol    = local.tcp_protocol
    cidr_blocks = local.all_ips
  }

  tags = merge(var.tags, tomap({
    "Name" = var.name
  }))
}
