import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstock_api.settings')
django.setup()

from django.core.management.base import BaseCommand
from products.models import Product
from alerts.models import Alert

class Command(BaseCommand):
    help = 'Créer des alertes automatiques pour les stocks faibles/épuisés'

    def handle(self, *args, **options):
        # Supprimer les anciennes alertes de stock automatiques
        Alert.objects.filter(type='stock', created_by__isnull=True).delete()
        
        products = Product.objects.filter(is_active=True)
        alerts_created = 0
        
        for product in products:
            # Stock épuisé
            if product.current_stock == 0:
                Alert.objects.create(
                    type='stock',
                    priority='critical',
                    title='Stock épuisé',
                    message=f'{product.name} est en rupture de stock',
                    related_product=product,
                    created_by=None  # Alerte automatique
                )
                alerts_created += 1
                self.stdout.write(
                    self.style.ERROR(f'CRITIQUE: {product.name} - Stock épuisé')
                )
            
            # Stock faible
            elif product.current_stock <= product.minimum_stock:
                Alert.objects.create(
                    type='stock',
                    priority='high',
                    title='Stock critique',
                    message=f'{product.name}: {product.current_stock} unité{"s" if product.current_stock > 1 else ""} restante{"s" if product.current_stock > 1 else ""}',
                    related_product=product,
                    created_by=None  # Alerte automatique
                )
                alerts_created += 1
                self.stdout.write(
                    self.style.WARNING(f'ALERTE: {product.name} - Stock faible ({product.current_stock} unités)')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'{alerts_created} alertes de stock créées avec succès')
        )
