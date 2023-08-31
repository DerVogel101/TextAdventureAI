#!/bin/bash

echo "Installing Python packages..."
pip install -r requirements.txt

echo "Running main.py..."
python3 main.py
