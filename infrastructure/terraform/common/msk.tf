module "msk-cluster" {
  source = "../modules/msk"
  
  name              = "demo"
  vpc_id            = module.vpc.vpc_id
  client_subnets    = module.vpc.public_subnet_ids
  kafka_version     = "3.5.1"
  instance_type     = "kafka.t3.small"
  broker_cnt        = 9
  volume_size       = 100

  tags = {
    "TerraformManaged" = "true"
  }
}

# resource "aws_msk_cluster" "example" {
#   cluster_name           = "test"
#   kafka_version          = "2.8.1"
#   number_of_broker_nodes = 3

#   broker_node_group_info {
#     instance_type = "kafka.t3.small"
#     client_subnets = module.vpc.public_subnet_ids
#     connectivity_info {
#       public_access {
#         type = "SERVICE_PROVIDED_EIPS"
#       }
#     }
#     storage_info {
#       ebs_storage_info {
#         volume_size = 100
#       }
#     }
#     security_groups = []
#   }

#   client_authentication {
#     unauthenticated = true
#   }

#   encryption_info {
#     encryption_in_transit {
#       client_broker = "PLAINTEXT"
#       in_cluster    = true
#     }
#   }

#   logging_info {
#     broker_logs {
#       cloudwatch_logs {
#         enabled = false
#       }

#       firehose {
#         enabled = false
#       }

#       s3 {
#         enabled = false
#       }
#     }
#   }

#   open_monitoring {
#     prometheus {
#       jmx_exporter {
#         enabled_in_broker = true
#       }

#       node_exporter {
#         enabled_in_broker = true
#       }
#     }
#   }
# }

# resource "aws_msk_scram_secret_association" "example" {
#   cluster_arn     = aws_msk_cluster.example.arn
#   secret_arn_list = [aws_secretsmanager_secret.example.arn]

#   depends_on = [aws_secretsmanager_secret_version.example]
# }
