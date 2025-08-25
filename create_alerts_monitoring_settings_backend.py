#!/usr/bin/env python
"""
Créer les endpoints backend pour Alerts, Monitoring et Settings
"""

def create_alerts_models():
    """Créer les modèles pour les alertes"""
    print("🔧 CRÉATION MODÈLES ALERTES...")
    
    alerts_models = '''
# Modèles pour les alertes système
class Alert(models.Model):
    """
    Modèle pour les alertes système
    """
    ALERT_TYPES = [
        ('stock', 'Stock'),
        ('sales', 'Ventes'),
        ('system', 'Système'),
        ('security', 'Sécurité'),
        ('maintenance', 'Maintenance'),
    ]
    
    PRIORITIES = [
        ('low', 'Faible'),
        ('medium', 'Moyenne'),
        ('high', 'Élevée'),
        ('critical', 'Critique'),
    ]
    
    STATUSES = [
        ('active', 'Active'),
        ('resolved', 'Résolue'),
        ('archived', 'Archivée'),
    ]
    
    type = models.CharField(
        max_length=20,
        choices=ALERT_TYPES,
        verbose_name='Type d\'alerte'
    )
    
    priority = models.CharField(
        max_length=10,
        choices=PRIORITIES,
        default='medium',
        verbose_name='Priorité'
    )
    
    title = models.CharField(
        max_length=200,
        verbose_name='Titre'
    )
    
    message = models.TextField(
        verbose_name='Message'
    )
    
    status = models.CharField(
        max_length=10,
        choices=STATUSES,
        default='active',
        verbose_name='Statut'
    )
    
    # Relations optionnelles
    related_product = models.ForeignKey(
        'products.Product',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Produit lié'
    )
    
    related_ingredient = models.ForeignKey(
        'kitchen.Ingredient',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Ingrédient lié'
    )
    
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='created_alerts',
        verbose_name='Créé par'
    )
    
    resolved_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='resolved_alerts',
        verbose_name='Résolu par'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de création'
    )
    
    resolved_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Date de résolution'
    )
    
    class Meta:
        verbose_name = 'Alerte'
        verbose_name_plural = 'Alertes'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_type_display()} - {self.title}"
    
    @classmethod
    def create_stock_alert(cls, ingredient=None, product=None, message=""):
        """Créer une alerte de stock"""
        if ingredient:
            title = f"Stock bas: {ingredient.nom}"
            related_ingredient = ingredient
            related_product = None
        elif product:
            title = f"Stock bas: {product.name}"
            related_product = product
            related_ingredient = None
        else:
            title = "Alerte de stock"
            related_product = None
            related_ingredient = None
        
        return cls.objects.create(
            type='stock',
            priority='high' if 'critique' in message.lower() else 'medium',
            title=title,
            message=message,
            related_product=related_product,
            related_ingredient=related_ingredient
        )


class SystemMetric(models.Model):
    """
    Modèle pour les métriques système
    """
    METRIC_TYPES = [
        ('api_response_time', 'Temps de réponse API'),
        ('database_connections', 'Connexions base de données'),
        ('server_cpu', 'CPU serveur'),
        ('server_memory', 'Mémoire serveur'),
        ('server_disk', 'Disque serveur'),
        ('active_users', 'Utilisateurs actifs'),
    ]
    
    metric_type = models.CharField(
        max_length=30,
        choices=METRIC_TYPES,
        verbose_name='Type de métrique'
    )
    
    value = models.FloatField(
        verbose_name='Valeur'
    )
    
    unit = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Unité'
    )
    
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Horodatage'
    )
    
    class Meta:
        verbose_name = 'Métrique système'
        verbose_name_plural = 'Métriques système'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.get_metric_type_display()}: {self.value} {self.unit}"


class SystemSetting(models.Model):
    """
    Modèle pour les paramètres système
    """
    SETTING_TYPES = [
        ('general', 'Général'),
        ('notifications', 'Notifications'),
        ('printing', 'Impression'),
        ('security', 'Sécurité'),
        ('backup', 'Sauvegarde'),
    ]
    
    category = models.CharField(
        max_length=20,
        choices=SETTING_TYPES,
        verbose_name='Catégorie'
    )
    
    key = models.CharField(
        max_length=100,
        verbose_name='Clé'
    )
    
    value = models.TextField(
        verbose_name='Valeur'
    )
    
    description = models.TextField(
        blank=True,
        verbose_name='Description'
    )
    
    updated_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Modifié par'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Dernière modification'
    )
    
    class Meta:
        verbose_name = 'Paramètre système'
        verbose_name_plural = 'Paramètres système'
        unique_together = ['category', 'key']
    
    def __str__(self):
        return f"{self.get_category_display()} - {self.key}"
    
    @classmethod
    def get_setting(cls, category, key, default=None):
        """Récupérer un paramètre"""
        try:
            setting = cls.objects.get(category=category, key=key)
            return setting.value
        except cls.DoesNotExist:
            return default
    
    @classmethod
    def set_setting(cls, category, key, value, user=None):
        """Définir un paramètre"""
        setting, created = cls.objects.get_or_create(
            category=category,
            key=key,
            defaults={'value': value, 'updated_by': user}
        )
        if not created:
            setting.value = value
            setting.updated_by = user
            setting.save()
        return setting
'''
    
    try:
        # Ajouter aux modèles analytics (ou créer une nouvelle app)
        with open('backend/analytics/models.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'class Alert' not in content:
            content += alerts_models
            
            with open('backend/analytics/models.py', 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Modèles alertes ajoutés")
        else:
            print("✅ Modèles alertes déjà présents")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur création modèles: {e}")
        return False

def create_alerts_serializers():
    """Créer les serializers pour les alertes"""
    print("\n🔧 CRÉATION SERIALIZERS ALERTES...")
    
    serializers_code = '''
# Serializers pour les alertes et monitoring
class AlertSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    resolved_by_name = serializers.CharField(source='resolved_by.get_full_name', read_only=True)
    related_product_name = serializers.CharField(source='related_product.name', read_only=True)
    related_ingredient_name = serializers.CharField(source='related_ingredient.nom', read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Alert
        fields = [
            'id', 'type', 'type_display', 'priority', 'priority_display',
            'title', 'message', 'status', 'status_display',
            'related_product', 'related_product_name',
            'related_ingredient', 'related_ingredient_name',
            'created_by', 'created_by_name', 'resolved_by', 'resolved_by_name',
            'created_at', 'resolved_at'
        ]
        read_only_fields = ['created_at', 'resolved_at']


class SystemMetricSerializer(serializers.ModelSerializer):
    metric_type_display = serializers.CharField(source='get_metric_type_display', read_only=True)
    
    class Meta:
        model = SystemMetric
        fields = [
            'id', 'metric_type', 'metric_type_display', 'value', 'unit', 'timestamp'
        ]
        read_only_fields = ['timestamp']


class SystemSettingSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.get_full_name', read_only=True)
    
    class Meta:
        model = SystemSetting
        fields = [
            'id', 'category', 'category_display', 'key', 'value',
            'description', 'updated_by', 'updated_by_name', 'updated_at'
        ]
        read_only_fields = ['updated_at']
'''
    
    try:
        with open('backend/analytics/serializers.py', 'w', encoding='utf-8') as f:
            f.write('''from rest_framework import serializers
from .models import Alert, SystemMetric, SystemSetting

''' + serializers_code)
        
        print("✅ Serializers alertes créés")
        return True
        
    except Exception as e:
        print(f"❌ Erreur création serializers: {e}")
        return False
