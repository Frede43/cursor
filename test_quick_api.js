// Test rapide de l'API pour vérifier les données

async function quickTest() {
    try {
        const response = await fetch('http://127.0.0.1:8000/api/reports/dashboard/stats/');
        const data = await response.json();
        
        console.log('🎯 DONNÉES DASHBOARD:');
        console.log(`📅 Date: ${data.today.date}`);
        console.log(`💰 Revenus: ${data.today.daily_revenue.toLocaleString()} BIF`);
        console.log(`📦 Produits vendus: ${data.today.products_sold.length} types`);
        console.log(`🏪 Produits en stock: ${data.quick_stats.total_products}`);
        console.log(`🚨 Alertes: ${data.alerts.total_unresolved}`);
        
        console.log('\n✅ Ces valeurs devraient apparaître dans le dashboard après rafraîchissement !');
        
    } catch (error) {
        console.log(`❌ Erreur: ${error.message}`);
    }
}

quickTest();
