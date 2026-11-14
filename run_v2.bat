@echo off
cd /d "%~dp0"
echo ===================================================================
echo   Starting AI Escape Room - VERSION 2 (Reliable State Machine)
echo ===================================================================
echo   Dedicated Port: 8502 (No conflict with Version 1)
echo   Opening: http://localhost:8502 ...
echo ===================================================================
python -m streamlit run app_v2.py --server.port 8502
pause
