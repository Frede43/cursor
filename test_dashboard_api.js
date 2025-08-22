// Test de l'API du dashboard pour diagnostiquer pourquoi les valeurs sont à 0

async function testDashboardAPI() {
    console.log('🔍 Test de l\'API Dashboard...\n');
    
    const backendUrl = 'http://127.0.0.1:8000/api';
    
    try {
        // Test de l'API dashboard stats
        console.log('📡 Test /reports/dashboard/stats/');
        const response = await fetch(`${backendUrl}/reports/dashboard/stats/`);
        
        console.log(`Status: ${response.status}`);
        
        if (response.ok) {
            const data = await response.json();
            console.log('✅ Données reçues:');
            console.log(JSON.stringify(data, null, 2));
            
            // Analyser les données
            console.log('\n📊 Analyse des données:');
            console.log(`• Date: ${data.today?.date}`);
            console.log(`• Ventes du jour: ${data.today?.sales || 0}`);
            console.log(`• Revenus du jour: ${data.today?.revenue || 0} BIF`);
            console.log(`• Commandes en cours: ${data.today?.pending_sales || 0}`);
            console.log(`• Produits actifs: ${data.quick_stats?.total_products || 0}`);
            console.log(`• Alertes actives: ${data.alerts?.total_unresolved || 0}`);
            console.log(`• Stock bas: ${data.alerts?.low_stock || 0}`);
            console.log(`• Rupture de stock: ${data.alerts?.out_of_stock || 0}`);
            
            // Vérifier pourquoi les valeurs sont à 0
            if (data.today?.sales === 0) {
                console.log('\n⚠️  Ventes à 0 - Causes possibles:');
                console.log('   • Aucune vente enregistrée aujourd\'hui');
                console.log('   • Problème avec le modèle DailyReport');
                console.log('   • Données de test manquantes');
            }
            
            if (data.quick_stats?.total_products === 0) {
                console.log('\n⚠️  Produits à 0 - Causes possibles:');
                console.log('   • Aucun produit actif en base');
                console.log('   • Problème de requête SQL');
            }
            
            return data;
        } else {
            console.log(`❌ Erreur API: ${response.status}`);
            const errorText = await response.text();
            console.log(`Réponse: ${errorText}`);
            return null;
        }
        
    } catch (error) {
        console.log(`❌ Erreur: ${error.message}`);
        return null;
    }
}

async function testRelatedAPIs() {
    console.log('\n🔍 Test des APIs connexes...\n');
    
    const backendUrl = 'http://127.0.0.1:8000/api';
    
    const endpoints = [
        { name: 'Produits', url: '/products/', expectAuth: true },
        { name: 'Rapports journaliers', url: '/reports/daily/', expectAuth: false },
        { name: 'Rapport détaillé', url: '/reports/daily-detailed/2025-08-18/', expectAuth: false },
        { name: 'Alertes', url: '/reports/alerts/unresolved/', expectAuth: false }
    ];
    
    for (const endpoint of endpoints) {
        try {
            console.log(`📡 Test ${endpoint.name}: ${endpoint.url}`);
            const response = await fetch(`${backendUrl}${endpoint.url}`);
            
            if (response.ok) {
                const data = await response.json();
                console.log(`   ✅ Status: ${response.status}`);
                
                if (data.results) {
                    console.log(`   📦 Résultats: ${data.results.length} éléments`);
                } else if (Array.isArray(data)) {
                    console.log(`   📦 Résultats: ${data.length} éléments`);
                } else if (data.count !== undefined) {
                    console.log(`   📦 Count: ${data.count}`);
                } else {
                    console.log(`   📦 Données: ${Object.keys(data).join(', ')}`);
                }
            } else {
                console.log(`   ❌ Status: ${response.status}`);
                if (response.status === 401 && endpoint.expectAuth) {
                    console.log(`   💡 Authentification requise (normal)`);
                }
            }
        } catch (error) {
            console.log(`   💥 Erreur: ${error.message}`);
        }
        console.log('');
    }
}

async function suggestFixes(dashboardData) {
    console.log('\n🔧 Suggestions de correction...\n');
    
    if (!dashboardData) {
        console.log('❌ Impossible d\'analyser - API dashboard non accessible');
        return;
    }
    
    const issues = [];
    const fixes = [];
    
    // Vérifier les ventes
    if (dashboardData.today?.sales === 0) {
        issues.push('Ventes du jour à 0');
        fixes.push('Créer des données de vente de test');
        fixes.push('Vérifier le modèle DailyReport');
    }
    
    // Vérifier les produits
    if (dashboardData.quick_stats?.total_products === 0) {
        issues.push('Aucun produit actif');
        fixes.push('Ajouter des produits via l\'admin Django');
        fixes.push('Vérifier le champ is_active des produits');
    }
    
    // Vérifier les alertes
    if (dashboardData.alerts?.total_unresolved === 0) {
        issues.push('Aucune alerte (peut être normal)');
    }
    
    console.log('🔍 Problèmes détectés:');
    issues.forEach((issue, i) => console.log(`   ${i + 1}. ${issue}`));
    
    console.log('\n💡 Actions recommandées:');
    fixes.forEach((fix, i) => console.log(`   ${i + 1}. ${fix}`));
    
    console.log('\n📋 Étapes immédiates:');
    console.log('   1. Vérifier les données en base via l\'admin Django');
    console.log('   2. Créer des données de test si nécessaire');
    console.log('   3. Redémarrer le serveur Django');
    console.log('   4. Rafraîchir le dashboard frontend');
}

// Exécuter les tests
async function runAllTests() {
    console.log('🧪 Diagnostic complet du Dashboard');
    console.log('=' * 50);
    
    // Test principal
    const dashboardData = await testDashboardAPI();
    
    // Tests connexes
    await testRelatedAPIs();
    
    // Suggestions
    await suggestFixes(dashboardData);
}

runAllTests();
