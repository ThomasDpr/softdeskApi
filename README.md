# SoftDesk API Documentation

## Introduction

Bienvenue dans la documentation de l'API SoftDesk. Cette API est conçue pour gérer des projets, des utilisateurs, des contributeurs, des problèmes (issues) et des commentaires. Elle est construite avec Django et Django REST Framework, et utilise JWT pour l'authentification.

## Installation

### Cloner le dépôt

Pour commencer, clonez le dépôt sur votre machine :

```bash
git clone https://github.com/ThomasDpr/softdeskApi.git

cd softdesk-api
```

### Installation avec Pipenv

1. Assurez-vous que Pipenv est installé sur votre machine. Si ce n'est pas le cas, installez-le avec :

   ```bash
   pip install pipenv
   ```

2. Installez les dépendances :

   ```bash
   pipenv install
   ```

3. Activez l'environnement virtuel :

   ```bash
   pipenv shell
   ```

### Installation avec un environnement virtuel classique

1. Créez un environnement virtuel :

   ```bash
   python -m venv env
   ```

2. Activez l'environnement virtuel :

   - Sur Windows :

     ```bash
     .\env\Scripts\activate
     ```

   - Sur macOS et Linux :

     ```bash
     source env/bin/activate
     ```

3. Installez les dépendances :

   ```bash
   pip install -r requirements.txt
   ```


## Lancer le serveur

Pour démarrer le serveur de développement, exécutez :

```bash
python manage.py runserver
```


## Endpoints de l'API

### Authentification

- **Obtenir un token JWT :**

  - **URL :** `/api/token/`
  - **Méthode :** POST
  - **Données requises :**
    ```json
    {
      "username": "votre_nom_utilisateur",
      "password": "votre_mot_de_passe"
    }
    ```
  - **Réponse :**
    ```json
    {
      "access": "token_jwt_access",
      "refresh": "token_jwt_refresh"
    }
    ```

- **Rafraîchir un token JWT :**

  - **URL :** `/api/token/refresh/`
  - **Méthode :** POST
  - **Données requises :**
    ```json
    {
      "refresh": "token_jwt_refresh"
    }
    ```
  - **Réponse :**
    ```json
    {
      "access": "nouveau_token_jwt_access"
    }
    ```

### Utilisateurs

- **Créer un utilisateur :**

  - **URL :** `/api/users/`
  - **Méthode :** POST
  - **Données requises :**
    ```json
    {
      "username": "nouveau_nom_utilisateur",
      "password": "nouveau_mot_de_passe",
      "date_of_birth": "YYYY-MM-DD",
      "can_be_contacted": true,
      "can_data_be_shared": false
    }
    ```
  - **Réponse :**
    ```json
    {
      "status": "success",
      "message": "Utilisateur créé avec succès",
      "data": {
        "id": 1,
        "username": "nouveau_nom_utilisateur",
        "date_of_birth": "YYYY-MM-DD",
        "can_be_contacted": true,
        "can_data_be_shared": false
      }
    }
    ```

- **Lister les utilisateurs (admin uniquement) :**

  - **URL :** `/api/users/`
  - **Méthode :** GET
  - **Réponse :**
    ```json
    [
      {
        "id": 1,
        "username": "utilisateur1",
        "date_of_birth": "YYYY-MM-DD",
        "can_be_contacted": true,
        "can_data_be_shared": false
      },
      {
        "id": 2,
        "username": "utilisateur2",
        "date_of_birth": "YYYY-MM-DD",
        "can_be_contacted": false,
        "can_data_be_shared": true
      }
    ]
    ```

- **Mettre à jour son profil :**

  - **URL :** `/api/users/{id}/`
  - **Méthode :** PATCH
  - **Données requises :**
    ```json
    {
      "can_be_contacted": false
    }
    ```
  - **Réponse :**
    ```json
    {
      "id": 1,
      "username": "utilisateur1",
      "date_of_birth": "YYYY-MM-DD",
      "can_be_contacted": false,
      "can_data_be_shared": false
    }
    ```

- **Supprimer son profil :**

  - **URL :** `/api/users/{id}/`
  - **Méthode :** DELETE
  - **Réponse :**
    ```json
    {
      "status": "success",
      "message": "Utilisateur supprimé avec succès"
    }
    ```

### Projets

- **Créer un projet :**

  - **URL :** `/api/projects/`
  - **Méthode :** POST
  - **Données requises :**
    ```json
    {
      "title": "Nouveau Projet",
      "description": "Description du projet",
      "type": "back-end"
    }
    ```
  - **Réponse :**
    ```json
    {
      "id": 1,
      "title": "Nouveau Projet",
      "description": "Description du projet",
      "type": "back-end",
      "author": 1,
      "created_time": "2023-10-01T12:00:00Z"
    }
    ```

- **Lister les projets :**

  - **URL :** `/api/projects/`
  - **Méthode :** GET
  - **Réponse :**
    ```json
    [
      {
        "id": 1,
        "title": "Projet 1",
        "description": "Description du projet 1",
        "type": "back-end",
        "author": 1,
        "created_time": "2023-10-01T12:00:00Z"
      },
      {
        "id": 2,
        "title": "Projet 2",
        "description": "Description du projet 2",
        "type": "front-end",
        "author": 2,
        "created_time": "2023-10-02T12:00:00Z"
      }
    ]
    ```

- **Mettre à jour un projet (auteur uniquement) :**

  - **URL :** `/api/projects/{id}/`
  - **Méthode :** PATCH
  - **Données requises :**
    ```json
    {
      "title": "Projet Modifié"
    }
    ```
  - **Réponse :**
    ```json
    {
      "id": 1,
      "title": "Projet Modifié",
      "description": "Description du projet",
      "type": "back-end",
      "author": 1,
      "created_time": "2023-10-01T12:00:00Z"
    }
    ```

- **Supprimer un projet (auteur uniquement) :**

  - **URL :** `/api/projects/{id}/`
  - **Méthode :** DELETE
  - **Réponse :**
    ```json
    {
      "status": "success",
      "message": "Projet supprimé avec succès"
    }
    ```

### Contributeurs

- **Ajouter un contributeur (auteur uniquement) :**

  - **URL :** `/api/projects/{project_id}/contributors/`
  - **Méthode :** POST
  - **Données requises :**
    ```json
    {
      "user": 2
    }
    ```
  - **Réponse :**
    ```json
    {
      "id": 1,
      "user": 2,
      "username": "utilisateur2",
      "project": 1,
      "created_time": "2023-10-01T12:00:00Z"
    }
    ```

- **Lister les contributeurs :**

  - **URL :** `/api/projects/{project_id}/contributors/`
  - **Méthode :** GET
  - **Réponse :**
    ```json
    [
      {
        "id": 1,
        "user": 2,
        "username": "utilisateur2",
        "project": 1,
        "created_time": "2023-10-01T12:00:00Z"
      }
    ]
    ```

- **Supprimer un contributeur (auteur uniquement) :**

  - **URL :** `/api/projects/{project_id}/contributors/{id}/`
  - **Méthode :** DELETE
  - **Réponse :**
    ```json
    {
      "status": "success",
      "message": "Contributeur supprimé avec succès"
    }
    ```

### Issues

- **Créer une issue (contributeur uniquement) :**

  - **URL :** `/api/projects/{project_id}/issues/`
  - **Méthode :** POST
  - **Données requises :**
    ```json
    {
      "title": "Nouvelle Issue",
      "description": "Description de l'issue",
      "priority": "HIGH",
      "tag": "BUG",
      "status": "To Do"
    }
    ```
  - **Réponse :**
    ```json
    {
      "id": 1,
      "title": "Nouvelle Issue",
      "description": "Description de l'issue",
      "priority": "HIGH",
      "tag": "BUG",
      "status": "To Do",
      "project": 1,
      "author": 1,
      "author_username": "utilisateur1",
      "assignee": null,
      "assignee_username": null,
      "created_time": "2023-10-01T12:00:00Z"
    }
    ```

- **Lister les issues :**

  - **URL :** `/api/projects/{project_id}/issues/`
  - **Méthode :** GET
  - **Réponse :**
    ```json
    [
      {
        "id": 1,
        "title": "Issue 1",
        "description": "Description de l'issue 1",
        "priority": "MEDIUM",
        "tag": "FEATURE",
        "status": "In Progress",
        "project": 1,
        "author": 1,
        "author_username": "utilisateur1",
        "assignee": 2,
        "assignee_username": "utilisateur2",
        "created_time": "2023-10-01T12:00:00Z"
      }
    ]
    ```

- **Mettre à jour une issue (auteur uniquement) :**

  - **URL :** `/api/projects/{project_id}/issues/{id}/`
  - **Méthode :** PATCH
  - **Données requises :**
    ```json
    {
      "status": "Finished"
    }
    ```
  - **Réponse :**
    ```json
    {
      "id": 1,
      "title": "Issue 1",
      "description": "Description de l'issue 1",
      "priority": "MEDIUM",
      "tag": "FEATURE",
      "status": "Finished",
      "project": 1,
      "author": 1,
      "author_username": "utilisateur1",
      "assignee": 2,
      "assignee_username": "utilisateur2",
      "created_time": "2023-10-01T12:00:00Z"
    }
    ```

- **Supprimer une issue (auteur uniquement) :**

  - **URL :** `/api/projects/{project_id}/issues/{id}/`
  - **Méthode :** DELETE
  - **Réponse :**
    ```json
    {
      "status": "success",
      "message": "Issue supprimée avec succès"
    }
    ```

### Commentaires

- **Créer un commentaire (contributeur uniquement) :**

  - **URL :** `/api/projects/{project_id}/issues/{issue_id}/comments/`
  - **Méthode :** POST
  - **Données requises :**
    ```json
    {
      "description": "Nouveau commentaire"
    }
    ```
  - **Réponse :**
    ```json
    {
      "id": 1,
      "description": "Nouveau commentaire",
      "author": 1,
      "issue": 1,
      "created_time": "2023-10-01T12:00:00Z"
    }
    ```

- **Lister les commentaires :**

  - **URL :** `/api/projects/{project_id}/issues/{issue_id}/comments/`
  - **Méthode :** GET
  - **Réponse :**
    ```json
    [
      {
        "id": 1,
        "description": "Commentaire 1",
        "author": 1,
        "issue": 1,
        "created_time": "2023-10-01T12:00:00Z"
      }
    ]
    ```

- **Mettre à jour un commentaire (auteur uniquement) :**

  - **URL :** `/api/projects/{project_id}/issues/{issue_id}/comments/{id}/`
  - **Méthode :** PUT
  - **Données requises :**
    ```json
    {
      "description": "Commentaire modifié"
    }
    ```
  - **Réponse :**
    ```json
    {
      "id": 1,
      "description": "Commentaire modifié",
      "author": 1,
      "issue": 1,
      "created_time": "2023-10-01T12:00:00Z"
    }
    ```

- **Supprimer un commentaire (auteur uniquement) :**

  - **URL :** `/api/projects/{project_id}/issues/{issue_id}/comments/{id}/`
  - **Méthode :** DELETE
  - **Réponse :**
    ```json
    {
      "status": "success",
      "message": "Commentaire supprimé avec succès"
    }
    ```

## Système de permissions

- **Utilisateurs :** 
  - Création : Ouvert à tous
  - Liste : Administrateurs uniquement
  - Mise à jour/Suppression : Propriétaire ou administrateur

- **Projets :**
  - Création : Authentifié
  - Liste : Authentifié et contributeur
  - Mise à jour/Suppression : Auteur uniquement

- **Contributeurs :**
  - Ajout/Suppression : Auteur du projet uniquement
  - Liste : Authentifié et contributeur

- **Issues :**
  - Création : Contributeur du projet
  - Liste : Contributeur du projet
  - Mise à jour/Suppression : Auteur de l'issue

- **Commentaires :**
  - Création : Contributeur du projet
  - Liste : Contributeur du projet
  - Mise à jour/Suppression : Auteur du commentaire
