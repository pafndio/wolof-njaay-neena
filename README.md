# 📱 Wolof Njaay Neena - Application Mobile

Application mobile de citations wolof quotidiennes avec système de suivi intelligent.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![Kivy](https://img.shields.io/badge/kivy-2.3.0-orange)
![Platform](https://img.shields.io/badge/platform-Android%20%7C%20iOS-lightgrey)

## ✨ Fonctionnalités

- 📖 **Citations aléatoires** sans répétition jusqu'à avoir tout lu
- 🔄 **Réinitialisation automatique** quand toutes les citations sont vues
- 📊 **Statistiques en temps réel** (vues/restantes/total)
- 🎨 **Design africain** avec motifs inspirés du Kente
- 📋 **Copie rapide** dans le presse-papier
- 🔗 **Partage social** natif Android/iOS
- 🔍 **Recherche** dans toutes les citations
- 📱 **Interface tactile** optimisée mobile
- 💾 **Sauvegarde locale** avec SQLite

## 🚀 Installation

### Prérequis

```bash
# Python 3.8 ou supérieur
python3 --version

# Pip à jour
pip3 install --upgrade pip
```

### Installation locale (test sur ordinateur)

```bash
# Cloner le projet
git clone <votre-repo>
cd wolof-njaay-mobile

# Installer les dépendances
pip3 install -r requirements.txt

# Lancer l'application
python3 main.py
```

### 📦 Compilation Android

#### 1. Installer Buildozer

```bash
# Sur Ubuntu/Debian
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# Installer buildozer
pip3 install --user buildozer
pip3 install --user cython==0.29.36

# Ajouter au PATH (si nécessaire)
export PATH=$PATH:~/.local/bin
```

#### 2. Préparer l'environnement

```bash
cd wolof-njaay-mobile

# Initialiser buildozer (première fois uniquement)
buildozer init

# Le fichier buildozer.spec est déjà configuré !
```

#### 3. Compiler l'APK

```bash
# Mode Debug (pour tests)
buildozer android debug

# Mode Release (pour distribution)
buildozer android release

# Le fichier APK sera dans : bin/
```

#### 4. Installer sur téléphone

```bash
# Via ADB
adb install bin/*.apk

# Ou transférez le fichier APK sur votre téléphone
# et installez-le manuellement
```

### 🍎 Compilation iOS (sur Mac uniquement)

```bash
# Installer kivy-ios
pip3 install kivy-ios

# Compiler les dépendances
toolchain build kivy

# Créer le projet Xcode
toolchain create WolofNjaay <chemin-vers-votre-dossier>

# Ouvrir dans Xcode
open WolofNjaay.xcodeproj
```

## 📂 Structure du projet

```
wolof-njaay-mobile/
├── main.py                 # Application principale Kivy
├── buildozer.spec         # Configuration de compilation Android
├── requirements.txt       # Dépendances Python
├── README.md             # Documentation
├── data/
│   ├── citations.json    # Base de citations wolof
│   └── leebu.db         # Base de données SQLite (créée auto)
└── assets/
    ├── images/          # Images et icônes
    └── fonts/           # Polices personnalisées (optionnel)
```

## 🎯 Utilisation

### Ajouter vos citations

Éditez le fichier `data/citations.json` :

```json
[
  {
    "id": 1,
    "citation": "Votre proverbe en wolof",
    "traduction": "La traduction en français"
  },
  {
    "id": 2,
    "citation": "Autre proverbe",
    "traduction": "Autre traduction"
  }
]
```

**Important** : 
- Utilisez des IDs uniques pour chaque citation
- Le format JSON doit être valide
- Encodage UTF-8 obligatoire

### Remplacer par vos 2644 citations

Pour utiliser le fichier complet du projet original :

```bash
# Téléchargez le fichier depuis le repo original
wget https://raw.githubusercontent.com/pafndio/wolof-njaay-neena/main/data/leebu_citations_COMPLET.json

# Renommez-le
mv leebu_citations_COMPLET.json data/citations.json

# Ou copiez manuellement le contenu
```

### Personnalisation

#### Modifier les couleurs

Dans `main.py`, cherchez les sections avec `Color()` :

```python
# Exemple : fond de l'écran d'accueil
Color(0.95, 0.85, 0.7, 1)  # RGBA (0-1)
```

#### Modifier les polices

```python
# Dans les Labels/Buttons
font_size='20sp'  # Taille
font_name='path/to/font.ttf'  # Police personnalisée
```

#### Ajouter une icône d'application

1. Créez une icône 512x512 pixels (PNG)
2. Placez-la dans `assets/images/icon.png`
3. Décommentez dans `buildozer.spec` :

```ini
icon.filename = %(source.dir)s/assets/images/icon.png
```

#### Ajouter un splash screen

1. Créez une image 1920x1080 pixels (PNG)
2. Placez-la dans `assets/images/presplash.png`
3. Décommentez dans `buildozer.spec` :

```ini
presplash.filename = %(source.dir)s/assets/images/presplash.png
```

## 🐛 Débogage

### Problèmes courants

#### L'application ne démarre pas

```bash
# Vérifier les logs Android
adb logcat | grep python
```

#### Erreur de compilation Buildozer

```bash
# Nettoyer le cache
buildozer android clean

# Recompiler
buildozer android debug
```

#### Citations non chargées

Vérifiez :
1. Le fichier `data/citations.json` existe
2. Le format JSON est valide
3. L'encodage est UTF-8

```bash
# Valider le JSON
python3 -m json.tool data/citations.json
```

## 📱 Fonctionnalités avancées

### Gestes tactiles (à implémenter)

Pour ajouter le swipe pour changer de citation :

```python
# Dans AccueilScreen
from kivy.uix.behaviors import ButtonBehavior

# Ajouter la détection de swipe
def on_touch_move(self, touch):
    if touch.dx > 100:  # Swipe droite
        self.nouvelle_citation(None)
    return super().on_touch_move(touch)
```

### Notifications quotidiennes (à implémenter)

Utilisez `plyer` pour les notifications :

```python
from plyer import notification

def send_notification():
    notification.notify(
        title='Citation du jour',
        message='Découvrez votre citation wolof !',
        app_name='Wolof Njaay Neena'
    )
```

### Widget Android (à implémenter)

Nécessite `kivy-garden` et `android-widget`.

## 🤝 Contribution

Les contributions sont les bienvenues !

1. Forkez le projet
2. Créez votre branche (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add AmazingFeature'`)
4. Pushez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📝 TODO

- [ ] Ajouter synthèse vocale (TTS wolof)
- [ ] Implémenter les favoris
- [ ] Ajouter catégories de citations
- [ ] Mode sombre/clair
- [ ] Partage sous forme d'image
- [ ] Widget Android
- [ ] Notifications quotidiennes
- [ ] Traduction multilingue (anglais, etc.)

## 🙏 Remerciements

Projet original : [pafndio/wolof-njaay-neena](https://github.com/pafndio/wolof-njaay-neena)

Citations wolof du Sénégal pour préserver et partager notre patrimoine culturel.

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.

## 👨‍💻 Auteur

Conversion mobile Kivy - 2024

---

**Jërëjëf !** (Merci en wolof) 🇸🇳
