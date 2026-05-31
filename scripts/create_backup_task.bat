@echo off
REM Lance le script PowerShell de création de tâche planifiée avec élévation (UAC).
REM Double-cliquez ou faites "Exécuter en tant qu'administrateur" sur ce fichier.

powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process powershell -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File \"%~dp0schedule_backup.ps1\"' -Verb RunAs"

pause
