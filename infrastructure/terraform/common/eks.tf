module "eks" {
  source = "../modules/eks"

  name          = "demo"
  vpc_id        = module.vpc.vpc_id
  subnet_ids    = module.vpc.public_subnet_ids
  instance_type = "c5a.xlarge"

  eks_cluster_role    = file("../iam/eks-cluster.json")
  eks_nodegroup_role  = file("../iam/eks-nodegroup.json")

  tags = {
    "TerraformManaged" = "true"
  }
}