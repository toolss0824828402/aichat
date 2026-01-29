#!/bin/bash
apt update && apt upgrade -y
pkg install python -y
pip install -r requirements.txt
echo "Setup Complete! Run: python ai_dragon.py"
