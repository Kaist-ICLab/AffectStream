resource "aws_security_group" "eks-cluster" {
  name        = "eks-cluster"
  description = "security_group for eks-cluster"
  vpc_id      = var.vpc_id

  tags = merge(var.tags, tomap({
    "Name" = "eks-cluster"
  }))
}

resource "aws_security_group_rule" "eks-cluster-ingress" {

  security_group_id = aws_security_group.eks-cluster.id
  type              = "ingress"
  description       = "ingress security_group_rule for eks-cluster"
  from_port         = local.any_port
  to_port           = local.any_port
  protocol          = local.any_protocol
  cidr_blocks       = local.all_ips
}

resource "aws_security_group_rule" "eks-cluster-egress" {

  security_group_id = aws_security_group.eks-cluster.id
  type              = "egress"
  description       = "egress security_group_rule for eks-cluster"
  from_port         = local.any_port
  to_port           = local.any_port
  protocol          = local.any_protocol
  cidr_blocks       = local.all_ips
}
