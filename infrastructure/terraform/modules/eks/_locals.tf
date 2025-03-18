locals {
  eks_version   = 1.25
  disk_size     = 20
  http_port     = 80
  ssh_port      = 22
  any_port      = 0
  any_protocol  = -1
  tcp_protocol  = "tcp"
  all_ip        = "0.0.0.0/0"
  all_ips       = ["0.0.0.0/0"]
}
