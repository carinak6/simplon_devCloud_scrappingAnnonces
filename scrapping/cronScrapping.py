from crontab import CronTab
#* * * * * #signifie: chaque minute de chaque heure de chaque jour du mois pour chaque mois pour chaque jour de la semaine.
#0 16 1,10,22 * * #dit à cron d'exécuter une tâche à 16 heures (ce qui correspond à la 16e heure) les 1er, 10 et 22 de chaque mois.
#30 * * * *

cron = CronTab(user='caryk6')

job = cron.new(command='python main.py', comment='execute tous les heures')
#my command définit la tâche à exécuter via la ligne de commande.

job.minute.every(2)

cron.write()

