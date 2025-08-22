// Test de l'API Orders pour vérifier les données

async function testOrdersAPI() {
    try {
        const response = await fetch('http://127.0.0.1:8000/api/orders/orders/');
        
        if (!response.ok) {
            console.log(`❌ Erreur HTTP: ${response.status} ${response.statusText}`);
            return;
        }
        
        const data = await response.json();
        
        console.log('🎯 DONNÉES ORDERS API:');
        console.log('=' * 50);
        
        if (data.results && data.results.length > 0) {
            console.log(`📊 Nombre de commandes: ${data.results.length}`);
            
            data.results.forEach((order, index) => {
                console.log(`\n📋 Commande ${index + 1}:`);
                console.log(`   • Numéro: ${order.order_number}`);
                console.log(`   • Table: ${order.table ? order.table.number : 'N/A'}`);
                console.log(`   • Statut: ${order.status}`);
                console.log(`   • Priorité: ${order.priority}`);
                console.log(`   • Montant: ${order.total_amount} BIF`);
                console.log(`   • Serveur: ${order.server ? order.server.first_name + ' ' + order.server.last_name : 'N/A'}`);
                console.log(`   • Items: ${order.items ? order.items.length : 0} articles`);
            });
            
            console.log('\n✅ API Orders fonctionne correctement !');
            console.log(`📈 Total commandes: ${data.results.length}`);
            
        } else {
            console.log('❌ Aucune commande trouvée');
        }
        
    } catch (error) {
        console.log(`❌ Erreur: ${error.message}`);
    }
}

testOrdersAPI();
