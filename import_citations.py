#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour télécharger les 2644 citations complètes depuis le repo GitHub
"""

import urllib.request
import json
import sys
from pathlib import Path

# URL du fichier JSON complet
URL = "https://raw.githubusercontent.com/pafndio/wolof-njaay-neena/main/data/leebu_citations_COMPLET.json"
DESTINATION = "data/citations.json"

def download_citations():
    """Télécharger les citations complètes"""
    print("📥 Téléchargement des citations complètes...")
    print(f"   Source: {URL}")
    print(f"   Destination: {DESTINATION}")
    print()
    
    try:
        # Télécharger le fichier
        with urllib.request.urlopen(URL) as response:
            data = response.read()
            
        # Parser le JSON pour valider
        citations = json.loads(data)
        
        print(f"✅ {len(citations)} citations téléchargées")
        
        # Créer le dossier data si nécessaire
        Path("data").mkdir(exist_ok=True)
        
        # Sauvegarder le fichier
        with open(DESTINATION, 'w', encoding='utf-8') as f:
            json.dump(citations, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Fichier sauvegardé : {DESTINATION}")
        print()
        print("🎉 Citations complètes installées avec succès !")
        print()
        print("Vous pouvez maintenant lancer l'application :")
        print("   python3 main.py")
        
        return True
        
    except urllib.error.URLError as e:
        print(f"❌ Erreur de connexion : {e}")
        print()
        print("Solutions possibles :")
        print("1. Vérifiez votre connexion Internet")
        print("2. Le repository GitHub est-il accessible ?")
        print("3. Téléchargez manuellement depuis :")
        print(f"   {URL}")
        return False
        
    except json.JSONDecodeError as e:
        print(f"❌ Erreur de format JSON : {e}")
        return False
        
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}")
        return False

def backup_current():
    """Sauvegarder le fichier actuel si existant"""
    if Path(DESTINATION).exists():
        backup_path = f"{DESTINATION}.backup"
        print(f"💾 Sauvegarde du fichier actuel vers {backup_path}")
        
        import shutil
        shutil.copy2(DESTINATION, backup_path)
        print("✅ Sauvegarde créée")
        print()

def main():
    print("=" * 60)
    print("  📖 Import des citations complètes Wolof Njaay Neena")
    print("=" * 60)
    print()
    
    # Vérifier si le fichier existe déjà
    if Path(DESTINATION).exists():
        response = input("⚠️  Un fichier citations.json existe déjà. Le remplacer ? (o/N) ")
        if response.lower() != 'o':
            print("❌ Opération annulée")
            return
        backup_current()
    
    # Télécharger
    success = download_citations()
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
