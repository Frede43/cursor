from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.conf import settings

class StockMovement(models.Model):
    """
    Modèle pour tracer tous les mouvements de stock
    """

    MOVEMENT_TYPES = [
        ('in', 'Entrée'),
        ('out', 'Sortie'),
        ('adjustment', 'Ajustement'),
        ('loss', 'Perte'),
        ('return', 'Retour'),
    ]

    REASONS = [
        ('purchase', 'Achat'),
        ('sale', 'Vente'),
        ('inventory', 'Inventaire'),
        ('damage', 'Dommage'),
        ('expiry', 'Expiration'),
        ('theft', 'Vol'),
        ('correction', 'Correction'),
    ]

    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='stock_movements',
        verbose_name='Produit'
    )

    movement_type = models.CharField(
        max_length=20,
        choices=MOVEMENT_TYPES,
        verbose_name='Type de mouvement'
    )

    reason = models.CharField(
        max_length=20,
        choices=REASONS,
        verbose_name='Raison'
    )

    quantity = models.PositiveIntegerField(
        verbose_name='Quantité'
    )

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        blank=True,
        null=True,
        verbose_name='Prix unitaire (BIF)'
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        blank=True,
        null=True,
        verbose_name='Montant total (BIF)'
    )

    stock_before = models.PositiveIntegerField(
        verbose_name='Stock avant'
    )

    stock_after = models.PositiveIntegerField(
        verbose_name='Stock après'
    )

    supplier = models.ForeignKey(
        'suppliers.Supplier',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Fournisseur'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Utilisateur'
    )

    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Notes'
    )

    reference = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Référence'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de création'
    )

    class Meta:
        verbose_name = 'Mouvement de stock'
        verbose_name_plural = 'Mouvements de stock'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product.name} - {self.get_movement_type_display()} - {self.quantity}"

    def save(self, *args, **kwargs):
        # Calculer le montant total si prix unitaire fourni
        if self.unit_price and not self.total_amount:
            self.total_amount = self.unit_price * self.quantity
        super().save(*args, **kwargs)


class Purchase(models.Model):
    """
    Modèle pour les achats/approvisionnements
    """

    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('received', 'Reçu'),
        ('partial', 'Partiel'),
        ('cancelled', 'Annulé'),
    ]

    reference = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Référence d\'achat'
    )

    supplier = models.ForeignKey(
        'suppliers.Supplier',
        on_delete=models.CASCADE,
        related_name='purchases',
        verbose_name='Fournisseur'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Utilisateur'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Statut'
    )

    order_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de commande'
    )

    delivery_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Date de livraison'
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        default=Decimal('0.00'),
        verbose_name='Montant total (BIF)'
    )

    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Notes'
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
        verbose_name = 'Achat'
        verbose_name_plural = 'Achats'
        ordering = ['-created_at']

    def __str__(self):
        return f"Achat {self.reference} - {self.supplier.name}"


class PurchaseItem(models.Model):
    """
    Détails des articles dans un achat
    """

    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Achat'
    )

    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        verbose_name='Produit'
    )

    quantity_ordered = models.PositiveIntegerField(
        verbose_name='Quantité commandée'
    )

    quantity_received = models.PositiveIntegerField(
        default=0,
        verbose_name='Quantité reçue'
    )

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Prix unitaire (BIF)'
    )

    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Prix total (BIF)'
    )

    class Meta:
        verbose_name = 'Article d\'achat'
        verbose_name_plural = 'Articles d\'achat'
        unique_together = ['purchase', 'product']

    def __str__(self):
        return f"{self.product.name} - {self.quantity_ordered}"

    def save(self, *args, **kwargs):
        # Calculer le prix total
        self.total_price = self.unit_price * self.quantity_ordered
        super().save(*args, **kwargs)


