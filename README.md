# JobBoard

## À propos
JobBoard est un projet développé dans le cadre de mes études, en collaboration avec un coéquipier. Il s'agit d'une plateforme permettant la mise en relation d'employeurs et de chercheurs d'emploi.

## Structure du projet
- Front-end: SvelteKit avec Tailwind CSS
- Back-end: FastAPI avec SQLAlchemy, Pydantic et PyMySQL

## Installation
### Prérequis
- Python
- Node.js
- Un serveur MySQL

### Configuration du back-end
```bash
# Cloner le dépôt
git clone https://github.com/Onited/JobBoard.git
cd JobBoard/api

# Installer les dépendances
pip install -r requirements.txt

# Démarrer le serveur
uvicorn main:app --reload
```

### Configuration du front-end
```bash
cd JobBoard/frontend

# Installer les dépendances
npm install

# Démarrer le serveur de développement
npm run dev
```

## Tests

Les tests unitaires pour l'API sont écrits en utilisant pytest, garantissant que toutes les fonctionnalités répondent aux attentes et fonctionnent comme prévu.

Pour exécuter les tests :

```bash
cd backend
pytest
```

## Remerciements
- Un grand merci à [Allrito](https://github.com/Allrito) pour sa contribution significative au développement du front-end de ce projet.
