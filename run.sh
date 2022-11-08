#!/bin/bash
echo "Running in $(pwd) as $(whoami)"
sudo uvicorn main:app --host 0.0.0.0 --port 80 --reload
#sudo nohup uvicorn backend:app --reload --host 0.0.0.0 --port 80 2>&1 &
