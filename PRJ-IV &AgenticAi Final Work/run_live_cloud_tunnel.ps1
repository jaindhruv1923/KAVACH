# ==============================================================================
# PRJ4 KAVACH 1-Click Instant Live Public Cloud Edge Tunnel
# Generates a live public HTTPS URL with SSL in 5 seconds with ZERO install!
# ==============================================================================

param(
    [int]$LocalPort = 8001
)

Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "   PRJ4 KAVACH LIVE EDGE CLOUD TUNNEL (PORT $LocalPort PUBLIC HTTPS)" -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host " Target Local Port: $LocalPort" -ForegroundColor Green

# Test if port is listening locally
$tcpTest = $false
try {
    $socket = New-Object System.Net.Sockets.TcpClient
    $socket.Connect("127.0.0.1", $LocalPort)
    $tcpTest = $true
    $socket.Close()
} catch {
    $tcpTest = $false
}

if (-not $tcpTest) {
    Write-Host "[WARNING] No service detected on localhost:$LocalPort." -ForegroundColor Red
    Write-Host "Make sure PRJ4 KAVACH is running on port $LocalPort" -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host "[SUCCESS] PRJ4 KAVACH is live on localhost:$LocalPort." -ForegroundColor Green
}

Write-Host "Establishing secure SSH reverse-proxy tunnel via localhost.run..." -ForegroundColor Cyan
Write-Host "Press Ctrl+C at any time to terminate the tunnel." -ForegroundColor DarkGray
Write-Host ""

ssh -o StrictHostKeyChecking=no -R 80:127.0.0.1:$LocalPort nokey@localhost.run

