@echo off
chcp 65001 > nul
title Discord Emoji and Sticker Cloner
echo Starting Discord Emoji and Sticker Cloner...
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" main.py
) else (
    python main.py
)
pause
