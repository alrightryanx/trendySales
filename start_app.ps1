Write-Host "Starting Omniscient Market Tracker..." -ForegroundColor Green

# Start Backend
Write-Host "Launching Backend on Port 8000..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; pip install -r requirements.txt; uvicorn main:app --reload --host 127.0.0.1 --port 8000"

# Start Frontend
Write-Host "Launching Frontend on Port 4303..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev -- -p 4303"

Write-Host "System coming online. Please wait for browser to load http://localhost:4303" -ForegroundColor Cyan
Start-Sleep -Seconds 5
Start-Process "http://localhost:4303"
