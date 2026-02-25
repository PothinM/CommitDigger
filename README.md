# CommitDigger ⛏️🕵️‍♂️

**CommitDigger** est un outil OSINT en ligne de commande écrit en Python. Il permet de "creuser" dans l'historique Git et d'extraire automatiquement les adresses e-mail liées aux commits dans les repositories publics d'un utilisateur GitHub.

Dans de nombreux cas, les développeurs masquent leur e-mail sur leur profil public, mais laissent fuiter leur adresse personnelle ou professionnelle dans l'historique de leurs commits Git. Cet outil automatise la recherche et l'extraction de ces données pour faciliter vos investigations.

## ✨ Fonctionnalités

- **Scan exhaustif :** Récupère la liste de tous les dépôts publics (hors forks) d'un utilisateur cible.
- **Deep Dive :** Analyse l'historique des commits pour en extraire les e-mails de l'`author` et du `committer`.
- **Filtrage intelligent :** Ignore automatiquement les adresses générées par GitHub (ex: `noreply@github.com`).
- **Discret & Rapide :** Utilise l'API officielle de GitHub pour une extraction propre sans parser de HTML brut.

## ⚙️ Prérequis

- Python 3.x
- Un Personal Access Token (PAT) GitHub (fortement recommandé pour éviter le Rate Limiting rapide de l'API).

## 🚀 Installation

1. Clonez ce repository :
    
    ```
    git clone https://github.com/PothinM/CommitDigger.git
    cd CommitDigger
    ```
    
2. Créez un environnement virtuel (recommandé) :
    
    ```
    python3 -m venv venv
    source venv/bin/activate  # Sur Windows : venv\Scripts\activate
    ```
    
3. Installez les dépendances requises :
    
    ```
    pip install -r requirements.txt
    ```
    
4. Créez un fichier `.env` à la racine du projet et ajoutez votre token GitHub :
    
    ```
    GITHUB_TOKEN=votre_token_github_ici
    ```
    

## 🛠️ Utilisation

La syntaxe de base requiert uniquement le nom d'utilisateur (pseudo) de la cible.

```
python3 commitdigger.py <username>
```

### Options disponibles :

- `-limit` : Définit le nombre maximum de commits à analyser par repository (défaut : 20). Utile pour des scans plus profonds sur de gros projets.

### Exemples :

**Scan rapide basique (20 derniers commits par repo) :**

```
python3 commitdigger.py torvalds
```

**Scan profond (100 derniers commits par repo) :**

```
python3 commitdigger.py torvalds --limit 100
```

## ⚠️ Avertissement Légal / Éthique

Cet outil a été créé à des fins de recherche en sources ouvertes (OSINT) et de cybersécurité (Red Teaming / Pentest). L'utilisation de cet outil pour collecter des données personnelles doit se faire dans le respect des lois en vigueur dans votre pays (ex: RGPD) et des conditions d'utilisation de GitHub. L'auteur décline toute responsabilité en cas d'utilisation malveillante.
