@echo off
echo Starting Scalable Hybrid RAG Pipeline...

:: Start FastAPI Server
start "RAG Backend" cmd /k "uvicorn app.main:app --host 0.0.0.0 --port 8000"

:: Start Embedding Worker
timeout /t 5
start "RAG Worker" cmd /k "python workers/embedding_worker.py"

:: Start Streamlit UI
timeout /t 5
start "RAG Frontend" cmd /k "streamlit run app_ui.py"

echo All components launched!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:8501
pause
