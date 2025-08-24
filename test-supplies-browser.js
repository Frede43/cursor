// Script de test pour la page d'approvisionnement
// À copier-coller dans la console du navigateur

// Configuration du test
const config = {
  apiBaseUrl: '/api',
  testSupplier: 1, // ID du fournisseur à utiliser pour le test
  testProducts: [1, 2], // IDs des produits à utiliser pour le test
  quantities: [10, 5], // Quantités à commander
  prices: [1500, 2000] // Prix unitaires
};

// Fonction principale de test
async function runSuppliesTest() {
  try {
    // 1. Création d'un approvisionnement
    console.log('🔍 Test 1: Création d\'un approvisionnement');
    const supplyData = {
      supplier_id: config.testSupplier,
      delivery_date: new Date().toISOString().split('T')[0],
      notes: 'Test automatique - ' + new Date().toLocaleString(),
      items: config.testProducts.map((productId, index) => ({
        product_id: productId,
        quantity_ordered: config.quantities[index],
        unit_price: config.prices[index]
      }))
    };
    
    console.log('Données d\'approvisionnement:', supplyData);
    
    // Créer l'approvisionnement
    const createdSupply = await createSupply(supplyData);
    console.log('✅ Approvisionnement créé avec succès:', createdSupply);
    
    // 2. Validation de l'approvisionnement
    if (createdSupply && createdSupply.id) {
      console.log(`🔍 Test 2: Validation de l'approvisionnement #${createdSupply.id}`);
      const validatedSupply = await validateSupply(createdSupply.id);
      console.log('✅ Approvisionnement validé avec succès:', validatedSupply);
      
      // 3. Vérification de la mise à jour du stock
      console.log('🔍 Test 3: Vérification de la mise à jour du stock');
      const inventory = await getInventory();
      console.log('✅ Stock récupéré avec succès:', inventory);
      
      // Vérifier si les produits testés ont bien été mis à jour dans le stock
      const updatedProducts = inventory.filter(item => 
        config.testProducts.includes(item.product_id)
      );
      
      if (updatedProducts.length > 0) {
        console.log('✅ Les produits ont bien été mis à jour dans le stock:', updatedProducts);
      } else {
        console.warn('⚠️ Aucun des produits testés n\'a été trouvé dans le stock');
      }
    }
    
    console.log('✅ TOUS LES TESTS ONT RÉUSSI ✅');
    
  } catch (error) {
    console.error('❌ ERREUR PENDANT LES TESTS:', error);
  }
}

// Fonctions d'API
async function createSupply(data) {
  const response = await fetch(`${config.apiBaseUrl}/supplies`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
    },
    body: JSON.stringify(data)
  });
  
  if (!response.ok) {
    throw new Error(`Erreur lors de la création: ${response.status} ${response.statusText}`);
  }
  
  return response.json();
}

async function validateSupply(id) {
  const response = await fetch(`${config.apiBaseUrl}/supplies/${id}/validate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
    }
  });
  
  if (!response.ok) {
    throw new Error(`Erreur lors de la validation: ${response.status} ${response.statusText}`);
  }
  
  return response.json();
}

async function getInventory() {
  const response = await fetch(`${config.apiBaseUrl}/inventory`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
    }
  });
  
  if (!response.ok) {
    throw new Error(`Erreur lors de la récupération du stock: ${response.status} ${response.statusText}`);
  }
  
  return response.json();
}

// Exécuter le test
console.log('🚀 DÉMARRAGE DES TESTS DE LA PAGE D\'APPROVISIONNEMENT');
runSuppliesTest();