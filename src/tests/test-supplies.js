// Script de test pour la page d'approvisionnement
// Ce script simule les interactions avec la page d'approvisionnement
// Pour l'exécuter, copiez tout le contenu et collez-le dans la console du navigateur

// Fonction pour simuler la création d'un approvisionnement
function testCreateSupply() {
  console.log('=== Test de création d\'approvisionnement ===');
  
  // Simuler les données d'un nouvel approvisionnement
  const newSupply = {
    supplier_id: 1, // ID du premier fournisseur
    delivery_date: new Date().toISOString().split('T')[0],
    notes: 'Test automatique de création d\'approvisionnement',
    items: [
      {
        product_id: 1, // ID du premier produit
        quantity_ordered: 10,
        unit_price: 1500
      },
      {
        product_id: 2, // ID du deuxième produit
        quantity_ordered: 5,
        unit_price: 2000
      }
    ]
  };
  
  console.log('Données de test:', newSupply);
  
  // Simuler l'appel API pour créer un approvisionnement
  fetch('/api/supplies', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
    },
    body: JSON.stringify(newSupply)
  })
  .then(response => {
    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }
    return response.json();
  })
  .then(data => {
    console.log('✅ Approvisionnement créé avec succès:', data);
    
    // Tester la validation de l'approvisionnement créé
    if (data && data.id) {
      testValidateSupply(data.id);
    }
  })
  .catch(error => {
    console.error('❌ Erreur lors de la création de l\'approvisionnement:', error);
  });
}

// Fonction pour simuler la validation d'un approvisionnement
function testValidateSupply(supplyId) {
  console.log(`=== Test de validation d'approvisionnement (ID: ${supplyId}) ===`);
  
  // Simuler l'appel API pour valider un approvisionnement
  fetch(`/api/supplies/${supplyId}/validate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
    }
  })
  .then(response => {
    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }
    return response.json();
  })
  .then(data => {
    console.log('✅ Approvisionnement validé avec succès:', data);
    
    // Vérifier la mise à jour du stock
    testCheckInventoryUpdate();
  })
  .catch(error => {
    console.error('❌ Erreur lors de la validation de l\'approvisionnement:', error);
  });
}

// Fonction pour vérifier la mise à jour du stock
function testCheckInventoryUpdate() {
  console.log('=== Test de vérification de la mise à jour du stock ===');
  
  // Simuler l'appel API pour récupérer les données de stock
  fetch('/api/inventory', {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
    }
  })
  .then(response => {
    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }
    return response.json();
  })
  .then(data => {
    console.log('✅ Données de stock récupérées avec succès:', data);
    console.log('Vérifiez que les quantités ont été mises à jour correctement.');
  })
  .catch(error => {
    console.error('❌ Erreur lors de la récupération des données de stock:', error);
  });
}

// Exécuter les tests
console.log('Démarrage des tests de la page d\'approvisionnement...');
testCreateSupply();

// Instructions pour exécuter ce script
console.log(`
=== Instructions d'utilisation ===
1. Assurez-vous d'être connecté à l'application
2. Ouvrez la console du navigateur (F12)
3. Copiez-collez ce script dans la console
4. Appuyez sur Entrée pour exécuter les tests
5. Vérifiez les résultats dans la console
`);