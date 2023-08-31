#!/bin/bash

if [ -f .env ]; then
    echo ".env file already exists."
else
    echo "Creating .env file..."
    read -p "Enter your ChatGPT API key: " api_key
    echo "API_KEY=\"$api_key\"" > .env
fi

if [ -d venv ]; then
    echo "Found venv."
else
    echo "Creating venv..."
    python3 -m virtualenv ./venv
fi
source venv/bin/activate

echo "Installing Python packages..."
pip install -r requirements.txt

echo "Running main.py..."
python3 main.py
