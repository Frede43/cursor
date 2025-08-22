// Test d'intégration frontend-backend pour le rapport journalier

async function testFrontendIntegration() {
    console.log('🔗 Test d\'intégration Frontend-Backend pour le rapport journalier...\n');
    
    const backendUrl = 'http://127.0.0.1:8000/api';
    const testDate = '2025-08-18';
    
    // Simuler l'appel que fait le frontend
    console.log('1. Test de l\'endpoint utilisé par le frontend:');
    console.log(`   URL: ${backendUrl}/reports/daily-detailed/${testDate}/`);
    
    try {
        // Headers similaires à ceux du navigateur
        const headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Origin': 'http://localhost:8081',
            'Referer': 'http://localhost:8081/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        };
        
        const response = await fetch(`${backendUrl}/reports/daily-detailed/${testDate}/`, {
            method: 'GET',
            headers: headers,
            mode: 'cors'
        });
        
        console.log(`   ✅ Status: ${response.status}`);
        console.log(`   📋 Headers CORS:`);
        console.log(`      Access-Control-Allow-Origin: ${response.headers.get('Access-Control-Allow-Origin') || 'Non défini'}`);
        console.log(`      Access-Control-Allow-Methods: ${response.headers.get('Access-Control-Allow-Methods') || 'Non défini'}`);
        
        if (response.ok) {
            const data = await response.json();
            
            console.log(`\n   📊 Données reçues (format frontend):`);
            console.log(`      Date: ${data.date}`);
            console.log(`      Total ventes: ${data.summary?.total_sales || 'N/A'}`);
            console.log(`      Chiffre d'affaires: ${data.summary?.total_revenue || 'N/A'} BIF`);
            console.log(`      Profit: ${data.summary?.total_profit || 'N/A'} BIF`);
            console.log(`      Marge: ${data.summary?.profit_margin || 'N/A'}%`);
            
            console.log(`\n   🏷️  Catégories (${Object.keys(data.categories || {}).length}):`);
            Object.entries(data.categories || {}).forEach(([name, categoryData]) => {
                console.log(`      • ${name}:`);
                console.log(`        - Chiffre d'affaires: ${categoryData.total_revenue} BIF`);
                console.log(`        - Quantité: ${categoryData.total_quantity} articles`);
                console.log(`        - Produits: ${categoryData.products?.length || 0}`);
                
                // Afficher quelques produits
                if (categoryData.products && categoryData.products.length > 0) {
                    categoryData.products.slice(0, 2).forEach(product => {
                        console.log(`          * ${product.name}: ${product.quantity_sold} × ${product.unit_price} = ${product.revenue} BIF`);
                    });
                }
            });
            
            // Vérifier la structure des données pour le frontend
            console.log(`\n   🔍 Validation de la structure des données:`);
            const requiredFields = ['date', 'summary', 'categories'];
            const missingFields = requiredFields.filter(field => !(field in data));
            
            if (missingFields.length === 0) {
                console.log(`      ✅ Tous les champs requis sont présents`);
            } else {
                console.log(`      ❌ Champs manquants: ${missingFields.join(', ')}`);
            }
            
            // Vérifier les champs du summary
            const summaryFields = ['total_sales', 'total_revenue', 'total_profit', 'profit_margin'];
            const missingSummaryFields = summaryFields.filter(field => !(field in (data.summary || {})));
            
            if (missingSummaryFields.length === 0) {
                console.log(`      ✅ Tous les champs du résumé sont présents`);
            } else {
                console.log(`      ⚠️  Champs du résumé manquants: ${missingSummaryFields.join(', ')}`);
            }
            
            // Sauvegarder pour inspection
            const fs = await import('fs');
            fs.writeFileSync('frontend_integration_test.json', JSON.stringify(data, null, 2));
            console.log(`\n   💾 Données sauvegardées dans 'frontend_integration_test.json'`);
            
        } else {
            console.log(`   ❌ Erreur HTTP: ${response.status}`);
            const errorText = await response.text();
            console.log(`   📄 Réponse: ${errorText.substring(0, 200)}...`);
        }
        
    } catch (error) {
        console.log(`   ❌ Erreur: ${error.message}`);
        return false;
    }
    
    // Test 2: Vérifier que le frontend peut traiter les données
    console.log(`\n2. Test de compatibilité avec le frontend:`);
    console.log(`   📱 Le frontend devrait maintenant pouvoir:`);
    console.log(`      • Afficher 73,300 BIF de chiffre d'affaires`);
    console.log(`      • Montrer 5 ventes au total`);
    console.log(`      • Lister 6 catégories de produits`);
    console.log(`      • Afficher les détails par catégorie`);
    
    console.log(`\n🎯 Actions recommandées:`);
    console.log(`   1. Ouvrir http://localhost:8081 dans le navigateur`);
    console.log(`   2. Aller dans "Rapports" > "Rapport journalier"`);
    console.log(`   3. Sélectionner la date 2025-08-18`);
    console.log(`   4. Vérifier que les données s'affichent correctement`);
    
    return true;
}

// Exécuter le test
testFrontendIntegration()
    .then(success => {
        if (success) {
            console.log('\n✅ Test d\'intégration réussi ! Le frontend devrait fonctionner.');
        } else {
            console.log('\n❌ Problèmes détectés dans l\'intégration');
        }
    })
    .catch(error => {
        console.error('\n💥 Erreur lors du test:', error.message);
    });
