# Infrastructure Setup

This directory contains all the infrastructure configurations for the Pharmacy Management System.

## Directory Structure

```
infrastructure/
├── terraform/          # Terraform configurations for AWS resources
├── docker/            # Docker configurations for containerization
└── README.md         # This file
```

## Prerequisites

- AWS CLI configured with appropriate credentials
- Terraform >= 1.2.0
- Docker and Docker Compose
- Node.js >= 16.x
- Python >= 3.9

## AWS Resources

The following AWS resources are managed through Terraform:

- VPC with Internet Gateway
- DynamoDB table for data storage
- ElastiCache (Redis) for caching
- S3 bucket for file storage
- RDS (PostgreSQL) for relational data
- ECS Cluster for container orchestration
- Security Groups for resource access control

## Local Development

1. Start the local development environment:
```bash
cd docker
docker-compose up
```

2. Access the services:
- Backend API: http://localhost:8000
- Customer Frontend: http://localhost:3000
- Admin Frontend: http://localhost:3001

## Deployment

1. Initialize Terraform:
```bash
cd terraform
terraform init
```

2. Create a `terraform.tfvars` file with required variables:
```hcl
aws_region = "us-west-2"
environment = "dev"
db_username = "admin"
db_password = "your-secure-password"
```

3. Apply the Terraform configuration:
```bash
terraform apply
```

4. The CI/CD pipeline will automatically deploy changes when merged to main.

## Security

- All sensitive values are stored in AWS Secrets Manager
- Security groups restrict access to resources
- SSL/TLS encryption for all public endpoints
- Regular security updates through CI/CD pipeline 