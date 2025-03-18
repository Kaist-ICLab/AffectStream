resource "aws_eks_cluster" "eks-cluster" {

  name     = var.name
  role_arn = aws_iam_role.iam-role-eks-cluster.arn
  version = local.eks_version

  depends_on = [
    aws_iam_role_policy_attachment.iam-policy-eks-cluster,
    aws_iam_role_policy_attachment.iam-policy-eks-cluster-vpc,
  ]

  enabled_cluster_log_types = ["api", "audit", "authenticator", "controllerManager", "scheduler"]

  vpc_config {
    security_group_ids      = [aws_security_group.eks-cluster.id]
    subnet_ids              = var.subnet_ids
    endpoint_public_access  = true
  }

  tags = merge(var.tags, tomap({
    "Name" = "eks-cluster"
  }))
}