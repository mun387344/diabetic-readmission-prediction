#!/bin/bash

# Start FastAPI inference microservice in background on port 8000
echo "Starting FastAPI backend service on port 8000..."
uvicorn app.api:app --host 0.0.0.0 --port 8000 &

# Wait briefly for FastAPI to initialize
sleep 3

# Start Streamlit clinical dashboard in foreground on port 8501
echo "Starting Streamlit frontend on port 8501..."
streamlit run app/ui.py --server.port 8501 --server.address 0.0.0.0