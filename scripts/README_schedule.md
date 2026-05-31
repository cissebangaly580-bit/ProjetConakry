# Création de la tâche planifiée — ConakryBackupDaily

Étapes rapides :

1. Ouvrez l'explorateur et allez dans le dossier `scripts` du projet.
2. Faites un clic droit sur `create_backup_task.bat` puis choisissez "Exécuter en tant qu'administrateur".
3. Acceptez l'invite UAC. Une fenêtre PowerShell s'ouvrira et exécutera `schedule_backup.ps1` avec élévation.
4. Vérifiez la présence de la tâche :

```powershell
Get-ScheduledTask -TaskName 'ConakryBackupDaily'
```

Si vous préférez exécuter manuellement la commande PowerShell (en tant qu'administrateur), copiez celle fournie précédemment dans la conversation.
