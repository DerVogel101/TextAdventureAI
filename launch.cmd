@echo off

if exist .env (
    echo .env file already exists.
) else (
    echo Creating .env file...
    set /p api_key=Enter your ChatGPT API key:
    echo API_KEY="%api_key%">.env
)

echo Installing Python packages...
pip install -r requirements.txt

echo Running main.py...
start /max python main.py
