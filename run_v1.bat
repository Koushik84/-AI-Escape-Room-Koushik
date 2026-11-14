@echo off
cd /d "%~dp0"
echo ===================================================================
echo   Starting AI Escape Room - VERSION 1 (Conversational LLM)
echo ===================================================================
echo   Dedicated Port: 8501 (No conflict with Version 2)
echo   Opening: http://localhost:8501 ...
echo ===================================================================
python -m streamlit run app_v1.py --server.port 8501
pause
