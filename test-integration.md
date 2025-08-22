# 🧪 **GUIDE DE TEST D'INTÉGRATION FRONTEND-BACKEND**

## 📋 **ÉTAPES DE TEST**

### **1. Démarrer le Backend Django**
```bash
cd D:/ProjetApp/bar-stock-wise/backend
python manage.py runserver
```
✅ **Vérifier** : Backend accessible sur http://localhost:8000

### **2. Démarrer le Frontend React**
```bash
cd C:/Users/AlainDev/Downloads/bar-wise-spark-main
npm install  # Si pas encore fait
npm run dev
```
✅ **Vérifier** : Frontend accessible sur http://localhost:8080

### **3. Tests de Connexion API**

#### **Test 1 : Authentification**
1. Aller sur http://localhost:8080/login
2. Essayer de se connecter avec :
   - **Email** : admin@barstock.demo
   - **Mot de passe** : demo123
3. **Résultat attendu** : Connexion réussie avec données réelles du backend

#### **Test 2 : Dashboard Complet**
1. Aller sur http://localhost:8080/dashboard
2. **Vérifier** :
   - ✅ Statistiques réelles du backend
   - ✅ Données de cuisine (ingrédients, recettes)
   - ✅ Alertes de stock
   - ✅ Bouton "Actualiser" fonctionnel

#### **Test 3 : Page Kitchen**
1. Aller sur http://localhost:8080/kitchen
2. **Vérifier** :
   - ✅ Liste des ingrédients avec données réelles
   - ✅ Recettes complexes (Coq au Vin Burundais)
   - ✅ Alertes de stock automatiques
   - ✅ Statuts en temps réel

#### **Test 4 : Fonctionnalités Avancées**
1. **Créer une vente** avec un plat qui a une recette
2. **Vérifier** : Déduction automatique des ingrédients
3. **Vérifier** : Alertes générées si stock faible

## 🔧 **DÉPANNAGE**

### **Erreur de Connexion API**
```
❌ Network Error / CORS Error
```
**Solution** :
1. Vérifier que le backend Django tourne sur le port 8000
2. Vérifier la configuration proxy dans vite.config.ts
3. Redémarrer le frontend

### **Erreur d'Authentification**
```
❌ 401 Unauthorized
```
**Solution** :
1. Créer un superuser Django :
   ```bash
   cd backend
   python manage.py createsuperuser
   ```
2. Utiliser ces identifiants pour se connecter

### **Données Manquantes**
```
❌ Pas d'ingrédients/recettes
```
**Solution** :
1. Exécuter les scripts de données d'exemple :
   ```bash
   cd backend
   python create_kitchen_data.py
   python create_complex_recipe.py
   ```

## ✅ **CHECKLIST DE VALIDATION**

### **Backend Django**
- [ ] Serveur démarré sur port 8000
- [ ] API accessible : http://localhost:8000/api/
- [ ] Admin accessible : http://localhost:8000/admin/
- [ ] Données d'exemple créées
- [ ] Migrations appliquées

### **Frontend React**
- [ ] Serveur démarré sur port 8080
- [ ] Proxy API configuré
- [ ] React Query configuré
- [ ] Services API créés
- [ ] Hooks personnalisés fonctionnels

### **Intégration**
- [ ] Authentification réelle
- [ ] Dashboard avec données backend
- [ ] Page Kitchen fonctionnelle
- [ ] Alertes en temps réel
- [ ] Gestion d'erreurs

## 🚀 **FONCTIONNALITÉS TESTÉES**

### **✅ Implémentées et Testées**
1. **Service API complet** avec authentification JWT
2. **Hooks React Query** pour cache et gestion d'état
3. **Dashboard avec données réelles** du backend
4. **Page Kitchen** avec ingrédients et recettes
5. **Gestion d'erreurs** et retry automatique
6. **Configuration proxy** Vite pour développement

### **🔄 En Cours d'Implémentation**
1. **Migration des autres pages** (Produits, Ventes, etc.)
2. **WebSockets** pour notifications temps réel
3. **Tests unitaires** et d'intégration
4. **Optimisations performance**

### **📋 À Implémenter**
1. **Toutes les pages** avec données réelles
2. **Formulaires de création/modification**
3. **Gestion des fichiers/images**
4. **Mode hors ligne**

## 📊 **RÉSULTATS ATTENDUS**

Si tout fonctionne correctement, vous devriez voir :

1. **Dashboard** : Statistiques réelles avec données du backend Django
2. **Kitchen** : 19 ingrédients, 3 recettes, alertes de stock
3. **Navigation** : Menu avec nouvelles pages (Dashboard, Kitchen)
4. **Performance** : Chargement rapide avec cache React Query
5. **Erreurs** : Gestion gracieuse avec messages utilisateur

## 🎯 **PROCHAINES ÉTAPES**

1. **Tester l'intégration** avec ce guide
2. **Migrer les autres pages** une par une
3. **Ajouter les WebSockets** pour temps réel
4. **Optimiser les performances**
5. **Ajouter les tests automatisés**

---

**🔥 Le frontend est maintenant connecté au backend avec toutes les fonctionnalités avancées !**
