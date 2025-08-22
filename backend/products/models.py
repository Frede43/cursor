from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Category(models.Model):
    """
    Catégories de produits : Boissons, Plats, Snacks
    """

    CATEGORY_TYPES = [
        ('boissons', 'Boissons'),
        ('plats', 'Plats'),
        ('snacks', 'Snacks'),
    ]

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nom de la catégorie'
    )

    type = models.CharField(
        max_length=20,
        choices=CATEGORY_TYPES,
        verbose_name='Type de catégorie'
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Description'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='Actif'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de création'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Date de modification'
    )

    class Meta:
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class Product(models.Model):
    """
    Modèle pour les produits du bar-restaurant
    """

    UNIT_CHOICES = [
        ('piece', 'Pièce'),
        ('bouteille', 'Bouteille'),
        ('casier', 'Casier'),
        ('litre', 'Litre'),
        ('kg', 'Kilogramme'),
        ('portion', 'Portion'),
    ]

    name = models.CharField(
        max_length=200,
        verbose_name='Nom du produit'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Catégorie'
    )

    code = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
        verbose_name='Code produit'
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Description'
    )

    unit = models.CharField(
        max_length=20,
        choices=UNIT_CHOICES,
        default='piece',
        verbose_name='Unité de mesure'
    )

    # Prix en Francs Burundais (BIF)
    purchase_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Prix d\'achat (BIF)'
    )

    selling_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Prix de vente (BIF)'
    )

    # Stock
    initial_stock = models.PositiveIntegerField(
        default=0,
        verbose_name='Stock initial'
    )

    current_stock = models.PositiveIntegerField(
        default=0,
        verbose_name='Stock actuel'
    )

    minimum_stock = models.PositiveIntegerField(
        default=5,
        verbose_name='Stock minimum (alerte)'
    )

    # Informations pour les casiers (spécifique aux boissons)
    units_per_case = models.PositiveIntegerField(
        default=1,
        verbose_name='Unités par casier'
    )

    case_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        blank=True,
        null=True,
        verbose_name='Prix du casier (BIF)'
    )

    # Gestion des pertes
    waste_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('5.00'),
        help_text='Pourcentage de perte moyen pour ce produit',
        verbose_name='% de perte moyen'
    )

    shelf_life_days = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text='Durée de conservation en jours',
        verbose_name='Durée de conservation (jours)'
    )

    storage_temperature = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text='Température de stockage recommandée',
        verbose_name='Température de stockage'
    )

    # Statut
    is_active = models.BooleanField(
        default=True,
        verbose_name='Produit actif'
    )

    is_available = models.BooleanField(
        default=True,
        verbose_name='Disponible à la vente'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de création'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Date de modification'
    )

    class Meta:
        verbose_name = 'Produit'
        verbose_name_plural = 'Produits'
        ordering = ['category', 'name']
        unique_together = ['name', 'category']

    def __str__(self):
        return f"{self.name} - {self.category.name}"

    @property
    def profit_margin(self):
        """Calcule la marge bénéficiaire"""
        if self.purchase_price > 0:
            return self.selling_price - self.purchase_price
        return Decimal('0.00')

    @property
    def profit_percentage(self):
        """Calcule le pourcentage de marge"""
        if self.purchase_price > 0:
            return ((self.selling_price - self.purchase_price) / self.purchase_price) * 100
        return Decimal('0.00')

    @property
    def is_low_stock(self):
        """Vérifie si le stock est bas"""
        return self.current_stock <= self.minimum_stock

    @property
    def is_out_of_stock(self):
        """Vérifie si le produit est en rupture"""
        return self.current_stock == 0

    def save(self, *args, **kwargs):
        # Générer un code automatique si pas fourni
        if not self.code:
            import random
            import time

            # Générer un code unique basé sur le nom et un timestamp
            timestamp = str(int(time.time()))[-4:]  # 4 derniers chiffres du timestamp
            random_num = random.randint(10, 99)
            base_code = f"{self.category.type.upper()[:3]}-{self.name[:3].upper()}-{timestamp}{random_num}"

            # Vérifier l'unicité et ajuster si nécessaire
            self.code = base_code
            counter = 1
            while Product.objects.filter(code=self.code).exists():
                self.code = f"{base_code}-{counter}"
                counter += 1

        super().save(*args, **kwargs)
