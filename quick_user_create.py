import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstock_api.settings')
sys.path.append('backend')
django.setup()

from accounts.models import User

# Créer admin
try:
    admin = User.objects.get(email='admin@barstockwise.com')
    print('✅ Admin existe déjà')
except User.DoesNotExist:
    # Générer un username unique
    import uuid
    admin_username = f'admin_{uuid.uuid4().hex[:8]}'
    admin = User.objects.create_user(
        username=admin_username,
        email='admin@barstockwise.com',
        password='admin123',
        first_name='Admin',
        last_name='BarStockWise',
        phone='000000000',
        role='admin',
        is_staff=True,
        is_superuser=True
    )
    print('✅ Admin créé: admin@barstockwise.com / admin123')

# Créer utilisateur test
try:
    user = User.objects.get(email='jean.testeur@barstockwise.com')
    print('✅ Utilisateur existe déjà')
except User.DoesNotExist:
    # Générer un username unique
    import uuid
    user_username = f'jean_testeur_{uuid.uuid4().hex[:8]}'
    user = User.objects.create_user(
        username=user_username,
        email='jean.testeur@barstockwise.com',
        password='temp123456',
        first_name='Jean',
        last_name='Testeur',
        phone='123456789',
        role='server',
        is_staff=True
    )
    print('✅ Utilisateur créé: jean.testeur@barstockwise.com / temp123456')

# Lister les utilisateurs
print('\n📋 Utilisateurs dans la base:')
for u in User.objects.all():
    admin_badge = ' (ADMIN)' if u.is_superuser else ''
    print(f'   {u.first_name} {u.last_name}{admin_badge} | {u.email} | {u.role}')

print('\n🎉 Utilisateurs prêts pour les tests!')
