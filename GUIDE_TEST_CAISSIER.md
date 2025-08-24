# 🎯 Guide de Test - Menus Caissier

## 📋 Objectif
Vérifier que les menus affichés correspondent exactement aux permissions accordées au caissier.

## 🔐 Identifiants de Test
- **URL :** http://localhost:5173
- **Username :** `test_caissier`
- **Password :** `caissier123`

## ✅ Menus qui DOIVENT être visibles

### 🏠 Toujours Visibles
- **Accueil** - Dashboard principal
- **Mon Profil** - Gestion du profil utilisateur

### 🔐 Selon Permissions Accordées
- **Ventes** - Gestion des ventes (permission: `sales_manage`)
- **Historique des Ventes** - Consultation historique (permission: `sales_history_view`)
- **Tables** - Gestion des tables (permission: `tables_manage`)
- **Produits** - Consultation produits LECTURE SEULE (permission: `products_view`)

## ❌ Menus qui NE DOIVENT PAS être visibles

### 🚫 Administration (Admin seulement)
- **Utilisateurs** - Gestion des utilisateurs
- **Fournisseurs** - Gestion des fournisseurs

### 🚫 Fonctions Avancées
- **Ajout de Produits** - Pas de permission `products_manage`
- **Paramètres Système** - Pas de permission `settings_manage`
- **Surveillance** - Pas de permission `monitoring_view`

## 🧪 Tests à Effectuer

### 1. Test de Connexion
1. Ouvrir http://localhost:5173
2. Se connecter avec `test_caissier` / `caissier123`
3. Vérifier que la connexion réussit

### 2. Test des Menus Visibles
1. Vérifier que la sidebar affiche uniquement les menus autorisés
2. Cliquer sur chaque menu autorisé pour vérifier l'accès
3. Vérifier que les menus interdits n'apparaissent pas

### 3. Test des Permissions Produits
1. Aller sur la page **Produits**
2. Vérifier que vous pouvez VOIR les produits
3. Vérifier que vous NE POUVEZ PAS ajouter de nouveaux produits
4. Vérifier que les boutons d'ajout/modification sont cachés ou désactivés

### 4. Test des Accès Interdits
1. Essayer d'accéder manuellement à `/users` dans l'URL
2. Vérifier que l'accès est refusé
3. Essayer d'accéder à `/suppliers`
4. Vérifier que l'accès est refusé

## 📊 Résultats Attendus

### ✅ Succès si :
- Seuls les 6 menus autorisés sont visibles
- Tous les menus autorisés fonctionnent
- Les accès interdits sont bloqués
- La page Produits est en lecture seule

### ❌ Problème si :
- Des menus interdits apparaissent
- Des menus autorisés ne fonctionnent pas
- Vous pouvez ajouter des produits
- Vous pouvez accéder aux pages interdites

## 🔧 Dépannage

### Si des menus interdits apparaissent :
```bash
# Vérifier les permissions
python test_cashier_menus.py
```

### Si des menus autorisés manquent :
1. Vérifier que le serveur Django fonctionne
2. Vérifier que les permissions sont bien assignées
3. Redémarrer le frontend si nécessaire

## 🎉 Validation Finale

Le test est réussi quand :
1. **6 menus exactement** sont visibles dans la sidebar
2. **Ventes, Tables, Historique** fonctionnent parfaitement
3. **Produits** est accessible en lecture seule
4. **Utilisateurs et Fournisseurs** sont inaccessibles
5. **Aucun bouton d'ajout de produits** n'est visible

---

**🚀 Une fois validé, le système de permissions fonctionne parfaitement !**
