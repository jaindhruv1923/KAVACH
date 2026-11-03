@echo off
REM ==============================================================================
REM PRJ4 KAVACH 1-Click Instant Live Public Cloud Edge Tunnel
REM Generates a live public HTTPS URL with SSL in 5 seconds with ZERO install!
REM ==============================================================================
title PRJ4 KAVACH Live Public Cloud Edge Tunnel
cls
echo ==================================================================
echo   PRJ4 KAVACH LIVE EDGE CLOUD TUNNEL (PORT 8001 PUBLIC HTTPS)
echo ==================================================================
echo Connecting to secure edge reverse proxy over localhost:8001...
echo Free SSL HTTPS link will be generated below in 3 seconds.
echo Press Ctrl+C to close the tunnel.
echo.

ssh -o StrictHostKeyChecking=no -R 80:127.0.0.1:8001 nokey@localhost.run
pause

