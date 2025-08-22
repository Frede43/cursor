# 🚀 Guide de Déploiement Local - BarStockWise

Ce guide vous explique comment déployer et exécuter l'application BarStockWise en local sur votre machine.

## 📋 Prérequis Système

### Logiciels requis
- **Python 3.8+** (recommandé: Python 3.11)
- **Node.js 18+** et **npm** ou **yarn**
- **Git** pour cloner le projet

### Vérification des versions
```bash
python --version
node --version
npm --version
git --version
```

## 📥 Installation

### 1. Cloner le projet
```bash
git clone https://github.com/Frede43/cursor.git
cd cursor
```

### 2. Configuration du Backend Django

#### Créer un environnement virtuel Python
```bash
# Windows
cd backend
python -m venv venv
venv\Scripts\activate

# Linux/Mac
cd backend
python3 -m venv venv
source venv/bin/activate
```

#### Installer les dépendances Python
```bash
pip install -r requirements.txt
```

#### Configuration de la base de données
```bash
# Appliquer les migrations
python manage.py makemigrations
python manage.py migrate

# Créer un superutilisateur (optionnel)
python manage.py createsuperuser
```

#### Variables d'environnement
Créer un fichier `.env` dans le dossier `backend/` :
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### 3. Configuration du Frontend React

#### Installer les dépendances Node.js
```bash
# Retourner au dossier racine
cd ..
npm install
# ou
yarn install
```

#### Variables d'environnement Frontend
Le fichier `.env` à la racine contient déjà la configuration :
```env
VITE_API_URL=http://localhost:8000
```

## 🏃‍♂️ Démarrage de l'Application

### Méthode 1: Démarrage Manuel (2 terminaux)

#### Terminal 1 - Backend Django
```bash
cd backend
# Activer l'environnement virtuel si pas déjà fait
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

python manage.py runserver
```
Le backend sera accessible sur: http://localhost:8000

#### Terminal 2 - Frontend React
```bash
# Depuis la racine du projet
npm run dev
# ou
yarn dev
```
Le frontend sera accessible sur: http://localhost:5173

### Méthode 2: Script de Démarrage Automatique

Utiliser le script fourni pour démarrer les deux services :

#### Windows
```bash
.\start-app.bat
```

#### Linux/Mac
```bash
chmod +x start-app.sh
./start-app.sh
```

## 🌐 Accès à l'Application

Une fois les deux services démarrés :

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Admin Django**: http://localhost:8000/admin

## 👤 Connexion par Défaut

### Comptes de test disponibles
- **Admin**: `admin` / `admin123`
- **Gérant**: `gerant` / `gerant123`
- **Serveur**: `serveur` / `serveur123`

## 🔧 Fonctionnalités Disponibles

### Modules principaux
- **Dashboard** - Vue d'ensemble des ventes et stocks
- **Kitchen** - Gestion des ingrédients et recettes
- **Products** - Catalogue des produits avec prix automatiques
- **Sales** - Point de vente avec gestion temps réel
- **Tables** - Gestion des tables et réservations
- **Orders** - Suivi des commandes
- **Reports** - Rapports et analyses
- **Users** - Gestion des utilisateurs et rôles
- **Settings** - Configuration système dynamique
- **Alerts** - Notifications de stock faible

### API REST
L'API est accessible sur http://localhost:8000/api/ avec les endpoints :
- `/api/accounts/` - Authentification
- `/api/products/` - Produits
- `/api/sales/` - Ventes
- `/api/kitchen/` - Cuisine
- `/api/settings/` - Paramètres
- `/api/alerts/` - Alertes

## 🛠️ Développement

### Structure du projet
```
bar-stock-wise/
├── backend/           # Django REST API
│   ├── accounts/      # Authentification
│   ├── products/      # Gestion produits
│   ├── sales/         # Système de vente
│   ├── kitchen/       # Gestion cuisine
│   ├── settings/      # Paramètres système
│   └── alerts/        # Système d'alertes
├── src/              # Frontend React
│   ├── components/   # Composants UI
│   ├── pages/        # Pages de l'app
│   ├── hooks/        # Hooks personnalisés
│   └── lib/          # Utilitaires
└── public/           # Assets statiques
```

### Commandes utiles

#### Backend
```bash
# Créer une nouvelle migration
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Collecter les fichiers statiques
python manage.py collectstatic

# Lancer les tests
python manage.py test
```

#### Frontend
```bash
# Démarrage en mode développement
npm run dev

# Build de production
npm run build

# Prévisualisation du build
npm run preview

# Linter
npm run lint
```

## 🐛 Dépannage

### Problèmes courants

#### Port déjà utilisé
```bash
# Changer le port du backend
python manage.py runserver 8001

# Changer le port du frontend
npm run dev -- --port 3000
```

#### Erreurs de base de données
```bash
# Supprimer et recréer la DB
rm backend/db.sqlite3
python manage.py migrate
```

#### Problèmes de dépendances
```bash
# Backend
pip install -r requirements.txt --force-reinstall

# Frontend
rm -rf node_modules package-lock.json
npm install
```

## 📞 Support

Pour toute question ou problème :
1. Vérifiez les logs dans les terminaux
2. Consultez la documentation Django/React
3. Vérifiez les issues GitHub du projet

## 🎯 Prochaines Étapes

Une fois l'application déployée localement :
1. Explorez les différents modules
2. Testez les fonctionnalités de gestion
3. Configurez les paramètres selon vos besoins
4. Ajoutez vos propres données de test

L'application est maintenant prête à être utilisée pour la gestion de votre restaurant !
