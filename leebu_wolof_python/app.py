#!/usr/bin/env python3
"""
Application Flask pour Leebu Wolof - Citations quotidiennes
"""

from flask import Flask, render_template, jsonify, request, send_file
import json
import random
import sqlite3
from datetime import datetime
from pathlib import Path
import io
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)
app.config['SECRET_KEY'] = 'leebu-wolof-secret-key-2024'

# Chemins
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / 'data'
DB_PATH = DATA_DIR / 'leebu.db'
CITATIONS_PATH = DATA_DIR / 'leebu_citations_COMPLET.json'

# Charger les citations
with open(CITATIONS_PATH, 'r', encoding='utf-8') as f:
    CITATIONS = json.load(f)

def init_db():
    """Initialiser la base de données SQLite"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Table pour suivre les citations affichées
    c.execute('''CREATE TABLE IF NOT EXISTS citations_vues
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  numero INTEGER UNIQUE,
                  date_vue TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Table pour la configuration
    c.execute('''CREATE TABLE IF NOT EXISTS config
                 (cle TEXT PRIMARY KEY,
                  valeur TEXT)''')
    
    conn.commit()
    conn.close()

def get_citation_aleatoire():
    """
    Récupère une citation aléatoire non encore vue.
    Si toutes les citations ont été vues, réinitialise et recommence.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Récupérer les numéros déjà vus
    c.execute('SELECT numero FROM citations_vues')
    vues = set(row[0] for row in c.fetchall())
    
    # Trouver les citations non vues
    non_vues = [cit for cit in CITATIONS if cit['numero'] not in vues]
    
    # Si toutes les citations ont été vues, réinitialiser
    if not non_vues:
        c.execute('DELETE FROM citations_vues')
        conn.commit()
        non_vues = CITATIONS.copy()
    
    # Choisir une citation aléatoire
    citation = random.choice(non_vues)
    
    # Marquer comme vue
    c.execute('INSERT OR IGNORE INTO citations_vues (numero) VALUES (?)', 
              (citation['numero'],))
    conn.commit()
    conn.close()
    
    return citation

def get_stats():
    """Récupère les statistiques des citations vues"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('SELECT COUNT(*) FROM citations_vues')
    vues = c.fetchone()[0]
    
    conn.close()
    
    return {
        'vues': vues,
        'total': len(CITATIONS),
        'restantes': len(CITATIONS) - vues
    }

def format_date_fr():
    """Formate la date en français"""
    jours = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    mois = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
            'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
    
    maintenant = datetime.now()
    jour = jours[maintenant.weekday()]
    return f"{jour} {maintenant.day} {mois[maintenant.month - 1]} {maintenant.year}"

@app.route('/')
def index():
    """Page d'accueil avec citation aléatoire"""
    citation = get_citation_aleatoire()
    stats = get_stats()
    date_fr = format_date_fr()
    
    return render_template('index.html', 
                         citation=citation,
                         stats=stats,
                         date_fr=date_fr)

@app.route('/toutes-citations')
def toutes_citations():
    """Page avec toutes les citations"""
    # Trier par numéro
    citations_triees = sorted(CITATIONS, key=lambda x: x['numero'])
    return render_template('toutes_citations.html', 
                         citations=citations_triees,
                         total=len(CITATIONS))

@app.route('/api/nouvelle-citation')
def nouvelle_citation():
    """API pour obtenir une nouvelle citation"""
    citation = get_citation_aleatoire()
    stats = get_stats()
    date_fr = format_date_fr()
    
    return jsonify({
        'citation': citation,
        'stats': stats,
        'date_fr': date_fr
    })

@app.route('/api/reset')
def reset_citations():
    """Réinitialiser les citations vues"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM citations_vues')
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Citations réinitialisées'})

@app.route('/api/stats')
def api_stats():
    """API pour obtenir les statistiques"""
    return jsonify(get_stats())

if __name__ == '__main__':
    # Initialiser la base de données
    init_db()
    
    # Lancer l'application
    print("🚀 Lancement de Leebu Wolof...")
    print(f"📊 {len(CITATIONS)} citations chargées")
    app.run(host='0.0.0.0', port=5000, debug=True)
