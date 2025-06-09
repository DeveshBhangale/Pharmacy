# Development Utilities

This directory contains various utilities and scripts to help with development and testing of the Pharmacy Management System.

## Directory Structure

```
dev-utils/
├── mock-data/           # Mock data generation utilities
│   ├── generate_mock_data.py    # Script to generate mock data
│   └── mock_data/              # Generated mock data files
└── scripts/            # Utility scripts
    ├── setup_dev_env.sh        # Development environment setup
    └── seed_database.py        # Database seeding script
```

## Mock Data Generation

The mock data generator creates realistic test data for:
- Medicines
- Customers
- Orders
- Prescriptions

To generate mock data:

```bash
cd mock-data
python generate_mock_data.py
```

This will create JSON files in the `mock_data` directory containing the generated data.

## Development Scripts

### Setup Development Environment

The `setup_dev_env.sh` script automates the setup of your development environment:
- Creates Python virtual environment
- Installs backend dependencies
- Installs frontend dependencies
- Generates mock data
- Sets up git hooks for code quality

To use:

```bash
cd scripts
./setup_dev_env.sh
```

### Seed Database

The `seed_database.py` script populates the databases with mock data:
- Seeds DynamoDB tables
- Seeds RDS database
- Uploads sample files to S3

To use:

```bash
cd scripts
python seed_database.py
```

Environment variables:
- `DYNAMODB_TABLE`: DynamoDB table name (default: pms-dev)
- `DATABASE_URL`: RDS connection string
- `S3_BUCKET`: S3 bucket name (default: pms-storage-dev)

## Requirements

- Python 3.9+
- Node.js 16+
- AWS CLI configured with appropriate credentials
- PostgreSQL client (for RDS seeding)
- Docker (optional, for containerized development) 