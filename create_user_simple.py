#!/usr/bin/env python3
"""
Script simple pour créer un utilisateur de test
"""

import sqlite3
import hashlib
from datetime import datetime

def hash_password(password):
    """Créer un hash de mot de passe compatible Django"""
    import hashlib
    import secrets
    
    # Générer un salt aléatoire
    salt = secrets.token_hex(16)
    
    # Créer le hash avec PBKDF2
    iterations = 100000
    hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), iterations)
    hash_hex = hash_obj.hex()
    
    # Format Django: pbkdf2_sha256$iterations$salt$hash
    return f"pbkdf2_sha256${iterations}${salt}${hash_hex}"

def create_user():
    """Créer un utilisateur directement en base SQLite"""
    print("🚀 Création d'utilisateur de test en base SQLite")
    print("=" * 50)
    
    # Connexion à la base de données
    db_path = "backend/db.sqlite3"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier si la table existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='accounts_user';")
        if not cursor.fetchone():
            print("❌ Table accounts_user non trouvée")
            return False
        
        # Vérifier si l'utilisateur existe déjà
        email = "jean.testeur@barstockwise.com"
        cursor.execute("SELECT id, first_name, last_name FROM accounts_user WHERE email = ?", (email,))
        existing = cursor.fetchone()
        
        if existing:
            print(f"⚠️ L'utilisateur {email} existe déjà")
            print(f"   ID: {existing[0]}")
            print(f"   Nom: {existing[1]} {existing[2]}")
            return True
        
        # Créer l'utilisateur
        print("👤 Création du nouvel utilisateur...")
        
        password_hash = hash_password("temp123456")
        now = datetime.now().isoformat()
        
        user_data = (
            "temp123456",  # password (sera hashé)
            None,          # last_login
            False,         # is_superuser
            email,         # email
            "Jean",        # first_name
            "Testeur",     # last_name
            True,          # is_active
            True,          # is_staff
            now,           # date_joined
            "123456789",   # phone
            "staff",       # role
            False,         # is_admin
            False,         # is_manager
        )
        
        # Insérer l'utilisateur
        cursor.execute("""
            INSERT INTO accounts_user 
            (password, last_login, is_superuser, email, first_name, last_name, 
             is_active, is_staff, date_joined, phone, role, is_admin, is_manager)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (password_hash,) + user_data[1:])
        
        user_id = cursor.lastrowid
        conn.commit()
        
        print(f"✅ Utilisateur créé avec succès!")
        print(f"   ID: {user_id}")
        print(f"   Email: {email}")
        print(f"   Nom: Jean Testeur")
        print(f"   Rôle: staff")
        print(f"   Mot de passe: temp123456")
        
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Erreur SQLite: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    finally:
        if conn:
            conn.close()

def create_admin():
    """Créer un utilisateur admin"""
    print("\n🔐 Création de l'utilisateur admin...")
    
    db_path = "backend/db.sqlite3"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier si l'admin existe déjà
        admin_email = "admin@barstockwise.com"
        cursor.execute("SELECT id, first_name, last_name FROM accounts_user WHERE email = ?", (admin_email,))
        existing = cursor.fetchone()
        
        if existing:
            print(f"✅ Admin existe déjà: {existing[1]} {existing[2]}")
            return True
        
        # Créer l'admin
        password_hash = hash_password("admin123")
        now = datetime.now().isoformat()
        
        cursor.execute("""
            INSERT INTO accounts_user 
            (password, last_login, is_superuser, email, first_name, last_name, 
             is_active, is_staff, date_joined, phone, role, is_admin, is_manager)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            password_hash,
            None,
            True,
            admin_email,
            "Admin",
            "BarStockWise",
            True,
            True,
            now,
            "000000000",
            "admin",
            True,
            True
        ))
        
        admin_id = cursor.lastrowid
        conn.commit()
        
        print(f"✅ Admin créé avec succès!")
        print(f"   ID: {admin_id}")
        print(f"   Email: {admin_email}")
        print(f"   Mot de passe: admin123")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur création admin: {e}")
        return False
    finally:
        if conn:
            conn.close()

def list_users():
    """Lister les utilisateurs"""
    print("\n📋 Liste des utilisateurs:")
    print("-" * 40)
    
    db_path = "backend/db.sqlite3"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, email, first_name, last_name, role, is_active, is_admin
            FROM accounts_user
            ORDER BY id
        """)
        
        users = cursor.fetchall()
        
        for user in users:
            user_id, email, first_name, last_name, role, is_active, is_admin = user
            status = "✅ Actif" if is_active else "❌ Inactif"
            role_emoji = {"admin": "👑", "manager": "👔", "staff": "👤"}.get(role, "👤")
            admin_badge = " (ADMIN)" if is_admin else ""
            
            print(f"{role_emoji} {first_name} {last_name}{admin_badge}")
            print(f"   ID: {user_id}")
            print(f"   Email: {email}")
            print(f"   Rôle: {role}")
            print(f"   Statut: {status}")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur listage: {e}")
        return False
    finally:
        if conn:
            conn.close()

def main():
    """Point d'entrée principal"""
    print("BarStockWise - Création d'utilisateurs SQLite")
    print("=" * 50)
    
    # Créer admin
    create_admin()
    
    # Créer utilisateur test
    create_user()
    
    # Lister les utilisateurs
    list_users()
    
    print("🎉 Création terminée!")
    print("\nComptes créés:")
    print("👑 Admin: admin@barstockwise.com / admin123")
    print("👤 Utilisateur: jean.testeur@barstockwise.com / temp123456")
    print("\nVous pouvez maintenant tester la connexion!")

if __name__ == "__main__":
    main()
