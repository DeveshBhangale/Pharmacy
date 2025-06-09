#!/bin/bash

# Exit on error
set -e

echo "Setting up development environment..."

# Create Python virtual environment
echo "Creating Python virtual environment..."
cd ../../backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Install frontend dependencies
echo "Installing frontend dependencies..."
cd ../frontend/customer
npm install

cd ../admin
npm install

# Generate mock data
echo "Generating mock data..."
cd ../../dev-utils/mock-data
python generate_mock_data.py

# Set up pre-commit hooks
echo "Setting up git hooks..."
cd ../..
if [ ! -f .git/hooks/pre-commit ]; then
    cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
set -e

echo "Running pre-commit checks..."

# Check Python formatting
cd backend
source venv/bin/activate
black --check .
flake8 .

# Check frontend formatting
cd ../frontend/customer
npm run lint
cd ../admin
npm run lint

echo "All checks passed!"
EOF
    chmod +x .git/hooks/pre-commit
fi

echo "Development environment setup complete!" 