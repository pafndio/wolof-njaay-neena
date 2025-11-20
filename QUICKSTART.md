# 🚀 Guide de Démarrage Rapide

## Installation en 3 étapes

### 1️⃣ Installer les dépendances

```bash
# Donner les droits d'exécution
chmod +x install.sh

# Lancer l'installation automatique
./install.sh
```

### 2️⃣ Importer les citations complètes (optionnel)

```bash
# Télécharger les 2644 citations depuis GitHub
python3 import_citations.py
```

### 3️⃣ Tester l'application

```bash
# Tester l'installation
python3 test.py

# Lancer l'application
python3 main.py
```

## 📱 Compiler pour Android

```bash
# Installer buildozer (première fois uniquement)
pip3 install buildozer

# Compiler l'APK
buildozer android debug

# Le fichier APK sera dans le dossier bin/
```

## ⚡ Commandes rapides

| Commande | Description |
|----------|-------------|
| `python3 main.py` | Lancer l'application |
| `python3 test.py` | Tester l'installation |
| `python3 import_citations.py` | Importer citations complètes |
| `buildozer android debug` | Compiler APK debug |
| `buildozer android release` | Compiler APK release |
| `adb install bin/*.apk` | Installer sur téléphone |

## 🎨 Personnalisation rapide

### Changer les couleurs

Éditez `main.py`, recherchez `Color()` :

```python
# Exemple : fond beige
Color(0.95, 0.85, 0.7, 1)  # RGBA (0-1)

# Bleu : Color(0.2, 0.4, 0.8, 1)
# Vert : Color(0.2, 0.6, 0.3, 1)
```

### Ajouter vos citations

Éditez `data/citations.json` :

```json
[
  {
    "id": 1,
    "citation": "Votre proverbe wolof",
    "traduction": "Traduction française"
  }
]
```

## 🐛 Problèmes fréquents

### Kivy ne s'installe pas

```bash
# Sur Ubuntu
sudo apt-get install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev

# Réinstaller Kivy
pip3 install --upgrade kivy
```

### Buildozer échoue

```bash
# Nettoyer le cache
buildozer android clean

# Vérifier Java
java -version  # Requis : Java 17

# Réessayer
buildozer android debug
```

### L'APK ne s'installe pas

1. Activez "Sources inconnues" sur Android
2. Vérifiez que l'APK n'est pas corrompu
3. Utilisez `adb install -r bin/*.apk` pour forcer

## 📚 Ressources

- **Documentation Kivy** : https://kivy.org/doc/stable/
- **Buildozer** : https://buildozer.readthedocs.io/
- **Projet original** : https://github.com/pafndio/wolof-njaay-neena

## 💬 Support

Consultez le fichier `README.md` pour la documentation complète.

---

**Jërëjëf !** (Merci) 🇸🇳
