@echo off
echo Installing Python packages...
pip install -r requirements.txt

echo Running main.py...
start /max python main.py