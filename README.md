# Recruitment API

## Description
Recruitment API est une architecture back-end développée avec Django et Django REST Framework. Le système met en relation des candidats et des recruteurs, en intégrant un pipeline d'authentification robuste et une gestion stricte des autorisations.

## Fonctionnalités Principales
- **Authentification Sécurisée** : Connexion via JWT (JSON Web Tokens) couplée à une vérification par email via code OTP (One Time Password). Le module inclut des mécanismes de prévention de la force brute.
- **Connexion Google (OAuth2)** : Les utilisateurs peuvent s'authentifier via leur compte Google. L'endpoint `/api/v1/auth/google/` accepte un Access Token Google et retourne une paire de tokens JWT propres à l'API.
- **Gestion des Rôles (RBAC)** : Architecture basée sur le principe de moindre privilège avec ségrégation stricte des rôles (Admin, Recruteur, Candidat).
- **Candidatures et Suivi** : Processus de postulation avec attachement de fichiers (CV/Lettres), suivi des statuts en temps réel par les recruteurs.
- **Analytics** : Tableaux de bord différenciés générant des statistiques d'attractivité (taux de conversion) pour les offres.
- **Système de Notifications** : Traçabilité asynchrone pour informer les acteurs des changements d'états d'une candidature.

## Endpoints et Documentation
Ce projet intègre `drf-spectacular` pour générer automatiquement le schéma OpenAPI.
Une fois le serveur de développement lancé, la documentation interactive est accessible sur :
- `http://127.0.0.1:8000/api/docs/`

Cette documentation liste de manière exhaustive toutes les ressources, les objets attendus et les codes de réponse HTTP configurés (200, 201, 400, 401, 403, 404).

## Déploiement Local

### 1. Prérequis
Vous devez disposer de Python 3 et d'un environnement virtuel configuré.

### 2. Installation
Clonez le dépôt puis installez les dépendances :
```bash
pip install -r requirements.txt
```

### 3. Configuration de l'environnement
Un fichier `.env` est requis à la racine du projet pour la gestion sécurisée des secrets. Il doit contenir a minima :
```
SECRET_KEY=votre_cle_django_securisee
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

### Configuration Google OAuth2
Pour activer la connexion via Google, vous devez créer un projet sur la [Google Cloud Console](https://console.cloud.google.com/), activer l'API OAuth2 et récupérer vos identifiants. Ajoutez ensuite dans la table `socialaccount_socialapp` via l'interface d'administration :
- **Provider** : google
- **Client ID** : votre identifiant OAuth2
- **Secret Key** : votre clé secrète OAuth2

Le flux d'authentification est le suivant :
1. Le frontend obtient un Access Token Google via le SDK Google.
2. Il envoie ce token à `POST /api/v1/auth/google/`.
3. L'API vérifie le token auprès de Google, crée ou récupère l'utilisateur, et retourne une paire de tokens JWT.

### 4. Base de données
Appliquez les migrations afin de structurer la base de données :
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Lancement
Démarrez le serveur de développement local :
```bash
python manage.py runserver
```
