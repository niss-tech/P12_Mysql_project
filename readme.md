# Epic Events CRM

Ce projet est une application CRM en ligne de commande (CLI) développée en Python avec SQLAlchemy et MySQL, dans le cadre de la formation OpenClassrooms (Projet P12). Il permet de gérer les clients, contrats et événements selon les droits des collaborateurs (gestion, commercial, support).



## Installation

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/niss-tech/P12_Mysql_project.git
   cd P12_Mysql_project
   ```

2. **Créer un environnement virtuel**
   ```bash
   python -m venv env
   source env/bin/activate      # Linux/macOS
   env\Scripts\activate       # Windows
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```



## Configuration de la base de données

L’application utilise **MySQL** avec **SQLAlchemy** comme ORM.

### Étapes :

1. **Créer la base de données**
   - Nom : `epic_crm`
   - Tu peux utiliser MySQL Workbench ou une commande :
     ```sql
     CREATE DATABASE epic_crm;
     ```

2. **(Optionnel) Créer un utilisateur MySQL dédié**
   ```sql
   CREATE USER 'epic_user'@'localhost' IDENTIFIED BY 'motdepasse';
   GRANT ALL PRIVILEGES ON epic_crm.* TO 'epic_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

3. **Configurer le fichier `.env`**
   À la racine du projet, créer un fichier `.env` :
   ```
   DB_USER=epic_user
   DB_PASSWORD=motdepasse
   DB_HOST=localhost
   DB_NAME=epic_crm
   ```

4. **Initialiser les tables**
   Une fois la base et le `.env` configurés :
   ```bash
   python init_db.py
   ```
   Ensuite un message sera affiché : `Tables créées avec succès !`



## Lancement de l'application

```bash
python app.py
```



## Fonctionnalités

- **Authentification** sécurisée avec hachage des mots de passe (`argon2`)
- **Permissions par rôle** :
  - Le **commercial** peut créer des clients, voir ses contrats et les modifier, créer des événements à partir de contrats signés
  - Le **gestionnaire** peut créer/modifier/supprimer des utilisateurs sur la plateforme , créer/modifier tous les contrats, modifier les évènements
  - Le **support** peut modifier uniquement ses propres événements attribués
- **Contrôle d'accès** au menu selon le rôle
- **Interface CLI** claire et interactive
- **Journalisation des erreurs** via Sentry
- **Tests unitaires et d'intégration** avec `pytest`
- **Stockage local de la session utilisateur** (session/session.json)



## Tests et couverture

- Les tests unitaires et d'intégration sont effectués avec `pytest`.
- La couverture de code est mesurée avec `coverage`.
- Pour générer un rapport HTML :
  ```bash
  pytest --cov=controllers --cov-report=html tests/


Le rapport sera généré dans le dossier htmlcov/ et peut être ouvert avec un navigateur.


## Configuration de la journalisation avec Sentry

L’application utilise [**Sentry**](https://sentry.io) pour journaliser les erreurs et exceptions non gérées. Cela permet de centraliser les erreurs critiques en production.

### Installation de la dépendance

Sentry est déjà inclus dans `requirements.txt`, mais si besoin :

```bash
pip install sentry-sdk python-dotenv
```

### Configuration

1. **Créer un compte sur** [https://sentry.io](https://sentry.io)
2. **Créer un projet de type Python**, puis récupérer le **DSN** (clé de connexion)
3. **Ajouter ce DSN dans le fichier `.env`** à la racine du projet :

   ```env
   SENTRY_DSN=https://<votre_dsn_ici>
   ```

4. Le fichier `config/logging_config.py` initialise automatiquement Sentry avec l'option suivante :
   - `send_default_pii=True` : pour enregistrer les infos utiles (comme l’adresse IP)

5. L’appel à `init_sentry()` est fait dans `app.py` avant le lancement de l’application.

### Résultat

Toutes les erreurs non attrapées ou les exceptions critiques sont automatiquement envoyées à Sentry.


