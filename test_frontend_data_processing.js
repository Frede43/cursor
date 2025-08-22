// Test du traitement des données par le frontend

async function testFrontendDataProcessing() {
    console.log('🔍 Test du traitement des données par le frontend...\n');
    
    const backendUrl = 'http://127.0.0.1:8000/api';
    const testDate = '2025-08-18';
    
    try {
        // Récupérer les données de l'API
        const response = await fetch(`${backendUrl}/reports/daily-detailed/${testDate}/`);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const apiData = await response.json();
        console.log('✅ Données récupérées de l\'API');
        console.log('📊 Structure des données:');
        console.log(`   • Date: ${apiData.date}`);
        console.log(`   • Summary présent: ${!!apiData.summary}`);
        console.log(`   • Categories présentes: ${!!apiData.categories}`);
        console.log(`   • Nombre de catégories: ${Object.keys(apiData.categories || {}).length}`);
        
        if (apiData.summary) {
            console.log('📈 Résumé:');
            console.log(`   • total_sales: ${apiData.summary.total_sales} (type: ${typeof apiData.summary.total_sales})`);
            console.log(`   • total_revenue: ${apiData.summary.total_revenue}`);
            console.log(`   • total_profit: ${apiData.summary.total_profit}`);
        }
        
        // Simuler le traitement du frontend
        console.log('\n🔄 Simulation du traitement frontend...');
        
        // Test de la condition du frontend
        const condition1 = apiData && apiData.summary && apiData.categories;
        const condition2 = apiData && apiData.summary?.total_sales > 0;
        
        console.log(`   • Condition simplifiée (summary && categories): ${condition1}`);
        console.log(`   • Condition originale (total_sales > 0): ${condition2}`);
        
        if (condition1) {
            // Simuler la transformation des données
            const products = Object.entries(apiData.categories || {}).flatMap(([categoryName, category]) => 
                category.products?.map((p) => ({
                    id: p.name || 'unknown',
                    name: p.name || 'Produit inconnu',
                    initialStock: p.initial_stock || 0,
                    incoming: p.incoming || 0,
                    outgoing: p.quantity_sold || 0,
                    finalStock: p.final_stock || 0,
                    price: p.unit_price || 0,
                    costPrice: p.cost_price || 0,
                    totalSales: p.quantity_sold || 0,
                    revenue: p.revenue || 0,
                    totalCost: p.total_cost || 0,
                    profit: p.profit || 0,
                    profitMargin: p.profit_margin || 0,
                    category: categoryName
                })) || []
            ) || [];
            
            console.log(`   ✅ Transformation réussie: ${products.length} produits`);
            
            // Afficher quelques produits
            console.log('\n📦 Premiers produits transformés:');
            products.slice(0, 3).forEach((product, index) => {
                console.log(`   ${index + 1}. ${product.name} (${product.category})`);
                console.log(`      • Stock: ${product.initialStock} → ${product.finalStock} (vendu: ${product.outgoing})`);
                console.log(`      • Prix: PA=${product.costPrice} FBu, PV=${product.price} FBu`);
                console.log(`      • CA: ${product.revenue} FBu, Bénéfice: ${product.profit} FBu`);
            });
            
            // Vérifier les catégories
            const categories = [...new Set(products.map(p => p.category))];
            console.log(`\n🏷️  Catégories détectées (${categories.length}): ${categories.join(', ')}`);
            
            return true;
        } else {
            console.log('   ❌ Les conditions du frontend ne sont pas remplies');
            return false;
        }
        
    } catch (error) {
        console.log(`❌ Erreur: ${error.message}`);
        return false;
    }
}

// Exécuter le test
testFrontendDataProcessing()
    .then(success => {
        if (success) {
            console.log('\n🎉 Le traitement des données devrait fonctionner !');
            console.log('💡 Si le tableau reste vide, le problème est ailleurs (rendu React, etc.)');
        } else {
            console.log('\n💥 Problème dans le traitement des données');
        }
    })
    .catch(error => {
        console.error('\n💥 Erreur lors du test:', error.message);
    });
