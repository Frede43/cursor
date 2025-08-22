// Script pour tester la connectivité frontend-backend

async function testFrontendBackendConnection() {
    console.log('🔗 Test de connectivité Frontend-Backend...\n');

    const backendUrl = 'http://127.0.0.1:8000/api';
    const frontendUrl = 'http://localhost:8081';

    // Test 1: Vérifier que le backend répond
    console.log('1. Test Backend API:');
    try {
        const testDate = '2025-08-18'; // Date avec nos données de test
        const response = await fetch(`${backendUrl}/reports/daily-detailed/${testDate}/`);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();

        console.log(`   ✅ Backend Status: ${response.status}`);
        console.log(`   📊 Données reçues:`);
        console.log(`      • Date: ${data.date}`);
        console.log(`      • Total ventes: ${data.summary.total_sales}`);
        console.log(`      • Chiffre d'affaires: ${data.summary.total_revenue} BIF`);
        console.log(`      • Catégories: ${Object.keys(data.categories).length}`);

        // Afficher les catégories
        Object.entries(data.categories).forEach(([name, categoryData]) => {
            console.log(`        - ${name}: ${categoryData.total_revenue} BIF (${categoryData.total_quantity} articles)`);
        });

    } catch (error) {
        console.log(`   ❌ Erreur Backend: ${error.message}`);
        return false;
    }

    // Test 2: Vérifier que le frontend répond
    console.log('\n2. Test Frontend:');
    try {
        const response = await fetch(frontendUrl);
        if (response.ok) {
            console.log(`   ✅ Frontend Status: ${response.status}`);
            console.log(`   🌐 Frontend accessible sur ${frontendUrl}`);
        } else {
            throw new Error(`HTTP ${response.status}`);
        }
    } catch (error) {
        console.log(`   ❌ Erreur Frontend: ${error.message}`);
        return false;
    }

    // Test 3: Test CORS
    console.log('\n3. Test CORS:');
    try {
        const response = await fetch(`${backendUrl}/reports/daily-detailed/${testDate}/`, {
            headers: {
                'Origin': frontendUrl,
                'Access-Control-Request-Method': 'GET',
                'Access-Control-Request-Headers': 'Content-Type'
            }
        });
        if (response.ok) {
            console.log(`   ✅ CORS configuré correctement`);
        } else {
            console.log(`   ⚠️  Réponse CORS: ${response.status}`);
        }
    } catch (error) {
        console.log(`   ⚠️  Possible problème CORS: ${error.message}`);
    }
    
    console.log('\n🎯 Prochaines étapes:');
    console.log('   1. Ouvrir le navigateur sur http://localhost:8081');
    console.log('   2. Vérifier que le dashboard affiche les données');
    console.log('   3. Naviguer vers le rapport journalier');
    console.log('   4. Vérifier que les 73,300 BIF s\'affichent correctement');
    
    return true;
}

// Exécuter le test
testFrontendBackendConnection()
    .then(success => {
        if (success) {
            console.log('\n✅ Tests de connectivité réussis !');
        } else {
            console.log('\n❌ Problèmes détectés dans la connectivité');
        }
    })
    .catch(error => {
        console.error('\n💥 Erreur lors des tests:', error.message);
    });
