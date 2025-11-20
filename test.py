#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier l'installation
"""

import sys
import json
from pathlib import Path

def test_python():
    """Tester la version Python"""
    print("🔍 Test Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (requis: 3.8+)")
        return False

def test_kivy():
    """Tester l'installation de Kivy"""
    print("🔍 Test Kivy...")
    try:
        import kivy
        print(f"   ✅ Kivy {kivy.__version__}")
        return True
    except ImportError:
        print("   ❌ Kivy non installé")
        print("      Installez avec: pip3 install kivy")
        return False

def test_sqlite():
    """Tester SQLite"""
    print("🔍 Test SQLite...")
    try:
        import sqlite3
        print(f"   ✅ SQLite {sqlite3.sqlite_version}")
        return True
    except ImportError:
        print("   ❌ SQLite non disponible")
        return False

def test_files():
    """Tester les fichiers nécessaires"""
    print("🔍 Test des fichiers...")
    
    required_files = [
        'main.py',
        'buildozer.spec',
        'requirements.txt',
        'data/citations.json'
    ]
    
    all_ok = True
    for file in required_files:
        if Path(file).exists():
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} manquant")
            all_ok = False
    
    return all_ok

def test_json():
    """Tester le fichier JSON"""
    print("🔍 Test des citations JSON...")
    try:
        with open('data/citations.json', 'r', encoding='utf-8') as f:
            citations = json.load(f)
        
        print(f"   ✅ {len(citations)} citations chargées")
        
        # Vérifier la structure
        if citations and isinstance(citations, list):
            first = citations[0]
            if 'id' in first and 'citation' in first:
                print(f"   ✅ Structure valide")
                print(f"   📝 Exemple: {first['citation'][:50]}...")
                return True
            else:
                print("   ❌ Structure JSON invalide")
                return False
        else:
            print("   ❌ Format JSON invalide")
            return False
            
    except FileNotFoundError:
        print("   ❌ Fichier citations.json non trouvé")
        return False
    except json.JSONDecodeError:
        print("   ❌ Erreur de format JSON")
        return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_database():
    """Tester la base de données"""
    print("🔍 Test de la base de données...")
    try:
        from main import Database
        
        # Créer une DB de test
        db = Database('test.db')
        
        # Tester l'insertion
        db.marquer_vue(1)
        vues = db.get_citations_vues()
        
        if 1 in vues:
            print("   ✅ Base de données fonctionnelle")
            
            # Nettoyer
            Path('test.db').unlink()
            return True
        else:
            print("   ❌ Problème avec la base de données")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def main():
    print("=" * 60)
    print("  🧪 Tests de l'application Wolof Njaay Neena")
    print("=" * 60)
    print()
    
    tests = [
        test_python,
        test_kivy,
        test_sqlite,
        test_files,
        test_json,
        test_database
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"   ❌ Erreur inattendue: {e}")
            results.append(False)
        print()
    
    # Résumé
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ Tous les tests réussis ({passed}/{total})")
        print()
        print("🚀 L'application est prête à être lancée !")
        print()
        print("Commandes utiles :")
        print("  • Lancer l'app:        python3 main.py")
        print("  • Compiler APK:        buildozer android debug")
        print("  • Import citations:    python3 import_citations.py")
        return 0
    else:
        print(f"❌ Tests échoués: {total - passed}/{total}")
        print()
        print("Vérifiez les erreurs ci-dessus et réinstallez si nécessaire.")
        print("Commande d'installation: ./install.sh")
        return 1

if __name__ == '__main__':
    sys.exit(main())
