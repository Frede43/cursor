// Test de la nouvelle API Dashboard avec les données Orders

async function testNewDashboardAPI() {
    try {
        const response = await fetch('http://127.0.0.1:8000/api/reports/dashboard/stats/');
        const data = await response.json();
        
        console.log('🎯 NOUVELLES DONNÉES DASHBOARD:');
        console.log('=' * 50);
        
        // Données principales
        console.log(`📅 Date: ${data.today.date}`);
        console.log(`💰 Revenus du jour: ${data.today.daily_revenue.toLocaleString()} BIF`);
        
        // Nouvelles données Orders vs Sales
        console.log(`\n📊 COMMANDES vs VENTES:`);
        console.log(`   🛒 Orders (vraies commandes): ${data.today.orders || 'N/A'}`);
        console.log(`   💳 Sales (ventes complétées): ${data.today.sales || 'N/A'}`);
        console.log(`   ⏳ Commandes en attente: ${data.today.pending_orders || 'N/A'}`);
        console.log(`   📦 Produits vendus (types): ${data.today.products_sold.length}`);
        
        // Tables
        console.log(`\n🪑 TABLES:`);
        console.log(`   Tables occupées: ${data.quick_stats.occupied_tables}/${data.quick_stats.total_tables}`);
        
        // Autres stats
        console.log(`\n📈 AUTRES STATS:`);
        console.log(`   🏪 Produits en stock: ${data.quick_stats.total_products}`);
        console.log(`   🚨 Alertes: ${data.alerts.total_unresolved}`);
        
        console.log('\n✅ RÉSUMÉ POUR LE DASHBOARD:');
        console.log(`   • Ventes du jour: ${data.today.daily_revenue.toLocaleString()} BIF ✅`);
        console.log(`   • Commandes: ${data.today.orders} ✅ (au lieu de ${data.today.sales})`);
        console.log(`   • Produits en stock: ${data.quick_stats.total_products} ✅`);
        console.log(`   • Alertes: ${data.alerts.total_unresolved} ✅`);
        console.log(`   • Tables occupées: ${data.quick_stats.occupied_tables}/${data.quick_stats.total_tables} ✅`);
        
    } catch (error) {
        console.log(`❌ Erreur: ${error.message}`);
    }
}

testNewDashboardAPI();
