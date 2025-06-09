terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.2.0"
}

provider "aws" {
  region = var.aws_region
}

# VPC Configuration
resource "aws_vpc" "pms_vpc" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "pms-vpc"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "pms_igw" {
  vpc_id = aws_vpc.pms_vpc.id

  tags = {
    Name = "pms-igw"
  }
} 