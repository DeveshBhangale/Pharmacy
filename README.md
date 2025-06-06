# Pharmacy Management System

An enterprise-level pharmacy management system that integrates AI-powered medicine recommendations, inventory management, and price comparison features.

## Features

- 🤖 AI-powered medicine recommendations using RNN
- 📦 Real-time inventory management
- 💊 Prescription upload and processing
- 💰 Medicine price comparison
- 🔍 Search and filter capabilities
- 📱 Responsive web interface
- 🔒 Secure authentication and authorization
- 📊 Analytics dashboard

## Tech Stack

### Backend
- Python 3.9+
- FastAPI
- TensorFlow
- AWS DynamoDB
- AWS ElastiCache (Redis)
- AWS S3

### Frontend
- Vue.js
- React.js
- TailwindCSS
- TypeScript

### Infrastructure
- AWS (ECS, EC2, RDS)
- Docker
- CI/CD with GitHub Actions

## Project Structure

```
pms/
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Core functionality
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   └── ml/             # ML models and utilities
│   ├── tests/              # Backend tests
│   └── requirements.txt    # Python dependencies
├── frontend/               # Frontend applications
│   ├── admin/             # React.js admin dashboard
│   └── customer/          # Vue.js customer portal
├── infrastructure/        # AWS infrastructure code
│   ├── terraform/        # Terraform configurations
│   └── docker/           # Docker configurations
└── dev-utils/            # Development utilities
    ├── mock-data/        # Mock data generators
    └── scripts/          # Utility scripts
```

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 16+
- Docker
- AWS CLI
- Terraform

### Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pms.git
cd pms
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up the frontend:
```bash
cd frontend/customer
npm install
cd ../customer
npm install
```

4. Start the development servers:
```bash
# Backend
cd backend
uvicorn app.main:app --reload

# Frontend (Admin)
cd frontend/admin
npm run dev

# Frontend (Customer)
cd frontend/customer
npm run dev
```

## Deployment

The system is designed to be deployed on AWS using infrastructure as code (Terraform). See the `infrastructure` directory for deployment configurations.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- AWS for cloud infrastructure
- TensorFlow team for ML capabilities
- Vue.js and React.js communities 