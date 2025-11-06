#!/bin/bash
echo "🚀 Setting up virtual environment and installing dependencies..."
python3 -m venv venv312
source venv312/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Setup complete. Activate with: source venv312/bin/activate"
