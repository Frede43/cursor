"""
Script rapide pour créer des tables via l'ORM Django
Exécuter avec: python manage.py shell < quick_create_tables.py
"""

from sales.models import Table

# Données des tables à créer
tables_data = [
    {'number': '1', 'capacity': 2, 'location': 'Terrasse'},
    {'number': '2', 'capacity': 4, 'location': 'Salle principale'},
    {'number': '3', 'capacity': 4, 'location': 'Salle principale'},
    {'number': '4', 'capacity': 6, 'location': 'Salle VIP'},
    {'number': '5', 'capacity': 2, 'location': 'Bar'},
    {'number': '6', 'capacity': 8, 'location': 'Salle de groupe'},
    {'number': '7', 'capacity': 4, 'location': 'Terrasse'},
    {'number': '8', 'capacity': 2, 'location': 'Bar'},
]

print("🏪 Création des tables...")

created_count = 0
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
        print(f"✅ Table {table.number} créée - {table.capacity} places ({table.location})")
        created_count += 1
    else:
        print(f"ℹ️  Table {table.number} existe déjà")

print(f"\n📊 {created_count} nouvelles tables créées")
print(f"📊 Total tables en base: {Table.objects.count()}")
print("🎯 Tables disponibles dans l'admin Django!")
