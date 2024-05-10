resource "aws_vpc" "studypalvpc" {
    cidr_block = var.vpc_config.vpc_cidr_block
    instance_tenancy = var.vpc_config.instance_tenancy
    enable_dns_hostnames = var.vpc_config.enable_dns_hostnames
    enable_dns_support = var.vpc_config.enable_dns_support

    tags = {
        name = "${local.project}-${var.env}-main"
    }  
}

resource "aws_internet_gateway" "studypaligw" {
  vpc_id = aws_vpc.studypalvpc.id
  tags = {
    name = "${local.project}-${var.env}-igw"
  }
}
resource "aws_eip" "studypalnat" {
    vpc = true
    tags = {
      name = "${local.project}-${var.env}-eip"
    }  
}

resource "aws_nat_gateway" "studypalnat" {
    allocation_id = aws_eip.studypalnat.id
    subnet_id = aws_subnet.public-ap-south-1a.id

    tags = {
      name = "${local.project}-${var.env}-nat"
    }
    depends_on = [aws_internet_gateway.studypaligw]  
}
