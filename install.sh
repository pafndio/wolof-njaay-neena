#!/bin/bash
# Script d'installation rapide pour Wolof Njaay Neena Mobile

echo "🚀 Installation de Wolof Njaay Neena Mobile"
echo "==========================================="
echo ""

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé. Installez-le d'abord !"
    exit 1
fi

echo "✅ Python 3 détecté"
PYTHON_VERSION=$(python3 --version)
echo "   $PYTHON_VERSION"
echo ""

# Créer un environnement virtuel (optionnel)
read -p "Créer un environnement virtuel ? (o/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Oo]$ ]]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✅ Environnement virtuel activé"
fi

# Installer les dépendances
echo ""
echo "📥 Installation des dépendances..."
pip3 install --upgrade pip
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dépendances installées avec succès"
else
    echo "❌ Erreur lors de l'installation des dépendances"
    exit 1
fi

# Vérifier les fichiers nécessaires
echo ""
echo "📋 Vérification des fichiers..."

if [ -f "data/citations.json" ]; then
    CITATION_COUNT=$(python3 -c "import json; print(len(json.load(open('data/citations.json'))))")
    echo "✅ Fichier citations.json trouvé ($CITATION_COUNT citations)"
else
    echo "⚠️  Fichier citations.json non trouvé (10 citations d'exemple disponibles)"
fi

if [ -f "main.py" ]; then
    echo "✅ Fichier main.py trouvé"
else
    echo "❌ Fichier main.py manquant !"
    exit 1
fi

# Proposer de lancer l'application
echo ""
echo "✨ Installation terminée !"
echo ""
read -p "Lancer l'application maintenant ? (O/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    echo ""
    echo "🚀 Lancement de l'application..."
    python3 main.py
fi

echo ""
echo "📚 Pour lancer l'application plus tard :"
echo "   python3 main.py"
echo ""
echo "📱 Pour compiler en APK Android :"
echo "   buildozer android debug"
echo ""
echo "Jërëjëf ! (Merci) 🇸🇳"
