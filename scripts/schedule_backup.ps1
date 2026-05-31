# Script PowerShell pour planifier l'exécution quotidienne de la sauvegarde
# Usage: exécuter en tant qu'administrateur une fois pour créer la tâche planifiée

$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument '-NoProfile -WindowStyle Hidden -Command "python \"$PSScriptRoot\\backup_data.py\""'
$trigger = New-ScheduledTaskTrigger -Daily -At 3am
$principal = New-ScheduledTaskPrincipal -UserId "NT AUTHORITY\SYSTEM" -RunLevel Highest
Register-ScheduledTask -TaskName "ConakryBackupDaily" -Action $action -Trigger $trigger -Principal $principal -Description "Sauvegarde quotidienne du projet Conakry Travel"
Write-Output "Tâche planifiée 'ConakryBackupDaily' créée (3:00 AM daily)."
