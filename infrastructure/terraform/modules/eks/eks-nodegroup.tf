resource "aws_eks_node_group" "eks-nodegroup" {

  node_group_name = "eks-nodegroup"
  cluster_name    = aws_eks_cluster.eks-cluster.name
  node_role_arn   = aws_iam_role.iam-role-eks-nodegroup.arn
  subnet_ids      = var.subnet_ids
  instance_types  = [var.instance_type]
  disk_size       = local.disk_size

  labels = {
    "role" = "eks-nodegroup"
  }

  scaling_config {
    desired_size = 5
    min_size     = 5
    max_size     = 7
  }

  depends_on = [
    aws_iam_role_policy_attachment.iam-policy-eks-nodegroup,
    aws_iam_role_policy_attachment.iam-policy-eks-nodegroup-cni,
    aws_iam_role_policy_attachment.iam-policy-eks-nodegroup-ecr,
  ]

  tags = merge(var.tags, tomap({
    "Name" = "${aws_eks_cluster.eks-cluster.name}-worker-node"
  }))
}