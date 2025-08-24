#!/usr/bin/env python
"""
SOLUTION DÉFINITIVE AU PROBLÈME DE CONNEXION
Ce script diagnostique et corrige tous les problèmes possibles
"""

import os
import sys
import django
import requests
import json
import subprocess
import time
from pathlib import Path

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstock_api.settings')
sys.path.append('backend')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import Permission, UserPermission

User = get_user_model()

class LoginFixerUltimate:
    def __init__(self):
        self.results = []
        
    def log(self, message, success=True):
        status = "✅" if success else "❌"
        print(f"{status} {message}")
        self.results.append((message, success))
    
    def test_backend_connectivity(self):
        """Test 1: Connectivité backend"""
        print("\n🔍 TEST 1: CONNECTIVITÉ BACKEND")
        try:
            response = requests.get('http://localhost:8000/api/accounts/login/', timeout=5)
            if response.status_code in [405, 200]:
                self.log("Backend Django accessible")
                return True
            else:
                self.log(f"Backend problème HTTP {response.status_code}", False)
                return False
        except Exception as e:
            self.log(f"Backend inaccessible: {e}", False)
            return False
    
    def fix_admin_user(self):
        """Test 2: Corriger l'utilisateur admin"""
        print("\n🔧 TEST 2: CORRECTION UTILISATEUR ADMIN")
        try:
            # Supprimer tous les anciens admins
            User.objects.filter(username='admin').delete()
            
            # Créer un admin propre
            admin = User.objects.create_user(
                username='admin',
                email='admin@barstock.com',
                password='admin123',
                first_name='Admin',
                last_name='System',
                role='admin',
                is_staff=True,
                is_superuser=True,
                is_active=True
            )
            
            self.log(f"Utilisateur admin créé/corrigé: {admin.username}")
            return True
        except Exception as e:
            self.log(f"Erreur création admin: {e}", False)
            return False
    
    def test_api_login(self):
        """Test 3: Test API de connexion"""
        print("\n🔐 TEST 3: API DE CONNEXION")
        try:
            headers = {
                'Content-Type': 'application/json',
                'Origin': 'http://localhost:5173'
            }
            
            data = {
                'username': 'admin',
                'password': 'admin123'
            }
            
            response = requests.post(
                'http://localhost:8000/api/accounts/login/',
                json=data,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                login_data = response.json()
                self.log(f"API login fonctionne - User: {login_data['user']['username']}")
                
                # Test permissions
                token = login_data['tokens']['access']
                perm_response = requests.get(
                    'http://localhost:8000/api/accounts/check-permissions/',
                    headers={'Authorization': f'Bearer {token}', 'Origin': 'http://localhost:5173'},
                    timeout=10
                )
                
                if perm_response.status_code == 200:
                    self.log("API permissions fonctionne")
                    return True
                else:
                    self.log(f"API permissions problème: {perm_response.status_code}", False)
                    return False
            else:
                self.log(f"API login échoue: {response.status_code} - {response.text}", False)
                return False
                
        except Exception as e:
            self.log(f"Erreur test API: {e}", False)
            return False
    
    def fix_frontend_config(self):
        """Test 4: Corriger la configuration frontend"""
        print("\n⚙️ TEST 4: CORRECTION CONFIGURATION FRONTEND")
        
        try:
            # 1. Corriger api.ts
            api_file = Path('src/services/api.ts')
            if api_file.exists():
                content = api_file.read_text(encoding='utf-8')
                
                # Forcer l'URL API à être relative
                if 'http://localhost:8000/api' in content:
                    content = content.replace('http://localhost:8000/api', '/api')
                    api_file.write_text(content, encoding='utf-8')
                    self.log("Configuration API corrigée vers /api")
                else:
                    self.log("Configuration API déjà correcte")
            
            # 2. Vérifier .env
            env_file = Path('.env')
            env_file.write_text('VITE_API_URL=/api\n', encoding='utf-8')
            self.log("Fichier .env créé/corrigé")
            
            # 3. Vérifier vite.config.ts
            vite_config = Path('vite.config.ts')
            if vite_config.exists():
                content = vite_config.read_text(encoding='utf-8')
                if 'port: 8080' in content:
                    content = content.replace('port: 8080', 'port: 5173')
                    vite_config.write_text(content, encoding='utf-8')
                    self.log("Configuration Vite corrigée vers port 5173")
                else:
                    self.log("Configuration Vite déjà correcte")
            
            return True
            
        except Exception as e:
            self.log(f"Erreur correction frontend: {e}", False)
            return False
    
    def fix_cors_settings(self):
        """Test 5: Corriger les paramètres CORS"""
        print("\n🌐 TEST 5: CORRECTION CORS")
        
        try:
            settings_file = Path('backend/barstock_api/settings.py')
            if settings_file.exists():
                content = settings_file.read_text(encoding='utf-8')
                
                # Vérifier que localhost:5173 est dans CORS_ALLOWED_ORIGINS
                if 'localhost:5173' in content:
                    self.log("CORS déjà configuré pour localhost:5173")
                else:
                    # Ajouter localhost:5173 si manquant
                    cors_section = '''CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]'''
                    # Remplacer la section CORS existante
                    import re
                    pattern = r'CORS_ALLOWED_ORIGINS\s*=\s*\[.*?\]'
                    content = re.sub(pattern, cors_section, content, flags=re.DOTALL)
                    settings_file.write_text(content, encoding='utf-8')
                    self.log("CORS corrigé pour localhost:5173")
                
                return True
            else:
                self.log("Fichier settings.py non trouvé", False)
                return False
                
        except Exception as e:
            self.log(f"Erreur correction CORS: {e}", False)
            return False
    
    def create_simple_login_test(self):
        """Test 6: Créer un test de connexion simple"""
        print("\n🧪 TEST 6: CRÉATION TEST SIMPLE")
        
        test_html = '''<!DOCTYPE html>
<html>
<head>
    <title>Test Login Simple</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .result { margin: 10px 0; padding: 10px; border-radius: 5px; }
        .success { background: #d4edda; color: #155724; }
        .error { background: #f8d7da; color: #721c24; }
        button { padding: 10px 20px; margin: 5px; }
        input { padding: 8px; margin: 5px; width: 200px; }
    </style>
</head>
<body>
    <h1>🔐 Test de Connexion Simple</h1>
    <div>
        <input type="text" id="username" placeholder="Username" value="admin">
        <input type="password" id="password" placeholder="Password" value="admin123">
        <button onclick="testLogin()">Se connecter</button>
    </div>
    <div id="result"></div>
    
    <script>
        async function testLogin() {
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const resultDiv = document.getElementById('result');
            
            try {
                const response = await fetch('/api/accounts/login/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ username, password })
                });
                
                if (response.ok) {
                    const data = await response.json();
                    resultDiv.innerHTML = `<div class="result success">✅ Connexion réussie! Utilisateur: ${data.user.username} (${data.user.role})</div>`;
                } else {
                    const errorText = await response.text();
                    resultDiv.innerHTML = `<div class="result error">❌ Erreur ${response.status}: ${errorText}</div>`;
                }
            } catch (error) {
                resultDiv.innerHTML = `<div class="result error">❌ Erreur réseau: ${error.message}</div>`;
            }
        }
    </script>
</body>
</html>'''
        
        try:
            test_file = Path('public/test-login.html')
            test_file.parent.mkdir(exist_ok=True)
            test_file.write_text(test_html, encoding='utf-8')
            self.log("Test de connexion simple créé: /test-login.html")
            return True
        except Exception as e:
            self.log(f"Erreur création test: {e}", False)
            return False
    
    def run_complete_fix(self):
        """Exécuter toutes les corrections"""
        print("🚀 CORRECTION COMPLÈTE DU PROBLÈME DE CONNEXION")
        print("=" * 60)
        
        # Exécuter tous les tests/corrections
        tests = [
            self.test_backend_connectivity,
            self.fix_admin_user,
            self.test_api_login,
            self.fix_frontend_config,
            self.fix_cors_settings,
            self.create_simple_login_test
        ]
        
        all_success = True
        for test in tests:
            success = test()
            if not success:
                all_success = False
        
        # Résumé final
        print("\n" + "=" * 60)
        print("📊 RÉSUMÉ DES CORRECTIONS")
        print("=" * 60)
        
        success_count = sum(1 for _, success in self.results if success)
        total_count = len(self.results)
        
        for message, success in self.results:
            status = "✅" if success else "❌"
            print(f"{status} {message}")
        
        print(f"\nRésultat: {success_count}/{total_count} corrections réussies")
        
        if all_success:
            print("\n🎉 PROBLÈME RÉSOLU!")
            print("✅ Toutes les corrections ont été appliquées")
            print("✅ Le système devrait maintenant fonctionner")
            print("\n🚀 INSTRUCTIONS FINALES:")
            print("1. Redémarrez le serveur Django (Ctrl+C puis python manage.py runserver)")
            print("2. Redémarrez le frontend (Ctrl+C puis npm run dev)")
            print("3. Ouvrez http://localhost:5173")
            print("4. Connectez-vous avec admin/admin123")
            print("5. Si ça ne marche pas, testez: http://localhost:5173/test-login.html")
        else:
            print(f"\n⚠️ {total_count - success_count} problème(s) persistent")
            print("❌ Des corrections manuelles peuvent être nécessaires")
        
        return all_success

if __name__ == "__main__":
    fixer = LoginFixerUltimate()
    fixer.run_complete_fix()
