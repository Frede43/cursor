// Test direct de l'API pour voir exactement ce qui est retourné

async function testAPIDirect() {
    console.log('🔍 Test direct de l\'API Dashboard...\n');
    
    try {
        const response = await fetch('http://127.0.0.1:8000/api/reports/dashboard/stats/');
        
        if (response.ok) {
            const data = await response.json();
            
            console.log('📡 Réponse brute de l\'API:');
            console.log(JSON.stringify(data, null, 2));
            
            console.log('\n🔍 Analyse détaillée:');
            console.log(`• today.sales: ${data.today?.sales} (type: ${typeof data.today?.sales})`);
            console.log(`• today.revenue: ${data.today?.revenue} (type: ${typeof data.today?.revenue})`);
            console.log(`• today.daily_revenue: ${data.today?.daily_revenue} (type: ${typeof data.today?.daily_revenue})`);
            console.log(`• products_sold length: ${data.today?.products_sold?.length || 0}`);
            
            // Vérifier si les données sont cohérentes
            const hasProducts = data.today?.products_sold?.length > 0;
            const hasRevenue = data.today?.daily_revenue > 0;
            const hasSales = data.today?.sales > 0;
            
            console.log('\n📊 Cohérence des données:');
            console.log(`• Produits vendus: ${hasProducts ? '✅' : '❌'}`);
            console.log(`• Revenus détaillés: ${hasRevenue ? '✅' : '❌'}`);
            console.log(`• Nombre de ventes: ${hasSales ? '✅' : '❌'}`);
            
            if (hasProducts && hasRevenue && !hasSales) {
                console.log('\n🔧 PROBLÈME IDENTIFIÉ:');
                console.log('Les données de vente existent mais le compteur sales est à 0');
                console.log('Cela indique un problème dans l\'API backend');
            }
            
        } else {
            console.log(`❌ Erreur HTTP: ${response.status}`);
            const text = await response.text();
            console.log(`Réponse: ${text}`);
        }
        
    } catch (error) {
        console.log(`❌ Erreur: ${error.message}`);
    }
}

testAPIDirect();
