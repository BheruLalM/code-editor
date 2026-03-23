$port = 8000
$tcp = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
if ($tcp) {
    $processes = Get-Process -Id $tcp.OwningProcess -ErrorAction SilentlyContinue
    if ($processes) {
        $processes | Stop-Process -Force
        Write-Host "Killed process on port $port"
    }
}
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --port 8000
