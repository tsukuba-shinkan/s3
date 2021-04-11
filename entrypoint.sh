#!/bin/bash
PORT="${PORT:-8000}"
echo "Running in $PORT"
python3 download.py
python3 gen_wordtable.py
python3 gen_wordtable_event.py

uvicorn app:app --host 0.0.0.0 --port $PORT