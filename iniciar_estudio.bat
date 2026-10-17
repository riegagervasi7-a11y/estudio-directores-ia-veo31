@echo off
title Estudio de Directores IA - Modo Bestia
cd /d "%~dp0"
echo =======================================================================
echo          INICIANDO ESTUDIO DE DIRECTORES IA - INTERFAZ GRAFICA
echo =======================================================================
echo Abriendo servidor local en http://localhost:7860 ...
python servidor_gui.py
pause
