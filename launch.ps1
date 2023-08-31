Write-Host "Installing Python packages..."
pip install -r requirements.txt

Write-Host "Running main.py..."
Start-Process python.exe -ArgumentList "main.py" -WindowStyle Maximized
