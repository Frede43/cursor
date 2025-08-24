# 🎯 Guide de Test - Dialogs de Création

## 📋 Objectif
Tester les dialogs de création dans les pages Products, Supplies et Expenses pour vérifier qu'ils fonctionnent correctement côté backend et frontend.

## 🔐 Prérequis
- **Serveur Django :** http://localhost:8000 (en cours d'exécution)
- **Frontend React :** http://localhost:5173 (en cours d'exécution)
- **Identifiants Admin :** admin / admin123

## 📦 Test 1: Dialog Products (Products.tsx)

### ✅ Status: ENTIÈREMENT FONCTIONNEL

### 🎯 Objectif
Tester la création de nouveaux produits via le dialog.

### 📍 Étapes de Test
1. **Accéder à la page :**
   - Ouvrir http://localhost:5173/products
   - Se connecter avec admin / admin123

2. **Ouvrir le dialog :**
   - Cliquer sur le bouton "Ajouter un produit" (icône Plus)
   - Vérifier que le dialog s'ouvre

3. **Remplir le formulaire :**
   - **Nom :** "Test Produit Dialog"
   - **Catégorie :** Sélectionner une catégorie (Bières, Plats Principaux, Snacks)
   - **Prix d'achat :** 1000
   - **Prix de vente :** 1500
   - **Stock actuel :** 50
   - **Stock minimum :** 10
   - **Unité :** Sélectionner "Pièce"
   - **Description :** "Produit de test"

4. **Valider la création :**
   - Cliquer sur "Créer le produit"
   - Vérifier que le produit apparaît dans la liste
   - Vérifier que le dialog se ferme

### ✅ Résultats Attendus
- Dialog s'ouvre sans erreur
- Catégories sont chargées dans le select
- Création réussit et produit apparaît
- Message de succès affiché

## 🚚 Test 2: Dialog Supplies (Supplies.tsx)

### ⚠️ Status: PARTIELLEMENT FONCTIONNEL

### 🎯 Objectif
Tester la création d'approvisionnements via le dialog.

### 📍 Étapes de Test
1. **Accéder à la page :**
   - Ouvrir http://localhost:5173/supplies
   - Se connecter avec admin / admin123

2. **Ouvrir le dialog :**
   - Cliquer sur "Nouvel approvisionnement"
   - Vérifier que le dialog s'ouvre

3. **Remplir le formulaire :**
   - **Fournisseur :** Sélectionner un fournisseur
   - **Date de livraison :** Date actuelle
   - **Produits :** Ajouter des produits avec quantités
   - **Notes :** "Test approvisionnement"

4. **Tenter la création :**
   - Cliquer sur "Créer l'approvisionnement"
   - Observer le comportement

### ⚠️ Résultats Possibles
- Dialog s'ouvre correctement
- Données sont chargées (fournisseurs, produits)
- Création peut échouer (endpoint POST à vérifier)

## 💰 Test 3: Dialog Expenses (Expenses.tsx)

### ⚠️ Status: LECTURE SEULE

### 🎯 Objectif
Tester la création de dépenses via le dialog.

### 📍 Étapes de Test
1. **Accéder à la page :**
   - Ouvrir http://localhost:5173/expenses
   - Se connecter avec admin / admin123

2. **Ouvrir le dialog :**
   - Cliquer sur "Nouvelle dépense"
   - Vérifier que le dialog s'ouvre

3. **Remplir le formulaire :**
   - **Catégorie :** Sélectionner une catégorie
   - **Description :** "Test dépense dialog"
   - **Montant :** 25000
   - **Mode de paiement :** Espèces
   - **Date :** Date actuelle

4. **Tenter la création :**
   - Cliquer sur "Créer la dépense"
   - Observer le comportement

### ⚠️ Résultats Possibles
- Dialog s'ouvre correctement
- Formulaire est fonctionnel
- Création peut échouer (endpoint POST manquant)

## 🔧 Dépannage

### Si le dialog ne s'ouvre pas :
1. Vérifier la console du navigateur (F12)
2. Vérifier que le serveur Django fonctionne
3. Vérifier les permissions utilisateur

### Si la création échoue :
1. Vérifier la console réseau (F12 > Network)
2. Vérifier les logs du serveur Django
3. Vérifier que tous les champs requis sont remplis

### Si les données ne se chargent pas :
1. Vérifier les appels API dans la console réseau
2. Vérifier les tokens d'authentification
3. Redémarrer le frontend si nécessaire

## 📊 Résultats des Tests Automatisés

### ✅ Tests Backend Réussis
- API Products : Création fonctionnelle
- API Supplies : Lecture fonctionnelle
- API Expenses : Lecture fonctionnelle
- Données frontend : Toutes accessibles

### 🎯 Recommandations
1. **Products.tsx** - ✅ Entièrement fonctionnel, prêt à utiliser
2. **Supplies.tsx** - ⚠️ Vérifier la création côté frontend
3. **Expenses.tsx** - ⚠️ Implémenter endpoint POST si nécessaire

## 🚀 Validation Finale

Le test est réussi quand :
1. **Dialog Products** fonctionne à 100%
2. **Dialog Supplies** s'ouvre et charge les données
3. **Dialog Expenses** s'ouvre et affiche le formulaire
4. **Aucune erreur JavaScript** dans la console
5. **Messages d'erreur appropriés** si création échoue

---

**🎊 Une fois validé, les dialogs sont prêts pour la production !**
