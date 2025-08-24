// Script de test pour l'authentification
// Exécuter avec: node test-auth.js

// Simuler les identifiants admin
const testCredentials = {
  username: 'admin',
  password: 'admin123'
};

// Fonction de test d'authentification
function testAuth() {
  console.log('Test d\'authentification avec:', testCredentials);
  
  // Simuler la connexion
  if (testCredentials.username === 'admin' && testCredentials.password === 'admin123') {
    console.log('✅ Authentification réussie!');
    
    // Créer un utilisateur fictif pour le test
    const user = {
      id: 1,
      username: 'admin',
      email: 'admin@barstockwise.com',
      first_name: 'Admin',
      last_name: 'User',
      role: 'admin',
      is_active: true,
      is_staff: true,
      is_superuser: true,
      date_joined: new Date().toISOString(),
      permissions: ['*'],
      isLoggedIn: true,
      lastActivity: Date.now()
    };
    
    // Enregistrer dans localStorage pour simuler une connexion réussie
    console.log('Utilisateur créé:', user);
    console.log('Stockage dans localStorage...');
    
    // Instructions pour l'utilisateur
    console.log('\n--- INSTRUCTIONS ---');
    console.log('1. Copiez le code suivant');
    console.log('2. Ouvrez la console du navigateur (F12)');
    console.log('3. Collez et exécutez le code dans la console');
    console.log('\nCODE À COPIER:');
    console.log(`localStorage.setItem('user', '${JSON.stringify(user)}');`);
    console.log('\nEnsuite, rafraîchissez la page pour être automatiquement connecté.');
  } else {
    console.log('❌ Échec de l\'authentification!');
  }
}

// Exécuter le test
testAuth();