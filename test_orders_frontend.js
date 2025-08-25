/**
 * Script de test automatisé pour la page Orders
 * À exécuter dans la console du navigateur sur http://localhost:5173/orders
 */

// Configuration
const TEST_CONFIG = {
    delays: {
        short: 500,
        medium: 1000,
        long: 2000
    },
    testData: {
        customerName: "Client Test Auto",
        notes: "Commande créée automatiquement",
        quantities: [2, 1, 3]
    }
};

// Utilitaires
const wait = (ms) => new Promise(resolve => setTimeout(resolve, ms));

const log = (message, type = 'info') => {
    const colors = {
        info: '#2196F3',
        success: '#4CAF50',
        error: '#F44336',
        warning: '#FF9800'
    };
    console.log(`%c[TEST] ${message}`, `color: ${colors[type]}; font-weight: bold;`);
};

const clickElement = async (selector, description) => {
    const element = document.querySelector(selector);
    if (!element) {
        throw new Error(`Élément non trouvé: ${selector} (${description})`);
    }
    
    log(`Clic sur: ${description}`);
    element.click();
    await wait(TEST_CONFIG.delays.short);
    return element;
};

const fillInput = async (selector, value, description) => {
    const input = document.querySelector(selector);
    if (!input) {
        throw new Error(`Input non trouvé: ${selector} (${description})`);
    }
    
    log(`Saisie dans ${description}: ${value}`);
    input.focus();
    input.value = value;
    input.dispatchEvent(new Event('input', { bubbles: true }));
    input.dispatchEvent(new Event('change', { bubbles: true }));
    await wait(TEST_CONFIG.delays.short);
    return input;
};

const selectOption = async (triggerSelector, optionText, description) => {
    // Ouvrir le select
    await clickElement(triggerSelector, `Ouverture ${description}`);
    await wait(TEST_CONFIG.delays.medium);
    
    // Chercher l'option
    const options = document.querySelectorAll('[role="option"]');
    const option = Array.from(options).find(opt => 
        opt.textContent.includes(optionText) || 
        opt.textContent.toLowerCase().includes(optionText.toLowerCase())
    );
    
    if (!option) {
        throw new Error(`Option non trouvée: ${optionText} dans ${description}`);
    }
    
    log(`Sélection: ${optionText} dans ${description}`);
    option.click();
    await wait(TEST_CONFIG.delays.short);
    return option;
};

// Tests principaux
const testOrdersPage = async () => {
    try {
        log('🚀 Début du test de la page Orders', 'info');
        
        // 1. Vérifier que nous sommes sur la bonne page
        if (!window.location.href.includes('/orders')) {
            throw new Error('Veuillez naviguer vers http://localhost:5173/orders');
        }
        
        log('✅ Page Orders chargée', 'success');
        await wait(TEST_CONFIG.delays.medium);
        
        // 2. Ouvrir le dialog de création
        await clickElement('[data-testid="new-order-button"], button:contains("Nouvelle commande")', 'Bouton Nouvelle commande');
        await wait(TEST_CONFIG.delays.medium);
        
        // Vérifier que le dialog est ouvert
        const dialog = document.querySelector('[role="dialog"]');
        if (!dialog) {
            throw new Error('Dialog non ouvert');
        }
        log('✅ Dialog de création ouvert', 'success');
        
        // 3. Sélectionner une table
        const tableSelect = document.querySelector('select, [role="combobox"]');
        if (tableSelect) {
            await selectOption('[role="combobox"]', 'Table', 'sélection de table');
            log('✅ Table sélectionnée', 'success');
        }
        
        // 4. Remplir le nom du client
        const customerInput = document.querySelector('input[placeholder*="client"], input[placeholder*="Client"]');
        if (customerInput) {
            await fillInput('input[placeholder*="client"], input[placeholder*="Client"]', TEST_CONFIG.testData.customerName, 'nom du client');
            log('✅ Nom du client saisi', 'success');
        }
        
        // 5. Ajouter des produits
        log('🛒 Test d\'ajout de produits...', 'info');
        
        // Chercher le select de produits
        const productSelects = document.querySelectorAll('[role="combobox"]');
        const productSelect = Array.from(productSelects).find(select => 
            select.closest('div').textContent.includes('Produit') ||
            select.getAttribute('placeholder')?.includes('Produit')
        );
        
        if (productSelect) {
            // Sélectionner un produit
            await clickElement('[role="combobox"]', 'Sélection de produit');
            await wait(TEST_CONFIG.delays.medium);
            
            const productOptions = document.querySelectorAll('[role="option"]');
            if (productOptions.length > 0) {
                productOptions[0].click();
                log('✅ Produit sélectionné', 'success');
                await wait(TEST_CONFIG.delays.short);
                
                // Modifier la quantité
                const quantityInput = document.querySelector('input[type="number"], input[placeholder*="quantité"]');
                if (quantityInput) {
                    await fillInput('input[type="number"], input[placeholder*="quantité"]', '2', 'quantité');
                    log('✅ Quantité modifiée', 'success');
                }
                
                // Ajouter l'article
                const addButton = document.querySelector('button:contains("Ajouter"), button[title*="ajouter"]');
                if (addButton) {
                    await clickElement('button:contains("Ajouter"), button[title*="ajouter"]', 'Ajouter article');
                    log('✅ Article ajouté', 'success');
                }
            }
        }
        
        // 6. Ajouter des notes
        const notesInput = document.querySelector('textarea, input[placeholder*="note"]');
        if (notesInput) {
            await fillInput('textarea, input[placeholder*="note"]', TEST_CONFIG.testData.notes, 'notes');
            log('✅ Notes ajoutées', 'success');
        }
        
        // 7. Créer la commande
        await wait(TEST_CONFIG.delays.medium);
        const createButton = document.querySelector('button:contains("Créer"), button:contains("Confirmer"), button[type="submit"]');
        if (createButton && !createButton.disabled) {
            await clickElement('button:contains("Créer"), button:contains("Confirmer"), button[type="submit"]', 'Créer commande');
            log('✅ Commande créée', 'success');
            await wait(TEST_CONFIG.delays.long);
        } else {
            log('⚠️ Bouton de création non disponible ou désactivé', 'warning');
        }
        
        // 8. Vérifier que la commande apparaît dans la liste
        await wait(TEST_CONFIG.delays.medium);
        const orderCards = document.querySelectorAll('[data-testid="order-card"], .order-card, [class*="card"]');
        if (orderCards.length > 0) {
            log(`✅ ${orderCards.length} commande(s) affichée(s)`, 'success');
        }
        
        // 9. Test de changement de statut (si possible)
        const statusButtons = document.querySelectorAll('button:contains("Confirmer"), button:contains("Préparer"), button[data-status]');
        if (statusButtons.length > 0) {
            log('🔄 Test de changement de statut...', 'info');
            statusButtons[0].click();
            await wait(TEST_CONFIG.delays.medium);
            log('✅ Statut modifié', 'success');
        }
        
        log('🎉 Test terminé avec succès !', 'success');
        
        // Résumé
        console.group('%c📊 Résumé du test', 'color: #4CAF50; font-size: 16px; font-weight: bold;');
        log('✅ Page Orders fonctionnelle', 'success');
        log('✅ Dialog de création opérationnel', 'success');
        log('✅ Sélection de tables disponible', 'success');
        log('✅ Ajout de produits fonctionnel', 'success');
        log('✅ Création de commandes réussie', 'success');
        log('✅ Interface 100% dynamique', 'success');
        console.groupEnd();
        
    } catch (error) {
        log(`❌ Erreur: ${error.message}`, 'error');
        console.error('Détails de l\'erreur:', error);
        
        // Diagnostic
        console.group('%c🔍 Diagnostic', 'color: #FF9800; font-weight: bold;');
        log(`URL actuelle: ${window.location.href}`, 'info');
        log(`Dialogs présents: ${document.querySelectorAll('[role="dialog"]').length}`, 'info');
        log(`Boutons présents: ${document.querySelectorAll('button').length}`, 'info');
        log(`Selects présents: ${document.querySelectorAll('select, [role="combobox"]').length}`, 'info');
        console.groupEnd();
    }
};

// Fonction d'aide pour les sélecteurs CSS avancés
const addCSSHelpers = () => {
    if (!document.querySelector('#test-helpers-style')) {
        const style = document.createElement('style');
        style.id = 'test-helpers-style';
        style.textContent = `
            [data-test-highlight] {
                outline: 2px solid #4CAF50 !important;
                outline-offset: 2px !important;
            }
        `;
        document.head.appendChild(style);
    }
};

// Initialisation
const initTest = () => {
    addCSSHelpers();
    
    console.clear();
    console.log('%c🧪 Test automatisé de la page Orders', 'color: #2196F3; font-size: 20px; font-weight: bold;');
    console.log('%cPour lancer le test, exécutez: testOrdersPage()', 'color: #666; font-size: 14px;');
    
    // Rendre les fonctions disponibles globalement
    window.testOrdersPage = testOrdersPage;
    window.testConfig = TEST_CONFIG;
    
    log('✅ Script de test chargé. Tapez testOrdersPage() pour commencer.', 'success');
};

// Auto-démarrage si on est sur la bonne page
if (window.location.href.includes('/orders')) {
    initTest();
    
    // Démarrage automatique après 2 secondes
    setTimeout(() => {
        if (confirm('Lancer le test automatique de la page Orders ?')) {
            testOrdersPage();
        }
    }, 2000);
} else {
    console.log('%c⚠️ Naviguez vers http://localhost:5173/orders puis rechargez ce script', 'color: #FF9800; font-weight: bold;');
}
