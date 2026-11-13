@echo off
title KAVACH MidSem Cloud Tunnel (Port 8000)
color 0B
echo Starting Public Cloud Tunnel for MidSem Platform (Port 8000)...
ssh -o StrictHostKeyChecking=no -R 80:127.0.0.1:8000 nokey@localhost.run
pause
