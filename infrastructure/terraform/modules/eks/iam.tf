# EKS cluster iam role

resource "aws_iam_role" "iam-role-eks-cluster" {
  name                  = "iam-role-eks-cluster"
  assume_role_policy    = var.eks_cluster_role
}

resource "aws_iam_role_policy_attachment" "iam-policy-eks-cluster" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.iam-role-eks-cluster.name
}

resource "aws_iam_role_policy_attachment" "iam-policy-eks-cluster-vpc" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSVPCResourceController"
  role       = aws_iam_role.iam-role-eks-cluster.name
}


# EKS nodegroup iam role

resource "aws_iam_role" "iam-role-eks-nodegroup" {
  name                  = "iam-role-eks-nodegroup"
  assume_role_policy    = var.eks_nodegroup_role
}

resource "aws_iam_role_policy_attachment" "iam-policy-eks-nodegroup" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.iam-role-eks-nodegroup.name
}

resource "aws_iam_role_policy_attachment" "iam-policy-eks-nodegroup-cni" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.iam-role-eks-nodegroup.name
}

resource "aws_iam_role_policy_attachment" "iam-policy-eks-nodegroup-ecr" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.iam-role-eks-nodegroup.name
}
