// Test final de l'API dashboard après corrections

async function testFinalDashboard() {
    console.log('🎯 Test final de l\'API Dashboard...\n');
    
    const backendUrl = 'http://127.0.0.1:8000/api';
    
    try {
        const response = await fetch(`${backendUrl}/reports/dashboard/stats/`);
        
        if (response.ok) {
            const data = await response.json();
            
            console.log('✅ API Dashboard - Données finales:');
            console.log('=' * 50);
            
            // Analyser les données principales
            const today = data.today;
            const alerts = data.alerts;
            const quickStats = data.quick_stats;
            
            console.log('📊 DONNÉES PRINCIPALES:');
            console.log(`   • Date: ${today.date}`);
            console.log(`   • Ventes du jour: ${today.sales} commandes`);
            console.log(`   • Revenus du jour: ${today.revenue.toLocaleString()} BIF`);
            console.log(`   • Revenus détaillés: ${today.daily_revenue.toLocaleString()} BIF`);
            console.log(`   • Commandes en cours: ${today.pending_sales}`);
            
            console.log('\n🏪 STATISTIQUES RAPIDES:');
            console.log(`   • Produits actifs: ${quickStats.total_products}`);
            console.log(`   • Alertes actives: ${quickStats.active_alerts}`);
            
            console.log('\n🚨 ALERTES:');
            console.log(`   • Total non résolues: ${alerts.total_unresolved}`);
            console.log(`   • Stock bas: ${alerts.low_stock}`);
            console.log(`   • Rupture de stock: ${alerts.out_of_stock}`);
            
            console.log('\n🛒 TOP PRODUITS VENDUS:');
            today.products_sold.slice(0, 5).forEach((product, i) => {
                console.log(`   ${i + 1}. ${product.product__name}: ${product.quantity_sold} unités (${product.revenue.toLocaleString()} BIF)`);
            });
            
            // Vérifier si toutes les données sont correctes
            const allGood = 
                today.sales > 0 && 
                today.revenue > 0 && 
                today.daily_revenue > 0 && 
                quickStats.total_products > 0 &&
                today.products_sold.length > 0;
            
            if (allGood) {
                console.log('\n🎉 SUCCÈS COMPLET !');
                console.log('✅ Toutes les données du dashboard sont maintenant correctes');
                console.log('\n📋 ACTIONS SUIVANTES:');
                console.log('   1. Rafraîchir http://localhost:8081/');
                console.log('   2. Vérifier que les cartes affichent les bonnes valeurs');
                console.log('   3. Tester les boutons d\'action rapide');
                console.log('   4. Vérifier que le bouton "Actualiser" fonctionne');
                
                return true;
            } else {
                console.log('\n⚠️  Certaines données sont encore manquantes');
                return false;
            }
            
        } else {
            console.log(`❌ Erreur API: ${response.status}`);
            return false;
        }
        
    } catch (error) {
        console.log(`❌ Erreur: ${error.message}`);
        return false;
    }
}

// Test des boutons d'action
async function testActionButtons() {
    console.log('\n🔘 Test des endpoints des boutons d\'action...\n');
    
    const backendUrl = 'http://127.0.0.1:8000/api';
    
    const endpoints = [
        { name: 'Ventes (Sales)', url: '/sales/', button: 'Nouvelle vente' },
        { name: 'Produits (Products)', url: '/products/', button: 'Ajouter produit' },
        { name: 'Rapport quotidien', url: '/reports/daily/', button: 'Rapport quotidien' },
        { name: 'Approvisionnements', url: '/supplies/', button: 'Réapprovisionnement' }
    ];
    
    for (const endpoint of endpoints) {
        try {
            const response = await fetch(`${backendUrl}${endpoint.url}`);
            
            if (response.status === 401) {
                console.log(`🔒 ${endpoint.name}: Authentification requise (normal)`);
            } else if (response.ok) {
                console.log(`✅ ${endpoint.name}: Accessible`);
            } else {
                console.log(`⚠️  ${endpoint.name}: Status ${response.status}`);
            }
        } catch (error) {
            console.log(`❌ ${endpoint.name}: Erreur - ${error.message}`);
        }
    }
}

// Exécuter tous les tests
async function runFinalTests() {
    console.log('🧪 TESTS FINAUX DU DASHBOARD');
    console.log('=' * 60);
    
    const dashboardSuccess = await testFinalDashboard();
    await testActionButtons();
    
    console.log('\n' + '=' * 60);
    if (dashboardSuccess) {
        console.log('🎉 DASHBOARD ENTIÈREMENT FONCTIONNEL !');
        console.log('📱 Vous pouvez maintenant utiliser toutes les fonctionnalités');
    } else {
        console.log('⚠️  Quelques ajustements peuvent encore être nécessaires');
    }
}

runFinalTests();
