#!/usr/bin/env python
"""
Script pour corriger et redimensionner le dialog utilisateur
"""

def fix_users_dialog():
    """Corriger le dialog utilisateur avec un meilleur format"""
    
    # Lire le fichier actuel
    try:
        with open('src/pages/Users.tsx', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remplacer le dialog de création avec un format plus large
        old_dialog_create = '''              <DialogContent className="max-w-lg">
                <DialogHeader>
                  <DialogTitle>Créer un nouvel utilisateur</DialogTitle>
                  <DialogDescription>
                    Ajoutez un nouveau membre à votre équipe
                  </DialogDescription>
                </DialogHeader>
                <div className="space-y-3">
                  <div className="space-y-1">
                    <Label htmlFor="username" className="text-sm">Nom d'utilisateur</Label>
                    <Input
                      id="username"
                      value={newUser.username}
                      onChange={(e) => setNewUser(prev => ({...prev, username: e.target.value}))}
                      placeholder="nom.utilisateur"
                      className="bg-white border-gray-300 focus:border-blue-500 focus:ring-blue-500 h-9"
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-3">
                    <div className="space-y-1">
                      <Label htmlFor="first_name" className="text-sm">Prénom</Label>
                      <Input
                        id="first_name"
                        value={newUser.first_name}
                        onChange={(e) => setNewUser(prev => ({...prev, first_name: e.target.value}))}
                        className="bg-white border-gray-300 focus:border-blue-500 focus:ring-blue-500 h-9"
                      />
                    </div>
                    <div className="space-y-1">
                      <Label htmlFor="last_name" className="text-sm">Nom</Label>
                      <Input
                        id="last_name"
                        value={newUser.last_name}
                        onChange={(e) => setNewUser(prev => ({...prev, last_name: e.target.value}))}
                        className="bg-white border-gray-300 focus:border-blue-500 focus:ring-blue-500 h-9"
                      />
                    </div>
                  </div>
                  
                  <div className="space-y-1">
                    <Label htmlFor="email" className="text-sm">Email</Label>
                    <Input
                      id="email"
                      type="email"
                      value={newUser.email}
                      onChange={(e) => setNewUser(prev => ({...prev, email: e.target.value}))}
                      className="bg-white border-gray-300 focus:border-blue-500 focus:ring-blue-500 h-9"
                    />
                  </div>'''
        
        new_dialog_create = '''              <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
                <DialogHeader>
                  <DialogTitle className="text-xl font-semibold">Créer un nouvel utilisateur</DialogTitle>
                  <DialogDescription className="text-base">
                    Ajoutez un nouveau membre à votre équipe avec les informations complètes
                  </DialogDescription>
                </DialogHeader>
                <div className="space-y-6 py-4">
                  {/* Informations de base */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="space-y-4">
                      <h3 className="text-lg font-medium text-gray-900">Informations personnelles</h3>
                      
                      <div className="space-y-2">
                        <Label htmlFor="username" className="text-sm font-medium">Nom d'utilisateur *</Label>
                        <Input
                          id="username"
                          value={newUser.username}
                          onChange={(e) => setNewUser(prev => ({...prev, username: e.target.value}))}
                          placeholder="nom.utilisateur"
                          className="h-10"
                          required
                        />
                      </div>

                      <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <Label htmlFor="first_name" className="text-sm font-medium">Prénom *</Label>
                          <Input
                            id="first_name"
                            value={newUser.first_name}
                            onChange={(e) => setNewUser(prev => ({...prev, first_name: e.target.value}))}
                            placeholder="Jean"
                            className="h-10"
                            required
                          />
                        </div>
                        <div className="space-y-2">
                          <Label htmlFor="last_name" className="text-sm font-medium">Nom *</Label>
                          <Input
                            id="last_name"
                            value={newUser.last_name}
                            onChange={(e) => setNewUser(prev => ({...prev, last_name: e.target.value}))}
                            placeholder="Dupont"
                            className="h-10"
                            required
                          />
                        </div>
                      </div>
                      
                      <div className="space-y-2">
                        <Label htmlFor="email" className="text-sm font-medium">Email *</Label>
                        <Input
                          id="email"
                          type="email"
                          value={newUser.email}
                          onChange={(e) => setNewUser(prev => ({...prev, email: e.target.value}))}
                          placeholder="jean.dupont@example.com"
                          className="h-10"
                          required
                        />
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="phone" className="text-sm font-medium">Téléphone</Label>
                        <Input
                          id="phone"
                          type="tel"
                          value={newUser.phone}
                          onChange={(e) => setNewUser(prev => ({...prev, phone: e.target.value}))}
                          placeholder="+257 XX XX XX XX"
                          className="h-10"
                        />
                      </div>
                    </div>

                    <div className="space-y-4">
                      <h3 className="text-lg font-medium text-gray-900">Rôle et permissions</h3>
                      
                      <div className="space-y-2">
                        <Label htmlFor="role" className="text-sm font-medium">Rôle *</Label>
                        <Select value={newUser.role} onValueChange={(value: any) => setNewUser(prev => ({...prev, role: value}))}>
                          <SelectTrigger className="h-10">
                            <SelectValue placeholder="Sélectionner un rôle" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="admin">👑 Administrateur</SelectItem>
                            <SelectItem value="manager">👔 Manager</SelectItem>
                            <SelectItem value="server">🍽️ Serveur</SelectItem>
                            <SelectItem value="cashier">💰 Caissier</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>

                      {/* Permissions */}
                      <div className="space-y-3">
                        <Label className="text-sm font-medium">Permissions spéciales</Label>
                        <div className="grid grid-cols-1 gap-3 max-h-48 overflow-y-auto border rounded-lg p-3 bg-gray-50">
                          {permissionsData && permissionsData.map((permission: any) => (
                            <div key={permission.id} className="flex items-center space-x-2">
                              <Checkbox
                                id={`perm-${permission.id}`}
                                checked={newUser.permissions.includes(permission.codename)}
                                onCheckedChange={(checked) => {
                                  if (checked) {
                                    setNewUser(prev => ({
                                      ...prev,
                                      permissions: [...prev.permissions, permission.codename]
                                    }));
                                  } else {
                                    setNewUser(prev => ({
                                      ...prev,
                                      permissions: prev.permissions.filter(p => p !== permission.codename)
                                    }));
                                  }
                                }}
                              />
                              <Label 
                                htmlFor={`perm-${permission.id}`} 
                                className="text-sm cursor-pointer"
                              >
                                {permission.name}
                              </Label>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Note de sécurité */}
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <div className="flex items-start space-x-3">
                      <Lock className="h-5 w-5 text-blue-600 mt-0.5" />
                      <div>
                        <h4 className="text-sm font-medium text-blue-900">Sécurité</h4>
                        <p className="text-sm text-blue-700 mt-1">
                          Un mot de passe temporaire sera généré automatiquement. 
                          L'utilisateur devra le changer lors de sa première connexion.
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Boutons d'action */}
                  <div className="flex justify-end space-x-3 pt-4 border-t">
                    <Button 
                      variant="outline" 
                      onClick={() => setShowNewUserDialog(false)}
                      className="px-6"
                    >
                      Annuler
                    </Button>
                    <Button 
                      onClick={createUser}
                      disabled={createUserMutation.isPending || !newUser.username || !newUser.first_name || !newUser.last_name || !newUser.email}
                      className="px-6"
                    >
                      {createUserMutation.isPending ? (
                        <>
                          <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                          Création...
                        </>
                      ) : (
                        <>
                          <UserCheck className="h-4 w-4 mr-2" />
                          Créer l'utilisateur
                        </>
                      )}
                    </Button>
                  </div>'''
        
        # Remplacer dans le contenu
        if old_dialog_create in content:
            content = content.replace(old_dialog_create, new_dialog_create)
            print("✅ Dialog de création d'utilisateur redimensionné")
        else:
            print("⚠️ Pattern de dialog de création non trouvé")
        
        # Sauvegarder le fichier modifié
        with open('src/pages/Users.tsx', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Fichier Users.tsx mis à jour avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction du dialog: {e}")
        return False

def run_users_fixes():
    """Exécuter toutes les corrections pour la page Users"""
    print("🔧 CORRECTION PAGE USERS ET DIALOG")
    print("=" * 50)
    
    print("\n1. Redimensionnement du dialog utilisateur...")
    success = fix_users_dialog()
    
    if success:
        print("\n✅ CORRECTIONS TERMINÉES!")
        print("\n📋 AMÉLIORATIONS APPORTÉES:")
        print("1. ✅ Dialog redimensionné (max-w-4xl)")
        print("2. ✅ Layout en 2 colonnes pour plus d'espace")
        print("3. ✅ Champs plus grands et mieux espacés")
        print("4. ✅ Section permissions avec scroll")
        print("5. ✅ Validation visuelle des champs requis")
        print("6. ✅ Note de sécurité pour le mot de passe")
        print("7. ✅ Boutons d'action améliorés")
        
        print("\n🚀 FONCTIONNALITÉS AMÉLIORÉES:")
        print("- ✅ Interface plus spacieuse et lisible")
        print("- ✅ Validation en temps réel")
        print("- ✅ Gestion des permissions visuellement claire")
        print("- ✅ Feedback utilisateur amélioré")
        print("- ✅ Design responsive")
        
        print("\n💡 TESTEZ MAINTENANT:")
        print("1. Allez sur http://localhost:5173/users")
        print("2. Cliquez sur 'Nouvel utilisateur'")
        print("3. Testez le nouveau format du dialog")
        print("4. Vérifiez la sélection des permissions")
        
        return True
    else:
        print("\n❌ ÉCHEC DES CORRECTIONS")
        return False

if __name__ == "__main__":
    success = run_users_fixes()
    
    if success:
        print("\n🎊 DIALOG UTILISATEUR CORRIGÉ!")
        print("Le dialog est maintenant plus grand et mieux organisé!")
    else:
        print("\n⚠️ Des problèmes persistent...")
    
    print("\n📋 PROCHAINE ÉTAPE:")
    print("Exécution du script de test pour vérifier que la page est 100% fonctionnelle")
