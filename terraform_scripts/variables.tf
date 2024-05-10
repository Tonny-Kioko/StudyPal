variable "env" {
    type = string
    description = "Deployment environments between prod and dev"
}

variable "vpc_config" {
    type = any
    description = "Config p[arameters for the VPC (subnets, cidr blocks, elastic IPs etc)"  
}

variable "cluster_config" {
    type = any
    description = "Config management for the cluster and its settings"  
}

variable "ui_config" {
    type = any
    description = "UI config settings"     
}

variable "ecr_names" {
    type = any
    description = "Names for ECR repositories required forr deployment"
  
}

