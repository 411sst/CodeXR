#!/usr/bin/env python3
import subprocess
import sys

print("🥽 Starting CodeXR...")
try:
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
except KeyboardInterrupt:
    print("\n👋 Thanks for using CodeXR!")
