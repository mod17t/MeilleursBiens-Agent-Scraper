# MeilleursBiens-Agent-Scraper
Script développé en Python 3 pour extraire automatiquement les profils de tous les agents du réseau immobilier MeilleursBiens et les exporter dans un fichier CSV.
# Ce que fait le script
Le script commence par parcourir l'annuaire principal de MeilleursBiens en gérant la pagination pour récupérer l'ensemble des profils disponibles. Plutôt que de parser le HTML de la page, il exploite une API interne identifiée en analysant le trafic réseau via les DevTools du navigateur, ce qui rend l'extraction plus fiable et plus rapide.

Pour chaque agent, il récupère les informations suivantes : prénom, nom, code postal, ville, numéro de téléphone, adresse e-mail, nombre de biens actifs, prix moyen des biens actifs, nombre de biens vendus et l'URL du profil LinkedIn si elle est disponible.

Une fois toutes les données collectées, le script génère automatiquement un fichier agents.csv dans le répertoire courant. Les champs manquants sont laissés vides sans interrompre l'exécution, et les erreurs réseau sont gérées avec des tentatives de réessai automatiques. Des délais sont également ajoutés entre les requêtes pour respecter le serveur.
