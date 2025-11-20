@echo off
chcp 65001 >nul
title Wolof Njaay Neena - Installation

echo ╔════════════════════════════════════════════════════════════╗
echo ║  📱 Wolof Njaay Neena - Application Mobile                ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Vérifier Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python n'est pas installé ou pas dans le PATH
    echo.
    echo Téléchargez Python depuis : https://www.python.org/downloads/
    echo Cochez "Add Python to PATH" pendant l'installation
    pause
    exit /b 1
)

echo ✅ Python détecté
python --version
echo.

REM Vérifier pip
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip n'est pas disponible
    pause
    exit /b 1
)

echo ✅ pip détecté
echo.

echo ╔════════════════════════════════════════════════════════════╗
echo ║  Installation des dépendances Python                      ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

echo 📦 Installation de Kivy...
pip install kivy pillow
if %errorlevel% neq 0 (
    echo ❌ Erreur lors de l'installation de Kivy
    pause
    exit /b 1
)

echo ✅ Kivy installé avec succès
echo.

echo ╔════════════════════════════════════════════════════════════╗
echo ║  Téléchargement des citations complètes                   ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

set /p download="Télécharger les 2644 citations depuis GitHub ? (O/N) : "
if /i "%download%"=="O" (
    echo 📥 Téléchargement en cours...
    python import_citations.py
    if %errorlevel% neq 0 (
        echo ⚠️  Erreur lors du téléchargement
        echo    Vous pouvez continuer avec les 10 citations d'exemple
        echo.
    )
)

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  Tests de l'application                                   ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

echo 🧪 Exécution des tests...
python test.py
echo.

echo ╔════════════════════════════════════════════════════════════╗
echo ║  Lancement de l'application                                ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

set /p launch="Lancer l'application maintenant ? (O/N) : "
if /i "%launch%"=="O" (
    echo 🚀 Lancement de l'application...
    echo.
    python main.py
)

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  📱 Compilation Android (APK)                              ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo ⚠️  IMPORTANT : Buildozer ne fonctionne pas nativement sur Windows
echo.
echo 🪟 Solutions pour compiler l'APK :
echo.
echo   1. WSL (Windows Subsystem for Linux) - RECOMMANDÉ
echo      • Installer : wsl --install
echo      • Suivre le guide : WINDOWS-BUILDOZER.md
echo.
echo   2. Google Colab (en ligne, gratuit)
echo      • Ouvrir : https://colab.research.google.com/
echo      • Copier le contenu de : colab-build-apk.py
echo.
echo   3. Machine virtuelle Linux
echo      • Installer VirtualBox + Ubuntu
echo      • Suivre les instructions Linux normales
echo.
echo 📖 Consultez WINDOWS-BUILDOZER.md pour plus de détails
echo.

pause

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  ✨ Installation terminée !                                ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 📚 Commandes utiles :
echo.
echo   • python main.py              - Lancer l'application
echo   • python test.py              - Tester l'installation
echo   • python import_citations.py  - Importer citations complètes
echo.
echo 🔧 Pour compiler l'APK :
echo   • Suivez WINDOWS-BUILDOZER.md
echo.
echo Jërëjëf ! (Merci) 🇸🇳
echo.

pause
