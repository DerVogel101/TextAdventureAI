Write-Host "Checking for .env file..."
if (Test-Path .env) {
    Write-Host ".env file already exists."
} else {
    Write-Host "Creating .env file..."
    $api_key = Read-Host "Enter your ChatGPT API key:"
    "API_KEY=`"$api_key`"" | Out-File -Encoding utf8 .env
}

Write-Host "Installing Python packages..."
pip install -r requirements.txt

Write-Host "Running main.py..."
Start-Process python.exe -ArgumentList "main.py" -WindowStyle Maximized
