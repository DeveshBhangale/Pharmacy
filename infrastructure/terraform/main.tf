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

# DynamoDB Table
resource "aws_dynamodb_table" "pms_table" {
  name           = "${var.app_name}-${var.environment}"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "PK"
  range_key      = "SK"

  attribute {
    name = "PK"
    type = "S"
  }

  attribute {
    name = "SK"
    type = "S"
  }

  tags = {
    Environment = var.environment
  }
}

# ElastiCache (Redis)
resource "aws_elasticache_cluster" "pms_redis" {
  cluster_id           = "${var.app_name}-${var.environment}"
  engine              = "redis"
  node_type           = "cache.t3.micro"
  num_cache_nodes     = 1
  parameter_group_name = "default.redis6.x"
  port                = 6379
  security_group_ids  = [aws_security_group.redis_sg.id]
}

# S3 Bucket
resource "aws_s3_bucket" "pms_storage" {
  bucket = "${var.app_name}-storage-${var.environment}"

  tags = {
    Environment = var.environment
  }
}

# RDS Instance
resource "aws_db_instance" "pms_db" {
  identifier           = "${var.app_name}-${var.environment}"
  allocated_storage    = 20
  storage_type         = "gp2"
  engine              = "postgres"
  engine_version      = "13.7"
  instance_class      = "db.t3.micro"
  username            = var.db_username
  password            = var.db_password
  skip_final_snapshot = true

  vpc_security_group_ids = [aws_security_group.rds_sg.id]

  tags = {
    Environment = var.environment
  }
}

# ECS Cluster
resource "aws_ecs_cluster" "pms_cluster" {
  name = "${var.app_name}-cluster-${var.environment}"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

# Security Groups
resource "aws_security_group" "redis_sg" {
  name        = "${var.app_name}-redis-sg"
  description = "Security group for Redis"
  vpc_id      = aws_vpc.pms_vpc.id

  ingress {
    from_port   = 6379
    to_port     = 6379
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }
}

resource "aws_security_group" "rds_sg" {
  name        = "${var.app_name}-rds-sg"
  description = "Security group for RDS"
  vpc_id      = aws_vpc.pms_vpc.id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }
} 