@echo off
call .venv\Scripts\activate
start pythonw.exe .\src\main.py
deactivate
