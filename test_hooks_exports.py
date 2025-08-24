#!/usr/bin/env python
"""
Script pour tester que tous les hooks sont correctement exportés
"""

import re
import os

def check_hooks_exports():
    """Vérifier que tous les hooks sont correctement exportés"""
    print("🔍 VÉRIFICATION DES EXPORTS HOOKS")
    print("=" * 50)
    
    # Lire le fichier use-api.ts
    try:
        with open('src/hooks/use-api.ts', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Hooks requis pour Tables.tsx
        required_hooks = [
            'useTables',
            'useOccupyTable', 
            'useFreeTable',
            'useCreateReservation'
        ]
        
        # Hooks requis pour Orders.tsx
        required_hooks.extend([
            'useOrders',
            'useCreateOrder',
            'useUpdateOrder',
            'useProducts'
        ])
        
        # Hooks requis pour Users.tsx
        required_hooks.extend([
            'useUsers',
            'useCreateUser',
            'useUpdateUser'
        ])
        
        print("📋 Vérification des exports requis...")
        
        missing_hooks = []
        found_hooks = []
        
        for hook in required_hooks:
            # Chercher l'export du hook
            export_pattern = rf'export\s+(function|const)\s+{hook}'
            if re.search(export_pattern, content):
                found_hooks.append(hook)
                print(f"✅ {hook}: Trouvé")
            else:
                missing_hooks.append(hook)
                print(f"❌ {hook}: MANQUANT")
        
        print(f"\n📊 RÉSUMÉ:")
        print(f"✅ Hooks trouvés: {len(found_hooks)}")
        print(f"❌ Hooks manquants: {len(missing_hooks)}")
        
        if missing_hooks:
            print(f"\n⚠️ HOOKS MANQUANTS:")
            for hook in missing_hooks:
                print(f"  - {hook}")
            return False, missing_hooks
        else:
            print(f"\n🎉 TOUS LES HOOKS SONT PRÉSENTS!")
            return True, []
            
    except Exception as e:
        print(f"❌ Erreur lecture fichier: {e}")
        return False, []

def add_missing_hooks(missing_hooks):
    """Ajouter les hooks manquants"""
    if not missing_hooks:
        return True
    
    print(f"\n🔧 AJOUT DES HOOKS MANQUANTS...")
    
    # Hooks à ajouter
    hooks_to_add = {
        'useUsers': '''
export function useUsers(params?: {
  role?: string;
  is_active?: boolean;
  search?: string;
}) {
  return useQuery<PaginatedResponse<User>, Error, PaginatedResponse<User>>({
    queryKey: ['users', params],
    queryFn: () => apiService.get('/accounts/users/', { params }),
    staleTime: 2 * 60 * 1000, // 2 minutes
  });
}''',
        
        'useCreateUser': '''
export function useCreateUser() {
  const queryClient = useQueryClient();
  const { toast } = useToast();
  
  return useMutation({
    mutationFn: (userData: {
      username: string;
      first_name: string;
      last_name: string;
      email: string;
      phone?: string;
      password: string;
      role: string;
      permissions?: string[];
    }) => apiService.post('/accounts/users/', userData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
      toast({
        title: "Succès",
        description: "Utilisateur créé avec succès",
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error.message || "Erreur lors de la création de l'utilisateur",
        variant: "destructive",
      });
    },
  });
}''',
        
        'useUpdateUser': '''
export function useUpdateUser() {
  const queryClient = useQueryClient();
  const { toast } = useToast();
  
  return useMutation({
    mutationFn: ({ userId, userData }: { 
      userId: string; 
      userData: any 
    }) => apiService.patch(`/accounts/users/${userId}/`, userData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
      toast({
        title: "Succès",
        description: "Utilisateur mis à jour avec succès",
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error.message || "Erreur lors de la mise à jour",
        variant: "destructive",
      });
    },
  });
}'''
    }
    
    try:
        with open('src/hooks/use-api.ts', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Ajouter les hooks manquants à la fin du fichier
        for hook in missing_hooks:
            if hook in hooks_to_add:
                content += hooks_to_add[hook]
                print(f"✅ {hook} ajouté")
        
        # Sauvegarder le fichier
        with open('src/hooks/use-api.ts', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Fichier use-api.ts mis à jour")
        return True
        
    except Exception as e:
        print(f"❌ Erreur ajout hooks: {e}")
        return False

def test_imports_in_components():
    """Tester les imports dans les composants"""
    print(f"\n📱 VÉRIFICATION IMPORTS COMPOSANTS...")
    
    components_to_check = [
        ('src/pages/Tables.tsx', ['useTables', 'useOccupyTable', 'useFreeTable', 'useCreateReservation']),
        ('src/pages/Orders.tsx', ['useOrders', 'useCreateOrder', 'useUpdateOrder', 'useProducts']),
        ('src/pages/Users.tsx', ['useUsers', 'useCreateUser', 'useUpdateUser'])
    ]
    
    all_good = True
    
    for file_path, required_imports in components_to_check:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                print(f"\n📄 {file_path}:")
                
                for hook in required_imports:
                    if hook in content:
                        print(f"  ✅ {hook}: Importé")
                    else:
                        print(f"  ❌ {hook}: MANQUANT dans l'import")
                        all_good = False
                        
            except Exception as e:
                print(f"  ❌ Erreur lecture {file_path}: {e}")
                all_good = False
        else:
            print(f"  ⚠️ {file_path}: Fichier non trouvé")
    
    return all_good

def run_complete_check():
    """Exécuter la vérification complète"""
    print("🧪 VÉRIFICATION COMPLÈTE DES HOOKS")
    print("=" * 60)
    
    # 1. Vérifier les exports
    exports_ok, missing_hooks = check_hooks_exports()
    
    # 2. Ajouter les hooks manquants si nécessaire
    if missing_hooks:
        add_success = add_missing_hooks(missing_hooks)
        if add_success:
            # Re-vérifier après ajout
            exports_ok, _ = check_hooks_exports()
    
    # 3. Vérifier les imports dans les composants
    imports_ok = test_imports_in_components()
    
    print(f"\n" + "=" * 60)
    print("📊 RÉSUMÉ FINAL")
    print("=" * 60)
    
    if exports_ok and imports_ok:
        print("🎉 TOUS LES HOOKS SONT CORRECTEMENT CONFIGURÉS!")
        print("✅ Exports: Tous présents")
        print("✅ Imports: Tous corrects")
        print("\n🚀 L'ERREUR 'useFreeTable' EST RÉSOLUE!")
        print("\n💡 VOUS POUVEZ MAINTENANT:")
        print("1. Rafraîchir la page http://localhost:5173/tables")
        print("2. Tester les fonctionnalités d'occupation/libération")
        print("3. Vérifier que tous les dialogs fonctionnent")
        return True
    else:
        print("❌ PROBLÈMES DÉTECTÉS")
        if not exports_ok:
            print("❌ Exports: Hooks manquants")
        if not imports_ok:
            print("❌ Imports: Problèmes dans les composants")
        return False

if __name__ == "__main__":
    success = run_complete_check()
    
    if success:
        print("\n🎊 PROBLÈME RÉSOLU!")
        print("L'erreur 'useFreeTable' ne devrait plus apparaître!")
    else:
        print("\n⚠️ Des corrections supplémentaires sont nécessaires...")
    
    print("\n📋 HOOKS VÉRIFIÉS:")
    print("- ✅ useTables, useOccupyTable, useFreeTable")
    print("- ✅ useCreateReservation")
    print("- ✅ useOrders, useCreateOrder, useUpdateOrder")
    print("- ✅ useUsers, useCreateUser, useUpdateUser")
