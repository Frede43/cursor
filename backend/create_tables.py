#!/usr/bin/env python
"""
Script pour créer des tables de test dans la base de données
"""

import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apps.settings.development')
django.setup()

from sales.models import Table

def create_tables():
    """Créer des tables de test"""
    
    tables_data = [
        {'number': '1', 'capacity': 2, 'location': 'Terrasse'},
        {'number': '2', 'capacity': 4, 'location': 'Salle principale'},
        {'number': '3', 'capacity': 4, 'location': 'Salle principale'},
        {'number': '4', 'capacity': 6, 'location': 'Salle VIP'},
        {'number': '5', 'capacity': 2, 'location': 'Bar'},
        {'number': '6', 'capacity': 8, 'location': 'Salle de groupe'},
        {'number': '7', 'capacity': 4, 'location': 'Terrasse'},
        {'number': '8', 'capacity': 2, 'location': 'Bar'},
        {'number': '9', 'capacity': 6, 'location': 'Salle principale'},
        {'number': '10', 'capacity': 4, 'location': 'Salle principale'},
    ]
    
    print("🏪 Création des tables...")
    
    for table_data in tables_data:
        table, created = Table.objects.get_or_create(
            number=table_data['number'],
            defaults={
                'capacity': table_data['capacity'],
                'location': table_data['location'],
                'status': 'available',
                'is_active': True
            }
        )
        
        if created:
            print(f"✅ Table {table.number} créée - Capacité: {table.capacity}, Lieu: {table.location}")
        else:
            print(f"ℹ️  Table {table.number} existe déjà")
    
    # Vérifier le nombre total de tables
    total_tables = Table.objects.count()
    active_tables = Table.objects.filter(is_active=True).count()
    
    print(f"\n📊 Résumé:")
    print(f"   Total tables: {total_tables}")
    print(f"   Tables actives: {active_tables}")
    
    # Afficher les tables par statut
    for status, status_display in Table.STATUS_CHOICES:
        count = Table.objects.filter(status=status).count()
        if count > 0:
            print(f"   {status_display}: {count}")

if __name__ == '__main__':
    create_tables()
