#!/usr/bin/env python
"""
Script simple pour créer des tables via Django shell
"""

import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstockwise.settings')
django.setup()

from sales.models import Table

def create_sample_tables():
    """Créer des tables d'exemple"""
    
    tables_to_create = [
        {'number': '1', 'capacity': 2, 'location': 'Terrasse', 'status': 'available'},
        {'number': '2', 'capacity': 4, 'location': 'Salle principale', 'status': 'available'},
        {'number': '3', 'capacity': 4, 'location': 'Salle principale', 'status': 'available'},
        {'number': '4', 'capacity': 6, 'location': 'Salle VIP', 'status': 'available'},
        {'number': '5', 'capacity': 2, 'location': 'Bar', 'status': 'available'},
        {'number': '6', 'capacity': 8, 'location': 'Salle de groupe', 'status': 'available'},
        {'number': '7', 'capacity': 4, 'location': 'Terrasse', 'status': 'available'},
        {'number': '8', 'capacity': 2, 'location': 'Bar', 'status': 'available'},
    ]
    
    print("🏪 Création des tables d'exemple...")
    
    created_count = 0
    existing_count = 0
    
    for table_data in tables_to_create:
        table, created = Table.objects.get_or_create(
            number=table_data['number'],
            defaults={
                'capacity': table_data['capacity'],
                'location': table_data['location'],
                'status': table_data['status'],
                'is_active': True
            }
        )
        
        if created:
            print(f"✅ Table {table.number} créée - {table.capacity} places ({table.location})")
            created_count += 1
        else:
            print(f"ℹ️  Table {table.number} existe déjà")
            existing_count += 1
    
    # Statistiques finales
    total_tables = Table.objects.count()
    active_tables = Table.objects.filter(is_active=True).count()
    
    print(f"\n📊 Résumé:")
    print(f"   Tables créées: {created_count}")
    print(f"   Tables existantes: {existing_count}")
    print(f"   Total en base: {total_tables}")
    print(f"   Tables actives: {active_tables}")
    
    # Affichage par statut
    print(f"\n📋 Tables par statut:")
    for status_code, status_name in Table.STATUS_CHOICES:
        count = Table.objects.filter(status=status_code).count()
        if count > 0:
            print(f"   {status_name}: {count}")
    
    print(f"\n🎯 Les tables sont maintenant disponibles dans l'admin Django!")

if __name__ == '__main__':
    try:
        create_sample_tables()
    except Exception as e:
        print(f"❌ Erreur: {e}")
