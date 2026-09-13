@echo off
title Aplikasi Perpustakaan
cd /d "%~dp0"

start "" http://127.0.0.1:5000/
python Website/app.py
pause
