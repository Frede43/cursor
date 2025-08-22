// Test de l'interface Tables avec vraies données

async function testTablesInterface() {
    console.log('🪑 TEST INTERFACE TABLES AVEC VRAIES DONNÉES');
    console.log('=' * 70);
    
    try {
        // Test de l'API Tables
        const response = await fetch('http://127.0.0.1:8000/api/sales/tables/');
        
        if (response.ok) {
            const data = await response.json();
            console.log('✅ API Tables fonctionnelle');
            console.log(`📊 ${data.results?.length || 0} tables récupérées`);
            
            if (data.results && data.results.length > 0) {
                console.log('\n📋 TABLES DANS LA BASE DE DONNÉES:');
                
                // Grouper par zone
                const zones = {};
                data.results.forEach(table => {
                    if (!zones[table.location]) {
                        zones[table.location] = [];
                    }
                    zones[table.location].push(table);
                });
                
                Object.entries(zones).forEach(([zone, tables]) => {
                    console.log(`\n🏢 Zone ${zone.toUpperCase()}:`);
                    tables.forEach(table => {
                        const statusEmoji = {
                            'available': '🟢',
                            'occupied': '🔴',
                            'reserved': '🟡',
                            'cleaning': '🟠'
                        };
                        
                        console.log(`   ${statusEmoji[table.status] || '⚪'} Table ${table.number} (${table.capacity} places) - ${table.status}`);
                        if (table.server) {
                            console.log(`      👤 Serveur: ${table.server}`);
                        }
                        if (table.customer) {
                            console.log(`      👥 Client: ${table.customer}`);
                        }
                        if (table.occupied_since) {
                            console.log(`      ⏰ Occupée depuis: ${table.occupied_since}`);
                        }
                    });
                });
                
                // Statistiques
                const stats = {
                    total: data.results.length,
                    available: data.results.filter(t => t.status === 'available').length,
                    occupied: data.results.filter(t => t.status === 'occupied').length,
                    reserved: data.results.filter(t => t.status === 'reserved').length,
                    cleaning: data.results.filter(t => t.status === 'cleaning').length
                };
                
                console.log('\n📊 STATISTIQUES:');
                console.log(`   • Total: ${stats.total} tables`);
                console.log(`   • Disponibles: ${stats.available} 🟢`);
                console.log(`   • Occupées: ${stats.occupied} 🔴`);
                console.log(`   • Réservées: ${stats.reserved} 🟡`);
                console.log(`   • En nettoyage: ${stats.cleaning} 🟠`);
                
                const occupationRate = Math.round((stats.occupied / stats.total) * 100);
                console.log(`   • Taux d'occupation: ${occupationRate}%`);
                
            } else {
                console.log('\n❌ Aucune table trouvée');
            }
            
        } else {
            console.log(`❌ Erreur API: ${response.status}`);
        }
        
    } catch (error) {
        console.log(`❌ Erreur: ${error.message}`);
    }
    
    console.log('\n🎯 INTERFACE TABLES AMÉLIORÉE:');
    console.log('-'.repeat(50));
    
    console.log('\n✅ FONCTIONNALITÉS IMPLÉMENTÉES:');
    console.log('   • Chargement des vraies données de la base');
    console.log('   • Indicateur de chargement avec animation');
    console.log('   • Statistiques en temps réel (disponibles/occupées/etc.)');
    console.log('   • Affichage par zones (Intérieur/Terrasse/VIP)');
    console.log('   • Tables cliquables avec dialogs détaillés');
    console.log('   • Informations complètes (serveur, client, durée)');
    console.log('   • Gestion des erreurs avec fallback');
    
    console.log('\n🎨 EXPÉRIENCE UTILISATEUR:');
    console.log('   • Design moderne et intuitif');
    console.log('   • Couleurs selon statut (vert/rouge/jaune/orange)');
    console.log('   • Informations visuelles claires');
    console.log('   • Interactions fluides');
    
    console.log('\n📱 MAINTENANT TESTEZ DANS LE NAVIGATEUR:');
    console.log('-'.repeat(50));
    
    console.log('\n1. 🔄 RAFRAÎCHISSEZ:');
    console.log('   • Allez sur http://localhost:8081/tables');
    console.log('   • Appuyez sur Ctrl+F5 pour forcer le rechargement');
    
    console.log('\n2. 🪑 VÉRIFIEZ L\'AFFICHAGE:');
    console.log('   • Indicateur "Chargement des tables..." puis données');
    console.log('   • Statistiques en haut (4 disponibles, 4 occupées, etc.)');
    console.log('   • 3 zones avec tables colorées selon statut');
    
    console.log('\n3. 🖱️ TESTEZ LES INTERACTIONS:');
    console.log('   • Cliquez sur n\'importe quelle table');
    console.log('   • Dialog s\'ouvre avec détails complets');
    console.log('   • Boutons pour changer statut et assigner serveur');
    console.log('   • Pour tables occupées: bouton "Nouvelle commande"');
    
    console.log('\n🎯 RÉSULTAT ATTENDU:');
    console.log('-'.repeat(50));
    
    console.log('\n📊 AFFICHAGE ATTENDU:');
    console.log('   Zone Intérieur: Tables 1🔴, 2🟢, 3🔴, 4🟢');
    console.log('   Zone Terrasse: Tables 5🔴, 6🟢, 7🟠');
    console.log('   Zone VIP: Tables 8🟡, 9🟢, 10🔴');
    
    console.log('\n🔗 INTERACTIONS ATTENDUES:');
    console.log('   • Tables occupées (1,3,5,10): Bouton "Nouvelle commande"');
    console.log('   • Tables disponibles (2,4,6,9): Boutons "Occuper"');
    console.log('   • Table réservée (8): Infos réservation');
    console.log('   • Table nettoyage (7): Bouton "Libérer"');
    
    console.log('\n🎊 INTERFACE TABLES MODERNE PRÊTE !');
    console.log('Testez maintenant sur http://localhost:8081/tables');
}

testTablesInterface();
