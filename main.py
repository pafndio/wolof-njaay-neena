#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wolof Njaay Neena - Application Mobile
Application de citations wolof quotidiennes avec suivi intelligent
"""

import json
import sqlite3
import random
from datetime import datetime
from pathlib import Path

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.metrics import dp
from kivy.utils import platform

# Gestion des permissions Android
if platform == 'android':
    from android.permissions import request_permissions, Permission
    from android.storage import primary_external_storage_path
    from jnius import autoclass
    
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Intent = autoclass('android.content.Intent')
    String = autoclass('java.lang.String')
    Uri = autoclass('android.net.Uri')


class Database:
    """Gestion de la base de données SQLite"""
    
    def __init__(self, db_path='data/leebu.db'):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialiser la base de données"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS citations_vues (
                id INTEGER PRIMARY KEY,
                date_vue TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def marquer_vue(self, citation_id):
        """Marquer une citation comme vue"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO citations_vues (id, date_vue)
            VALUES (?, ?)
        ''', (citation_id, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def get_citations_vues(self):
        """Obtenir la liste des IDs des citations vues"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM citations_vues')
        vues = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        return vues
    
    def reset_citations(self):
        """Réinitialiser toutes les citations vues"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM citations_vues')
        
        conn.commit()
        conn.close()
    
    def get_count_vues(self):
        """Obtenir le nombre de citations vues"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM citations_vues')
        count = cursor.fetchone()[0]
        
        conn.close()
        return count


class CitationManager:
    """Gestionnaire des citations wolof"""
    
    def __init__(self, json_path='data/leebu_citations_COMPLET.json'):
        self.json_path = json_path
        self.citations = self.load_citations()
        self.db = Database()
    
    def load_citations(self):
        """Charger les citations depuis le fichier JSON"""
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Fichier {self.json_path} non trouvé")
            return []
    
    def get_citation_aleatoire(self):
        """Obtenir une citation aléatoire non vue"""
        vues = self.db.get_citations_vues()
        non_vues = [c for c in self.citations if c['id'] not in vues]
        
        # Si toutes les citations ont été vues, réinitialiser
        if not non_vues:
            self.db.reset_citations()
            non_vues = self.citations
        
        if non_vues:
            citation = random.choice(non_vues)
            self.db.marquer_vue(citation['id'])
            return citation
        
        return None
    
    def get_stats(self):
        """Obtenir les statistiques"""
        vues = self.db.get_count_vues()
        total = len(self.citations)
        restantes = total - vues
        
        return {
            'vues': vues,
            'total': total,
            'restantes': restantes
        }
    
    def reset(self):
        """Réinitialiser les citations vues"""
        self.db.reset_citations()
    
    def search_citations(self, query):
        """Rechercher des citations"""
        query = query.lower()
        results = []
        
        for citation in self.citations:
            if query in citation['citation'].lower() or query in citation.get('traduction', '').lower():
                results.append(citation)
        
        return results


class AccueilScreen(Screen):
    """Écran d'accueil avec citation du jour"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.citation_manager = None
        self.current_citation = None
        self.build_ui()
    
    def build_ui(self):
        """Construire l'interface"""
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Définir le fond avec un dégradé (simulé avec une couleur unie)
        with layout.canvas.before:
            Color(0.95, 0.85, 0.7, 1)  # Couleur beige/crème
            self.rect = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=self.update_rect, size=self.update_rect)
        
        # Titre
        titre = Label(
            text='[b]Wolof Njaay Neena[/b]',
            markup=True,
            font_size='28sp',
            size_hint_y=None,
            height=dp(50),
            color=(0.2, 0.3, 0.1, 1)
        )
        layout.add_widget(titre)
        
        # Date du jour
        today = datetime.now().strftime('%A %d %B %Y')
        self.date_label = Label(
            text=f'[b]{today}[/b]',
            markup=True,
            font_size='16sp',
            size_hint_y=None,
            height=dp(30),
            color=(0.3, 0.3, 0.3, 1)
        )
        layout.add_widget(self.date_label)
        
        # Conteneur de la citation avec bordure
        citation_container = BoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(10),
            size_hint_y=0.5
        )
        
        with citation_container.canvas.before:
            Color(1, 0.98, 0.9, 1)  # Fond clair
            self.citation_rect = RoundedRectangle(
                pos=citation_container.pos,
                size=citation_container.size,
                radius=[dp(15)]
            )
            Color(0.8, 0.5, 0.2, 1)  # Bordure orange/marron
            self.citation_border = RoundedRectangle(
                pos=citation_container.pos,
                size=citation_container.size,
                radius=[dp(15)]
            )
        citation_container.bind(pos=self.update_citation_rect, size=self.update_citation_rect)
        
        # Texte de la citation
        self.citation_label = Label(
            text='',
            markup=True,
            font_size='20sp',
            color=(0.1, 0.1, 0.1, 1),
            halign='center',
            valign='middle',
            text_size=(None, None)
        )
        self.citation_label.bind(size=self.update_text_size)
        citation_container.add_widget(self.citation_label)
        
        # Traduction
        self.traduction_label = Label(
            text='',
            markup=True,
            font_size='16sp',
            color=(0.3, 0.3, 0.3, 1),
            italic=True,
            halign='center',
            valign='middle',
            text_size=(None, None)
        )
        self.traduction_label.bind(size=self.update_text_size_trad)
        citation_container.add_widget(self.traduction_label)
        
        layout.add_widget(citation_container)
        
        # Statistiques
        self.stats_label = Label(
            text='',
            font_size='14sp',
            size_hint_y=None,
            height=dp(30),
            color=(0.4, 0.4, 0.4, 1)
        )
        layout.add_widget(self.stats_label)
        
        # Boutons d'action
        actions_layout = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(120))
        
        btn_nouvelle = Button(
            text='Nouvelle Citation',
            font_size='16sp',
            background_color=(0.2, 0.6, 0.3, 1),
            background_normal=''
        )
        btn_nouvelle.bind(on_press=self.nouvelle_citation)
        
        btn_copier = Button(
            text='Copier',
            font_size='16sp',
            background_color=(0.3, 0.5, 0.7, 1),
            background_normal=''
        )
        btn_copier.bind(on_press=self.copier_citation)
        
        btn_partager = Button(
            text='Partager',
            font_size='16sp',
            background_color=(0.8, 0.5, 0.2, 1),
            background_normal=''
        )
        btn_partager.bind(on_press=self.partager_citation)
        
        btn_liste = Button(
            text='Toutes les Citations',
            font_size='16sp',
            background_color=(0.5, 0.3, 0.6, 1),
            background_normal=''
        )
        btn_liste.bind(on_press=self.voir_liste)
        
        actions_layout.add_widget(btn_nouvelle)
        actions_layout.add_widget(btn_copier)
        actions_layout.add_widget(btn_partager)
        actions_layout.add_widget(btn_liste)
        
        layout.add_widget(actions_layout)
        
        # Bouton reset (petit)
        btn_reset = Button(
            text='Réinitialiser',
            size_hint_y=None,
            height=dp(40),
            font_size='14sp',
            background_color=(0.8, 0.3, 0.3, 1),
            background_normal=''
        )
        btn_reset.bind(on_press=self.reset_citations)
        layout.add_widget(btn_reset)
        
        self.add_widget(layout)
    
    def update_rect(self, *args):
        """Mettre à jour le rectangle de fond"""
        self.rect.pos = self.parent.pos if self.parent else (0, 0)
        self.rect.size = self.parent.size if self.parent else Window.size
    
    def update_citation_rect(self, instance, value):
        """Mettre à jour le rectangle de la citation"""
        self.citation_border.pos = (instance.x - dp(3), instance.y - dp(3))
        self.citation_border.size = (instance.width + dp(6), instance.height + dp(6))
        self.citation_rect.pos = instance.pos
        self.citation_rect.size = instance.size
    
    def update_text_size(self, instance, value):
        """Mettre à jour la taille du texte de la citation"""
        instance.text_size = (instance.width - dp(20), None)
    
    def update_text_size_trad(self, instance, value):
        """Mettre à jour la taille du texte de la traduction"""
        instance.text_size = (instance.width - dp(20), None)
    
    def on_enter(self):
        """Appelé quand l'écran devient actif"""
        if not self.current_citation:
            self.charger_citation()
    
    def charger_citation(self):
        """Charger une nouvelle citation"""
        if self.citation_manager:
            citation = self.citation_manager.get_citation_aleatoire()
            if citation:
                self.current_citation = citation
                self.citation_label.text = f'[b]{citation["citation"]}[/b]'
                self.traduction_label.text = f'[i]{citation.get("traduction", "")}[/i]'
                self.update_stats()
    
    def update_stats(self):
        """Mettre à jour les statistiques"""
        if self.citation_manager:
            stats = self.citation_manager.get_stats()
            self.stats_label.text = f'Citations vues: {stats["vues"]}/{stats["total"]} | Restantes: {stats["restantes"]}'
    
    def nouvelle_citation(self, instance):
        """Obtenir une nouvelle citation"""
        self.charger_citation()
    
    def copier_citation(self, instance):
        """Copier la citation dans le presse-papier"""
        if self.current_citation:
            text = f"{self.current_citation['citation']}\n{self.current_citation.get('traduction', '')}"
            Clipboard.copy(text)
            self.show_popup('Succès', 'Citation copiée !')
    
    def partager_citation(self, instance):
        """Partager la citation"""
        if not self.current_citation:
            return
        
        text = f"{self.current_citation['citation']}\n\n{self.current_citation.get('traduction', '')}\n\n- Wolof Njaay Neena"
        
        if platform == 'android':
            try:
                intent = Intent()
                intent.setAction(Intent.ACTION_SEND)
                intent.putExtra(Intent.EXTRA_TEXT, String(text))
                intent.setType('text/plain')
                
                chooser = Intent.createChooser(intent, String('Partager via'))
                PythonActivity.mActivity.startActivity(chooser)
            except Exception as e:
                self.show_popup('Erreur', f'Impossible de partager: {str(e)}')
        else:
            Clipboard.copy(text)
            self.show_popup('Info', 'Citation copiée pour partage !')
    
    def voir_liste(self, instance):
        """Aller à la liste complète"""
        self.manager.current = 'liste'
    
    def reset_citations(self, instance):
        """Réinitialiser les citations vues"""
        if self.citation_manager:
            self.citation_manager.reset()
            self.update_stats()
            self.show_popup('Succès', 'Citations réinitialisées !')
    
    def show_popup(self, title, message):
        """Afficher un popup"""
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        content.add_widget(Label(text=message))
        
        btn_close = Button(text='OK', size_hint_y=None, height=dp(50))
        content.add_widget(btn_close)
        
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.3)
        )
        btn_close.bind(on_press=popup.dismiss)
        popup.open()


class ListeScreen(Screen):
    """Écran de liste de toutes les citations"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.citation_manager = None
        self.build_ui()
    
    def build_ui(self):
        """Construire l'interface"""
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # En-tête
        header = BoxLayout(size_hint_y=None, height=dp(100), spacing=dp(10))
        
        # Bouton retour
        btn_retour = Button(
            text='← Retour',
            size_hint_x=0.3,
            background_color=(0.3, 0.5, 0.7, 1),
            background_normal=''
        )
        btn_retour.bind(on_press=self.retour_accueil)
        header.add_widget(btn_retour)
        
        # Barre de recherche
        search_layout = BoxLayout(orientation='vertical', spacing=dp(5))
        search_layout.add_widget(Label(text='Rechercher:', size_hint_y=0.3, font_size='14sp'))
        
        self.search_input = TextInput(
            hint_text='Tapez pour rechercher...',
            multiline=False,
            size_hint_y=0.7
        )
        self.search_input.bind(text=self.on_search)
        search_layout.add_widget(self.search_input)
        
        header.add_widget(search_layout)
        layout.add_widget(header)
        
        # Liste des citations
        self.scroll_view = ScrollView()
        self.citations_layout = GridLayout(
            cols=1,
            spacing=dp(10),
            size_hint_y=None,
            padding=dp(5)
        )
        self.citations_layout.bind(minimum_height=self.citations_layout.setter('height'))
        
        self.scroll_view.add_widget(self.citations_layout)
        layout.add_widget(self.scroll_view)
        
        self.add_widget(layout)
    
    def on_enter(self):
        """Appelé quand l'écran devient actif"""
        self.afficher_citations()
    
    def afficher_citations(self, citations=None):
        """Afficher les citations"""
        self.citations_layout.clear_widgets()
        
        if self.citation_manager:
            if citations is None:
                citations = self.citation_manager.citations
            
            for citation in citations:
                item = self.create_citation_item(citation)
                self.citations_layout.add_widget(item)
    
    def create_citation_item(self, citation):
        """Créer un widget pour une citation"""
        item = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(100),
            padding=dp(10),
            spacing=dp(10)
        )
        
        with item.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            rect = RoundedRectangle(pos=item.pos, size=item.size, radius=[dp(10)])
        
        def update_rect(instance, value):
            rect.pos = instance.pos
            rect.size = instance.size
        
        item.bind(pos=update_rect, size=update_rect)
        
        # Texte de la citation
        text_layout = BoxLayout(orientation='vertical')
        
        citation_label = Label(
            text=f'[b]{citation["citation"]}[/b]',
            markup=True,
            font_size='16sp',
            color=(0.1, 0.1, 0.1, 1),
            size_hint_y=0.6,
            halign='left',
            valign='middle'
        )
        citation_label.bind(size=lambda i, v: setattr(i, 'text_size', (i.width, None)))
        
        trad_label = Label(
            text=f'[i]{citation.get("traduction", "")}[/i]',
            markup=True,
            font_size='14sp',
            color=(0.4, 0.4, 0.4, 1),
            size_hint_y=0.4,
            halign='left',
            valign='middle'
        )
        trad_label.bind(size=lambda i, v: setattr(i, 'text_size', (i.width, None)))
        
        text_layout.add_widget(citation_label)
        text_layout.add_widget(trad_label)
        
        item.add_widget(text_layout)
        
        # Bouton copier
        btn_copy = Button(
            text='Copier',
            size_hint_x=0.25,
            background_color=(0.3, 0.6, 0.4, 1),
            background_normal=''
        )
        btn_copy.bind(on_press=lambda x: self.copier_citation(citation))
        item.add_widget(btn_copy)
        
        return item
    
    def copier_citation(self, citation):
        """Copier une citation"""
        text = f"{citation['citation']}\n{citation.get('traduction', '')}"
        Clipboard.copy(text)
    
    def on_search(self, instance, value):
        """Rechercher des citations"""
        if self.citation_manager:
            if value.strip():
                results = self.citation_manager.search_citations(value)
                self.afficher_citations(results)
            else:
                self.afficher_citations()
    
    def retour_accueil(self, instance):
        """Retourner à l'accueil"""
        self.manager.current = 'accueil'


class WolofNjaayApp(App):
    """Application principale"""
    
    def build(self):
        """Construire l'application"""
        # Demander les permissions Android
        if platform == 'android':
            request_permissions([
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE
            ])
        
        # Gestionnaire d'écrans
        sm = ScreenManager(transition=SlideTransition())
        
        # Initialiser le gestionnaire de citations
        citation_manager = CitationManager()
        
        # Écran d'accueil
        accueil = AccueilScreen(name='accueil')
        accueil.citation_manager = citation_manager
        sm.add_widget(accueil)
        
        # Écran de liste
        liste = ListeScreen(name='liste')
        liste.citation_manager = citation_manager
        sm.add_widget(liste)
        
        return sm


if __name__ == '__main__':
    WolofNjaayApp().run()
