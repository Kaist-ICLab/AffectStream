variable name {
  type        = string
  default     = "demo"
  description = "Prefix of resources"
}

variable vpc_id {
  type        = string
  description = "Key name for nat instance"
}

variable subnet_ids {
  type        = list
  description = "EKS cluster subnet ids"
}

variable instance_type {
  type        = string
  description = "EKS cluster node instance type"
}

variable eks_cluster_role {
  type        = string
  default     = "demo"
  description = "EKS cluster role"
}

variable eks_nodegroup_role {
  type        = string
  default     = "demo"
  description = "EKS cluster role"
}

variable tags {
  type        = map
  description = "Tag map for all resources"
}
