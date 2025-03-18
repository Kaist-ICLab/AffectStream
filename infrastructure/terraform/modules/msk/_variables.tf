variable name {
  type        = string
  default     = "demo"
  description = "Prefix of resources"
}

variable vpc_id {
  type        = string
  description = "VPC id"
}

variable client_subnets {
  type        = list
  description = "EKS cluster subnet ids"
}

variable kafka_version {
  type        = string
  description = "Prefix of resources"
}

variable instance_type {
  type        = string
  description = "Prefix of resources"
}

variable broker_cnt {
  type        = number
  description = "VPC public subnet IP lists"
}

variable volume_size {
  type        = number
  description = "VPC public subnet IP lists"
}

# variable kms_arn {
#   type        = string
#   description = "KMS arn for MSK TLS authentication"
# }

variable tags {
  type        = map
  description = "Tag map for all resources"
}
