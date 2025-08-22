// Test détaillé de l'API pour vérifier toutes les données

async function testDetailedAPI() {
    try {
        const response = await fetch('http://127.0.0.1:8000/api/reports/dashboard/stats/');
        const data = await response.json();
        
        console.log('🎯 DONNÉES DASHBOARD DÉTAILLÉES:');
        console.log('=' * 50);
        
        // Données principales
        console.log(`📅 Date: ${data.today.date}`);
        console.log(`💰 Revenus du jour: ${data.today.daily_revenue.toLocaleString()} BIF`);
        console.log(`📦 Produits vendus (types): ${data.today.products_sold.length}`);
        
        // Nouvelles données
        console.log(`🛒 Commandes (sales): ${data.today.sales}`);
        console.log(`⏳ Commandes en attente: ${data.today.pending_sales}`);
        
        // Tables
        if (data.quick_stats.occupied_tables !== undefined) {
            console.log(`🪑 Tables occupées: ${data.quick_stats.occupied_tables}/${data.quick_stats.total_tables}`);
        } else {
            console.log(`❌ Tables occupées: données manquantes`);
        }
        
        // Autres stats
        console.log(`🏪 Produits en stock: ${data.quick_stats.total_products}`);
        console.log(`🚨 Alertes: ${data.alerts.total_unresolved}`);
        
        console.log('\n✅ Résumé pour le Dashboard:');
        console.log(`   • Ventes du jour: ${data.today.daily_revenue.toLocaleString()} BIF ✅`);
        console.log(`   • Commandes: ${data.today.sales} ✅`);
        console.log(`   • Produits en stock: ${data.quick_stats.total_products} ✅`);
        console.log(`   • Alertes: ${data.alerts.total_unresolved} ✅`);
        if (data.quick_stats.occupied_tables !== undefined) {
            console.log(`   • Tables occupées: ${data.quick_stats.occupied_tables}/${data.quick_stats.total_tables} ✅`);
        }
        
    } catch (error) {
        console.log(`❌ Erreur: ${error.message}`);
    }
}

testDetailedAPI();
