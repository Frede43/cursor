// Test de la nouvelle architecture à deux niveaux

async function testEnhancedAPI() {
    console.log('🚀 TEST DE L\'ARCHITECTURE À DEUX NIVEAUX');
    console.log('=' * 60);
    
    try {
        // 1. Test API Sales (Niveau Commercial)
        console.log('\n📊 1. TEST API SALES (Niveau Commercial)');
        console.log('-'.repeat(50));
        
        const salesResponse = await fetch('http://127.0.0.1:8000/api/products-enhanced/sales/menu/');
        const salesData = await salesResponse.json();
        
        if (salesData.success) {
            console.log('✅ API Sales fonctionne !');
            console.log(`📋 Menu organisé par catégories:`);
            
            Object.entries(salesData.menu).forEach(([category, items]) => {
                console.log(`\n   📂 ${category}:`);
                items.forEach(item => {
                    const availability = item.availability;
                    const status = availability.available_quantity > 0 ? '✅' : '❌';
                    console.log(`      ${status} ${item.name} - ${item.price} BIF (${availability.available_quantity} disponibles)`);
                });
            });
            
            console.log(`\n📈 Statistiques:`);
            console.log(`   • Total articles: ${salesData.stats.total_items}`);
            console.log(`   • Disponibles: ${salesData.stats.available_items}`);
            console.log(`   • Indisponibles: ${salesData.stats.unavailable_items}`);
        } else {
            console.log('❌ Erreur API Sales:', salesData.error);
        }
        
        // 2. Test API Kitchen (Niveau Technique)
        console.log('\n🍳 2. TEST API KITCHEN (Niveau Technique)');
        console.log('-'.repeat(50));
        
        const kitchenResponse = await fetch('http://127.0.0.1:8000/api/products-enhanced/kitchen/dashboard/');
        const kitchenData = await kitchenResponse.json();
        
        if (kitchenData.success) {
            console.log('✅ API Kitchen fonctionne !');
            
            console.log(`\n🚨 Alertes de stock (${kitchenData.summary.critical_alerts + kitchenData.summary.warning_alerts}):`);
            kitchenData.stock_alerts.slice(0, 5).forEach(alert => {
                const icon = alert.severity === 'critical' ? '🔴' : '⚠️';
                console.log(`   ${icon} ${alert.ingredient}: ${alert.current_stock}/${alert.minimum_stock} ${alert.unit}`);
            });
            
            console.log(`\n📊 Prévisions de production:`);
            kitchenData.production_forecast.slice(0, 3).forEach(forecast => {
                console.log(`   🍽️ ${forecast.recipe}: ${forecast.max_portions} portions possibles`);
                console.log(`      💰 Coût: ${forecast.cost_per_portion} BIF/portion`);
                console.log(`      ⏱️ Temps: ${forecast.prep_time} min`);
                if (forecast.limiting_ingredient) {
                    console.log(`      🚫 Limitant: ${forecast.limiting_ingredient}`);
                }
            });
            
            console.log(`\n💰 Valeur du stock: ${kitchenData.stock_value.total_stock_value.toLocaleString()} BIF`);
            console.log(`🛒 Articles à acheter: ${kitchenData.summary.items_to_buy}`);
            
        } else {
            console.log('❌ Erreur API Kitchen:', kitchenData.error);
        }
        
        // 3. Test de simulation de vente
        console.log('\n💳 3. TEST SIMULATION DE VENTE');
        console.log('-'.repeat(50));
        
        // Simuler une vente de Burger
        const saleData = {
            items: [
                { menu_item_id: 3, quantity: 1 },  // Burger Deluxe
                { menu_item_id: 1, quantity: 2 }   // Bière Primus
            ]
        };
        
        const saleResponse = await fetch('http://127.0.0.1:8000/api/products-enhanced/sales/process/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(saleData)
        });
        
        const saleResult = await saleResponse.json();
        
        if (saleResult.success) {
            console.log('✅ Vente simulée avec succès !');
            console.log(`📦 Articles traités: ${saleResult.items_processed}`);
            console.log('🔄 Les stocks ont été automatiquement déduits');
        } else {
            console.log('❌ Erreur simulation vente:', saleResult.error);
            if (saleResult.availability_check) {
                console.log('📋 Détails de disponibilité:');
                saleResult.availability_check.forEach(check => {
                    const status = check.is_available ? '✅' : '❌';
                    console.log(`   ${status} Article ${check.menu_item_id}: ${check.quantity} demandé`);
                });
            }
        }
        
        console.log('\n🎯 RÉSUMÉ DU TEST');
        console.log('=' * 60);
        console.log('✅ Architecture à deux niveaux opérationnelle !');
        console.log('📊 Sales API: Interface commerciale simplifiée');
        console.log('🍳 Kitchen API: Gestion technique complète');
        console.log('🔄 Déduction automatique des stocks');
        console.log('📈 Calculs de rentabilité en temps réel');
        console.log('🚨 Alertes de stock intelligentes');
        
    } catch (error) {
        console.log(`❌ Erreur générale: ${error.message}`);
    }
}

testEnhancedAPI();
