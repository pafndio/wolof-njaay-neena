# Leebu Wolof - Application Python Flask

Application web pour afficher des citations wolof quotidiennes avec un système de suivi intelligent.

## Fonctionnalités

### 🎯 Page d'accueil
- **Citations aléatoires sans répétition** : Chaque citation est unique jusqu'à ce que toutes aient été vues
- **Réinitialisation automatique** : La boucle recommence automatiquement après avoir vu toutes les citations
- **Statistiques en temps réel** : Nombre de citations vues et restantes
- **Affiche avec design africain** : Motifs Kente authentiques avec bordures colorées
- **Texte d'introduction** : "Wolof njaay neena tay + date du jour" en gras
- **4 actions** : Nouvelle citation, Télécharger, Copier, Partager

### 📚 Page "Toutes les citations"
- **Liste complète** : Accès à toutes les 2644 citations
- **Recherche** : Filtrage en temps réel
- **Copie rapide** : Bouton pour copier chaque citation
- **Design en grille** : Affichage responsive

### 💾 Base de données SQLite
- Suivi des citations déjà vues
- Persistance des données entre les sessions
- Réinitialisation manuelle possible

## Installation

```bash
# Installer les dépendances
pip3 install -r requirements.txt

# Lancer l'application
python3 app.py
```

L'application sera accessible sur `http://localhost:5000`

## Structure du projet

```
leebu_wolof_python/
├── app.py                      # Application Flask principale
├── requirements.txt            # Dépendances Python
├── README.md                   # Documentation
├── data/
│   ├── leebu_citations_COMPLET.json  # 2644 citations wolof
│   └── leebu.db               # Base de données SQLite (créée automatiquement)
├── templates/
│   ├── base.html              # Template de base
│   ├── index.html             # Page d'accueil
│   └── toutes_citations.html  # Page toutes les citations
└── static/
    ├── css/
    │   └── style.css          # Styles CSS
    ├── js/
    │   └── main.js            # JavaScript
    └── images/
        └── kente_pattern_*.jpg # Motifs africains
```

## Technologies utilisées

- **Backend** : Python 3.11, Flask 3.0
- **Base de données** : SQLite3
- **Frontend** : HTML5, CSS3, JavaScript
- **Design** : Poppins (Google Fonts), Font Awesome
- **Capture d'image** : html2canvas

## API Endpoints

- `GET /` : Page d'accueil avec citation aléatoire
- `GET /toutes-citations` : Page avec toutes les citations
- `GET /api/nouvelle-citation` : Obtenir une nouvelle citation (JSON)
- `GET /api/stats` : Obtenir les statistiques (JSON)
- `GET /api/reset` : Réinitialiser les citations vues (JSON)

## Auteur

Développé pour préserver et partager les proverbes wolof du Sénégal.

## Licence

© 2024 Leebu Wolof - Tous droits réservés
