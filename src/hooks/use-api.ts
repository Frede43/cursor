/**
 * Hooks React Query pour la gestion des données API
 * Centralise toutes les requêtes avec cache et gestion d'erreurs
 */

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useToast } from './use-toast';
import {
  productService,
  salesService,
  supplierService,
  reportsService,
  apiService
} from '@/services/api';
import type {
  DashboardStats,
  KitchenDashboard,
  PaginatedResponse,
  Product,
  Sale,
  Supplier,
  Expense,
  ExpenseCategory,
  Supply,
  Table,
  Order,
  User,
  StockMovement,
  Purchase,
  PurchaseItem,
  UserActivity,
  DailyReport,
  StockAlert,
  Alert
} from '@/types/api';

// Types pour les paramètres de requête
interface UseProductsParams {
  search?: string;
  category?: number;
  status?: 'ok' | 'low' | 'critical';
  page?: number;
}

interface UseSalesParams {
  date_from?: string;
  date_to?: string;
  server?: number;
  status?: string;
  page?: number;
}

interface UseIngredientsParams {
  search?: string;
  status?: 'ok' | 'alerte' | 'rupture';
  unite?: string;
}

interface UseRecipesParams {
  search?: string;
  status?: 'available' | 'unavailable' | 'inactive';
}

// ==================== HOOKS PRODUITS ====================

export function useProducts(params?: UseProductsParams) {
  return useQuery<PaginatedResponse<Product>, Error, PaginatedResponse<Product>>({
    queryKey: ['products', params],
    queryFn: () => productService.getProducts(params) as Promise<PaginatedResponse<Product>>,
    staleTime: 5 * 60 * 1000, // 5 minutes
    gcTime: 10 * 60 * 1000, // 10 minutes
  });
}

export function useProduct(id: number) {
  return useQuery<Product, Error, Product>({
    queryKey: ['products', id],
    queryFn: () => productService.getProduct(id),
    enabled: !!id,
  });
}

export function useCreateProduct() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: (data: any) => productService.createProduct(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['products'] });
      toast({
        title: "Succès",
        description: "Produit créé avec succès",
        variant: "default",
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error.message || "Erreur lors de la création du produit",
        variant: "destructive",
      });
    },
  });
}

export function useUpdateProduct() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) => 
      productService.updateProduct(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['products'] });
      toast({
        title: "Succès",
        description: "Produit mis à jour avec succès",
        variant: "default",
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
}

export function useUpdateProductStock() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) => 
      productService.updateStock(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['products'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
      toast({
        title: "Succès",
        description: "Stock mis à jour avec succès",
        variant: "default",
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error.message || "Erreur lors de la mise à jour du stock",
        variant: "destructive",
      });
    },
  });
}


// ==================== HOOKS VENTES ====================

export function useSales(params?: UseSalesParams) {
  return useQuery<PaginatedResponse<Sale>, Error, PaginatedResponse<Sale>>({
    queryKey: ['sales', params],
    queryFn: () => apiService.get('/sales/', { params }) as Promise<PaginatedResponse<Sale>>,
    staleTime: 1 * 60 * 1000, // 1 minute
  });
}

export function useCreateSale() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: (data: {
      table_number?: number;
      payment_method: 'cash' | 'card' | 'mobile';
      items: Array<{
        product: number;
        quantity: number;
        notes?: string;
      }>;
      notes?: string;
    }) => salesService.createSale(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sales'] });
      queryClient.invalidateQueries({ queryKey: ['products'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
      queryClient.invalidateQueries({ queryKey: ['kitchen'] });
      toast({
        title: "Succès",
        description: "Vente enregistrée avec succès",
        variant: "default",
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error.message || "Erreur lors de l'enregistrement de la vente",
        variant: "destructive",
      });
    },
  });
}

export function useSalesStats(period?: 'today' | 'week' | 'month') {
  return useQuery({
    queryKey: ['sales', 'stats', period],
    queryFn: () => salesService.getSalesStats(period),
    staleTime: 5 * 60 * 1000, // 5 minutes
    refetchOnWindowFocus: false, // Éviter les refetch lors du focus
  });
}

// Hook pour approuver une vente
export function useApproveSale() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: (id: number) => salesService.approveSale(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sales'] });
      queryClient.invalidateQueries({ queryKey: ['reports'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
      toast({
        title: "Succès",
        description: "Vente approuvée avec succès"
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error.message || "Erreur lors de l'approbation de la vente",
        variant: "destructive"
      });
    }
  });
}

// Hook pour annuler une vente
export function useCancelSale() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: ({ id, reason }: { id: number; reason: string }) => 
      salesService.cancelSale(id, reason),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sales'] });
      queryClient.invalidateQueries({ queryKey: ['reports'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
      toast({
        title: "Succès",
        description: "Vente annulée avec succès"
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error.message || "Erreur lors de l'annulation de la vente",
        variant: "destructive"
      });
    }
  });
}

// Hook pour marquer une vente comme payée
export function useMarkSaleAsPaid() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: (id: number) => salesService.markAsPaid(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sales'] });
      queryClient.invalidateQueries({ queryKey: ['products'] }); // Actualiser les stocks
      queryClient.invalidateQueries({ queryKey: ['reports'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
      toast({
        title: "Succès",
        description: "Vente marquée comme payée et stock mis à jour"
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error.message || "Erreur lors du marquage comme payé",
        variant: "destructive"
      });
    }
  });
}

// Hook pour supprimer une vente
export function useDeleteSale() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: (id: number) => salesService.deleteSale(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sales'] });
      queryClient.invalidateQueries({ queryKey: ['reports'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
      toast({
        title: "Succès",
        description: "Vente supprimée avec succès"
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error.message || "Erreur lors de la suppression de la vente",
        variant: "destructive"
      });
    }
  });
}

// ==================== HOOKS FOURNISSEURS ====================

export function useSuppliers(params?: {
  search?: string;
  is_active?: boolean;
}) {
  return useQuery<PaginatedResponse<Supplier>, Error, PaginatedResponse<Supplier>>({
    queryKey: ['suppliers', params],
    queryFn: () => supplierService.getSuppliers(params) as Promise<PaginatedResponse<Supplier>>,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

export function useCreateSupplier() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: supplierService.createSupplier.bind(supplierService),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['suppliers'] });
      toast({
        title: "Succès",
        description: "Fournisseur créé avec succès"
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error.message || "Erreur lors de la création du fournisseur",
        variant: "destructive"
      });
    }
  });
}

export function useUpdateSupplier() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) => 
      supplierService.updateSupplier(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['suppliers'] });
      toast({
        title: "Succès",
        description: "Fournisseur mis à jour avec succès"
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error.message || "Erreur lors de la mise à jour du fournisseur",
        variant: "destructive"
      });
    }
  });
}

export function useDeleteSupplier() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: (id: number) => supplierService.deleteSupplier(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['suppliers'] });
      toast({
        title: "Succès",
        description: "Fournisseur supprimé avec succès"
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error.message || "Erreur lors de la suppression du fournisseur",
        variant: "destructive"
      });
    }
  });
}

// ==================== HOOKS CUISINE ====================

export function useKitchenDashboard() {
  return useQuery<KitchenDashboard, Error, KitchenDashboard>({
    queryKey: ['kitchen', 'dashboard'],
    queryFn: () => apiService.get('/kitchen/dashboard/'),
    staleTime: 2 * 60 * 1000, // 2 minutes
  });
}

export function useIngredients(params?: UseIngredientsParams) {
  return useQuery({
    queryKey: ['kitchen', 'ingredients', params],
    queryFn: () => apiService.get('/kitchen/ingredients/', { params }),
    staleTime: 3 * 60 * 1000, // 3 minutes
  });
}

export function useRecipes(params?: UseRecipesParams) {
  return useQuery({
    queryKey: ['kitchen', 'recipes', params],
    queryFn: () => apiService.get('/kitchen/recipes/', { params }),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

export function useCreateIngredient() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: (data: any) => apiService.post('/kitchen/ingredients/', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['kitchen', 'ingredients'] });
      queryClient.invalidateQueries({ queryKey: ['kitchen', 'dashboard'] });
      toast({
        title: "Succès",
        description: "Ingrédient créé avec succès",
        variant: "default",
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error.message || "Erreur lors de la création de l'ingrédient",
        variant: "destructive",
      });
    },
  });
}

export function useUpdateIngredientStock() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) => 
      apiService.patch(`/kitchen/ingredients/${id}/stock/`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['kitchen'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
      toast({
        title: "Succès",
        description: "Stock d'ingrédient mis à jour",
        variant: "default",
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error.message || "Erreur lors de la mise à jour du stock",
        variant: "destructive",
      });
    },
  });
}

export function useIngredientsAlerts() {
  return useQuery({
    queryKey: ['kitchen', 'alerts'],
    queryFn: () => apiService.get('/kitchen/ingredients/alerts/'),
    staleTime: 1 * 60 * 1000, // 1 minute
    refetchInterval: 2 * 60 * 1000, // Refetch toutes les 2 minutes
  });
}

// Hook pour les données de cuisine dans les rapports
export function useKitchenReport(date?: string) {
  return useQuery({
    queryKey: ['kitchen', 'report', date],
    queryFn: () => apiService.get('/kitchen/reports/', { params: { date } }),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}



// Hook pour mettre à jour un ingrédient
export function useUpdateIngredient() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) => apiService.put(`/kitchen/ingredients/${id}/`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['kitchen', 'ingredients'] });
      queryClient.invalidateQueries({ queryKey: ['kitchen', 'dashboard'] });
      queryClient.invalidateQueries({ queryKey: ['kitchen', 'alerts'] });
      toast({
        title: "Succès",
        description: "Ingrédient mis à jour avec succès"
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error.message || "Erreur lors de la mise à jour de l'ingrédient",
        variant: "destructive"
      });
    }
  });
}

export function useCheckRecipeAvailability() {
  const { toast } = useToast();

  return useMutation({
    mutationFn: ({ id, quantity }: { id: number; quantity: number }) => 
      apiService.post(`/kitchen/recipes/${id}/check-availability/`, { quantity }),
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error.message || "Erreur lors de la vérification de la recette",
        variant: "destructive",
      });
    },
  });
}

// ==================== HOOKS TABLES ====================

export function useTables(params?: {
  status?: string;
  capacity?: number;
}) {
  return useQuery<PaginatedResponse<Table>, Error, PaginatedResponse<Table>>({
    queryKey: ['tables', params],
    queryFn: () => apiService.get('/sales/tables/', { params }),
    staleTime: 2 * 60 * 1000, // 2 minutes
  });
}

export function useUpdateTableStatus() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: ({ tableId, status }: { tableId: number; status: string }) =>
      apiService.patch(`/apps/tables/${tableId}/`, { status }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tables'] });
      toast({
        title: "Statut mis à jour",
        description: "Le statut de la table a été mis à jour."
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error?.response?.data?.message || "Impossible de mettre à jour le statut de la table.",
        variant: "destructive"
      });
    }
  });
}

export function useOccupyTable() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: ({ tableId, customerName, partySize }: {
      tableId: number;
      customerName: string;
      partySize: number
    }) =>
      apiService.post(`/sales/tables/${tableId}/occupy/`, {
        customer_name: customerName,
        party_size: partySize
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tables'] });
      toast({
        title: "Succès",
        description: "Table occupée avec succès",
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error.message || "Erreur lors de l'occupation de la table",
        variant: "destructive",
      });
    },
  });
}

export function useFreeTable() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: (tableId: number) =>
      apiService.post(`/sales/tables/${tableId}/free/`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tables'] });
      toast({
        title: "Succès",
        description: "Table libérée avec succès",
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error.message || "Erreur lors de la libération de la table",
        variant: "destructive",
      });
    },
  });
}

// ==================== HOOKS FOURNISSEURS ET APPROVISIONNEMENTS ====================

export function useSupplies(params?: {
  supplier?: number;
  status?: string;
  start_date?: string;
  end_date?: string;
}) {
  return useQuery<PaginatedResponse<Supply>, Error, PaginatedResponse<Supply>>({
    queryKey: ['supplies', params],
    queryFn: () => apiService.get('/inventory/supplies/', { params }),
    staleTime: 2 * 60 * 1000, // 2 minutes
  });
}

export function useCreateSupply() {
  const queryClient = useQueryClient();
  const { toast } = useToast();
  
  return useMutation({
    mutationFn: (data: any) => apiService.post('/inventory/supplies/', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['supplies'] });
      toast({
        title: "Approvisionnement créé",
        description: "Le nouvel approvisionnement a été enregistré avec succès."
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error?.response?.data?.message || "Impossible de créer l'approvisionnement.",
        variant: "destructive"
      });
    }
  });
}

export function useUpdateSupply() {
  const queryClient = useQueryClient();
  const { toast } = useToast();
  
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) => 
      apiService.patch(`/inventory/supplies/${id}/`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['supplies'] });
      toast({
        title: "Approvisionnement mis à jour",
        description: "Les modifications ont été enregistrées avec succès."
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error?.response?.data?.message || "Impossible de mettre à jour l'approvisionnement.",
        variant: "destructive"
      });
    }
  });
}

export function useValidateSupply() {
  const queryClient = useQueryClient();
  const { toast } = useToast();
  
  return useMutation({
    mutationFn: (supplyId: number) => 
      apiService.post(`/inventory/supplies/${supplyId}/validate/`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['supplies'] });
      queryClient.invalidateQueries({ queryKey: ['products'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
      toast({
        title: "Livraison validée",
        description: "Le stock a été mis à jour avec succès."
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur de validation",
        description: error?.response?.data?.message || "Impossible de valider la livraison.",
        variant: "destructive"
      });
    }
  });
}

export function useRejectSupply() {
  const queryClient = useQueryClient();
  const { toast } = useToast();
  
  return useMutation({
    mutationFn: (supplyId: number) => 
      apiService.post(`/inventory/supplies/${supplyId}/reject/`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['supplies'] });
      toast({
        title: "Livraison rejetée",
        description: "La livraison a été marquée comme rejetée.",
        variant: "destructive"
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error?.response?.data?.message || "Impossible de rejeter la livraison.",
        variant: "destructive"
      });
    }
  });
}

// ==================== HOOKS ALERTES ====================

export function useAlerts(params?: {
  type?: string;
  priority?: string;
  status?: string;
}) {
  return useQuery<PaginatedResponse<Alert>, Error, PaginatedResponse<Alert>>({
    queryKey: ['alerts', params],
    queryFn: () => apiService.get('/alerts/alerts/', { params }),
    staleTime: 1 * 60 * 1000, // 1 minute
  });
}


export function useUpdateExpense() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: ({ id, data }: { id: string | number, data: any }) => 
      apiService.put(`/expenses/${id}/`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['expenses'] });
      toast({
        title: "Dépense mise à jour",
        description: "La dépense a été mise à jour avec succès."
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: "Impossible de mettre à jour la dépense.",
        variant: "destructive"
      });
    }
  });
}

export function useApproveExpense() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: (expenseId: string | number) => 
      apiService.post(`/expenses/${expenseId}/approve/`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['expenses'] });
      toast({
        title: "Dépense approuvée",
        description: "La dépense a été approuvée avec succès."
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: "Impossible d'approuver la dépense.",
        variant: "destructive"
      });
    }
  });
}

export function useRejectExpense() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: (expenseId: string | number) => 
      apiService.post(`/expenses/${expenseId}/reject/`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['expenses'] });
      toast({
        title: "Dépense rejetée",
        description: "La dépense a été rejetée."
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: "Impossible de rejeter la dépense.",
        variant: "destructive"
      });
    }
  });
}

export function useBudgetSettings() {
  return useQuery({
    queryKey: ['budget-settings'],
    queryFn: () => apiService.get('/expenses/budget-settings/'),
    staleTime: 10 * 60 * 1000, // 10 minutes
    retry: false, // Don't retry on 404
    throwOnError: false, // Don't throw on error
  });
}

export function useUpdateBudgetSettings() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: (budgetData: any) => apiService.put('/expenses/budget-settings/', budgetData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['budget-settings'] });
      toast({
        title: "Budget mis à jour",
        description: "Les paramètres de budget ont été mis à jour."
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: "Impossible de mettre à jour le budget.",
        variant: "destructive"
      });
    }
  });
}

export function usePaymentMethods() {
  return useQuery({
    queryKey: ['payment-methods'],
    queryFn: () => apiService.get('/expenses/payment-methods/'),
    staleTime: 10 * 60 * 1000, // 10 minutes
    retry: false, // Don't retry on 404
    throwOnError: false, // Don't throw on error
  });
}

export function useMenuItems(params?: {
  category?: number;
  is_available?: boolean;
}) {
  return useQuery<PaginatedResponse<any>, Error, PaginatedResponse<any>>({
    queryKey: ['menu-items', params],
    queryFn: () => apiService.get('/menu/items/', { params }),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

export function useCreateOrder() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: (orderData: any) => apiService.post('/orders/', orderData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['orders'] });
      queryClient.invalidateQueries({ queryKey: ['kitchen-queue'] });
      toast({
        title: "Commande créée",
        description: "La nouvelle commande a été créée avec succès.",
        variant: "default",
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error.message || "Impossible de créer la commande.",
        variant: "destructive",
      });
    },
  });
}

export function useResolveAlert() {
  const queryClient = useQueryClient();
  const { toast } = useToast();
  
  return useMutation({
    mutationFn: (alertId: number) => 
      apiService.post(`/alerts/alerts/${alertId}/resolve/`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['alerts'] });
      toast({
        title: "Alerte résolue",
        description: "L'alerte a été marquée comme résolue."
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: "Impossible de résoudre l'alerte.",
        variant: "destructive"
      });
    }
  });
}

export function useArchiveAlert() {
  const queryClient = useQueryClient();
  const { toast } = useToast();
  
  return useMutation({
    mutationFn: (alertId: number) => 
      apiService.post(`/alerts/alerts/${alertId}/archive/`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['alerts'] });
      toast({
        title: "Alerte archivée",
        description: "L'alerte a été archivée avec succès."
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error?.response?.data?.message || "Impossible d'archiver l'alerte.",
        variant: "destructive"
      });
    }
  });
}

export function useUnresolvedAlerts() {
  return useQuery<Alert[], Error, Alert[]>({
    queryKey: ['alerts', 'unresolved'],
    queryFn: () => apiService.get('/reports/alerts/unresolved/'),
    staleTime: 1 * 60 * 1000, // 1 minute
    refetchInterval: 2 * 60 * 1000, // Refetch toutes les 2 minutes
  });
}

// ==================== HOOKS COMMANDES ====================

export function useOrders(params?: {
  status?: string;
  priority?: string;
  table?: number;
  date?: string;
}) {
  return useQuery<PaginatedResponse<Order>, Error, PaginatedResponse<Order>>({
    queryKey: ['orders', params],
    queryFn: () => apiService.get('/orders/orders/', { params }),
    staleTime: 30 * 1000, // 30 secondes pour les commandes
    refetchInterval: 60 * 1000, // Refetch toutes les minutes
  });
}


export function useUpdateOrderStatus() {
  const queryClient = useQueryClient();
  const { toast } = useToast();
  
  return useMutation({
    mutationFn: ({ orderId, action }: { orderId: number; action: string }) => 
      apiService.post(`/orders/orders/${orderId}/${action}/`),
    onSuccess: (_, { action }) => {
      queryClient.invalidateQueries({ queryKey: ['orders'] });
      const actionMessages = {
        confirm: "Commande confirmée",
        start_preparing: "Préparation commencée",
        mark_ready: "Commande prête",
        serve: "Commande servie",
        cancel: "Commande annulée"
      };
      toast({
        title: actionMessages[action as keyof typeof actionMessages] || "Statut mis à jour",
        description: "Le statut de la commande a été mis à jour."
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error?.response?.data?.message || "Impossible de mettre à jour le statut.",
        variant: "destructive"
      });
    }
  });
}

export function useKitchenQueue() {
  return useQuery({
    queryKey: ['orders', 'kitchen-queue'],
    queryFn: () => apiService.get('/orders/orders/kitchen_queue/'),
    staleTime: 15 * 1000, // 15 secondes
    refetchInterval: 30 * 1000, // Refetch toutes les 30 secondes
  });
}

// ==================== HOOKS MONITORING ====================

export function useSystemStats() {
  return useQuery({
    queryKey: ['monitoring', 'stats'],
    queryFn: () => apiService.get('/monitoring/stats/'),
    staleTime: 30 * 1000, // 30 secondes
    refetchInterval: 60 * 1000, // Refetch toutes les minutes
  });
}

export function useSystemMetrics(params?: {
  metric_type?: string;
}) {
  return useQuery({
    queryKey: ['monitoring', 'metrics', params],
    queryFn: () => apiService.get('/monitoring/metrics/', { params }),
    staleTime: 1 * 60 * 1000, // 1 minute
  });
}

export function useSystemAlerts(params?: {
  severity?: string;
  status?: string;
}) {
  return useQuery({
    queryKey: ['monitoring', 'alerts', params],
    queryFn: () => apiService.get('/monitoring/alerts/', { params }),
    staleTime: 30 * 1000, // 30 secondes
  });
}

export function useAcknowledgeSystemAlert() {
  const queryClient = useQueryClient();
  const { toast } = useToast();
  
  return useMutation({
    mutationFn: (alertId: number) => 
      apiService.post(`/monitoring/alerts/${alertId}/acknowledge/`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['monitoring', 'alerts'] });
      toast({
        title: "Alerte acquittée",
        description: "L'alerte système a été acquittée."
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error?.response?.data?.message || "Impossible d'acquitter l'alerte.",
        variant: "destructive"
      });
    }
  });
}

export function usePerformanceLogs(params?: {
  endpoint?: string;
  method?: string;
}) {
  return useQuery({
    queryKey: ['monitoring', 'performance', params],
    queryFn: () => apiService.get('/monitoring/performance/', { params }),
    staleTime: 2 * 60 * 1000, // 2 minutes
  });
}
export function useDashboardStats() {
  return useQuery<DashboardStats, Error, DashboardStats>({
    queryKey: ['dashboard', 'stats'],
    queryFn: () => reportsService.getDashboardStats() as Promise<DashboardStats>,
    staleTime: 5 * 60 * 1000, // 5 minutes
    refetchInterval: 10 * 60 * 1000, // Refetch toutes les 10 minutes
    refetchOnWindowFocus: false, // Éviter les refetch lors du focus
  });
}

export const useDailyReport = (date?: string) => {
  return useQuery({
    queryKey: ['dailyReport', date],
    queryFn: () => reportsService.getDailyReport(date),
    enabled: !!date
  });
};

export const useDailyDetailedReport = (date: string) => {
  return useQuery({
    queryKey: ['dailyDetailedReport', date],
    queryFn: () => reportsService.getDailyDetailedReport(date),
    enabled: !!date
  });
};

export const useLowStockProducts = () => {
  return useQuery({
    queryKey: ['lowStockProducts'],
    queryFn: () => productService.getLowStockProducts(),
    staleTime: 2 * 60 * 1000, // 2 minutes
    refetchInterval: 5 * 60 * 1000, // Refetch toutes les 5 minutes
  });
};

// ==================== HOOKS UTILISATEURS ====================

export function useUsers(params?: {
  search?: string;
  role?: string;
  is_active?: boolean;
}) {
  return useQuery<PaginatedResponse<User>, Error, PaginatedResponse<User>>({
    queryKey: ['users', params],
    queryFn: () => apiService.get('/accounts/users/', { params }),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

export function useUserActivities(userId?: number) {
  return useQuery({
    queryKey: ['users', userId, 'activities'],
    queryFn: () => apiService.get(`/accounts/users/${userId}/activities/`),
    enabled: !!userId,
    staleTime: 2 * 60 * 1000, // 2 minutes
  });
}

export function useCreateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: any) => apiService.post('/accounts/users/', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    }
  });
}

export function usePermissions(params?: { category?: string }) {
  return useQuery({
    queryKey: ['permissions', params],
    queryFn: async () => {
      const response = await apiService.get('/accounts/permissions/list/', { params }) as any;
      // Si la réponse est paginée, retourner seulement les résultats
      return response.results || response;
    },
    staleTime: 10 * 60 * 1000, // 10 minutes
  });
}

export function useAssignPermissions() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ userId, permissions }: { userId: number; permissions: string[] }) =>
      apiService.post(`/accounts/users/${userId}/assign-permissions/`, { permissions }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    }
  });
}

// Hook pour récupérer les serveurs (utilisateurs avec rôle server)
export function useServers(params?: { is_active?: boolean }) {
  return useQuery({
    queryKey: ['servers', params],
    queryFn: async () => {
      const response = await apiService.get('/accounts/users/', {
        params: {
          role: 'server',
          is_active: params?.is_active ?? true
        }
      }) as any;
      return response.results || response;
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

export function useUpdateProfile() {
  const queryClient = useQueryClient();
  const { toast } = useToast();
  
  return useMutation({
    mutationFn: (data: any) => apiService.patch('/accounts/profile/', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['profile'] });
      toast({
        title: "Profil mis à jour",
        description: "Votre profil a été mis à jour avec succès."
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error?.response?.data?.message || "Impossible de mettre à jour le profil.",
        variant: "destructive"
      });
    }
  });
}

export function useChangePassword() {
  const { toast } = useToast();
  
  return useMutation({
    mutationFn: (data: any) => apiService.post('/accounts/change-password/', data),
    onSuccess: () => {
      toast({
        title: "Mot de passe modifié",
        description: "Votre mot de passe a été modifié avec succès."
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error?.response?.data?.message || "Impossible de modifier le mot de passe.",
        variant: "destructive"
      });
    }
  });
}

export function useUpdatePreferences() {
  const queryClient = useQueryClient();
  const { toast } = useToast();
  
  return useMutation({
    mutationFn: (data: any) => apiService.patch('/settings/preferences/', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['preferences'] });
      toast({
        title: "Préférences mises à jour",
        description: "Vos préférences ont été sauvegardées."
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error?.response?.data?.message || "Impossible de sauvegarder les préférences.",
        variant: "destructive"
      });
    }
  });
}

// ==================== HOOKS ANALYTICS ====================

export function useAnalytics(params?: { period?: string }) {
  return useQuery({
    queryKey: ['analytics', params],
    queryFn: () => apiService.get('/analytics/analytics/', { params }),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

// ==================== HOOKS DÉPENSES ====================

export function useExpenses(params?: {
  category?: number;
  search?: string;
  is_approved?: boolean;
  start_date?: string;
  end_date?: string;
}) {
  return useQuery<PaginatedResponse<Expense>, Error, PaginatedResponse<Expense>>({
    queryKey: ['expenses', params],
    queryFn: () => apiService.get('/expenses/', { params }),
    staleTime: 1 * 60 * 1000, // 1 minute
  });
}

export function useExpenseCategories(params?: { search?: string; is_active?: boolean }) {
  return useQuery<PaginatedResponse<ExpenseCategory>, Error, PaginatedResponse<ExpenseCategory>>({
    queryKey: ['expense-categories', params],
    queryFn: () => apiService.get('/expenses/categories/', { params }),
    staleTime: 10 * 60 * 1000, // 10 minutes
  });
}

export function useCreateExpense() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: (data: Omit<Expense, 'id' | 'created_at' | 'updated_at'>) =>
      apiService.post('/expenses/', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['expenses'] });
      toast({
        title: "Succès",
        description: "Dépense créée avec succès",
        variant: "default",
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error.message || "Erreur lors de la création de la dépense",
        variant: "destructive",
      });
    },
  });
}

// ==================== HOOKS STOCKS ET INVENTAIRE ====================

export function useStockMovements(params?: {
  product?: number;
  movement_type?: string;
  start_date?: string;
  end_date?: string;
}) {
  return useQuery<PaginatedResponse<StockMovement>, Error, PaginatedResponse<StockMovement>>({
    queryKey: ['inventory', 'movements', params],
    queryFn: () => apiService.get('/inventory/movements/', { params }),
    staleTime: 1 * 60 * 1000, // 1 minute
  });
}

export function useStockSummary() {
  return useQuery({
    queryKey: ['inventory', 'stock-summary'],
    queryFn: () => apiService.get('/inventory/stock-summary/'),
    staleTime: 2 * 60 * 1000, // 2 minutes
  });
}

export function useLowStock() {
  return useQuery({
    queryKey: ['inventory', 'low-stock'],
    queryFn: () => apiService.get('/inventory/low-stock/'),
    staleTime: 1 * 60 * 1000, // 1 minute
  });
}

export function usePurchases(params?: {
  supplier?: number;
  status?: string;
  start_date?: string;
  end_date?: string;
}) {
  return useQuery<PaginatedResponse<Purchase>, Error, PaginatedResponse<Purchase>>({
    queryKey: ['inventory', 'purchases', params],
    queryFn: () => apiService.get('/inventory/purchases/', { params }),
    staleTime: 2 * 60 * 1000, // 2 minutes
  });
}

export function useCreateStockMovement() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: (data: Omit<StockMovement, 'id' | 'created_at' | 'updated_at'>) =>
      apiService.post('/inventory/movements/', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['inventory'] });
      queryClient.invalidateQueries({ queryKey: ['products'] });
      toast({
        title: "Succès",
        description: "Mouvement de stock enregistré",
        variant: "default",
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error.message || "Erreur lors de l'enregistrement du mouvement",
        variant: "destructive",
      });
    },
  });
}

// ==================== HOOKS GRAPHIQUES ET ANALYTICS ====================

export function useSalesChart(params?: {
  date?: string;
  period?: 'day' | 'week' | 'month';
}) {
  return useQuery<any, Error, any>({
    queryKey: ['analytics', 'sales-chart', params],
    queryFn: () => apiService.get('/analytics/sales-chart/', { params }),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

export function useProductSalesChart(params: {
  date?: string;
  period?: 'day' | 'week' | 'month';
} = {}) {
  return useQuery<any, Error, any>({
    queryKey: ['analytics', 'product-sales', params],
    queryFn: () => apiService.get('/analytics/product-sales/', { params }),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

// ==================== HOOKS RAPPORTS AVANCÉS ====================

export function useStockAlerts(params?: {
  alert_type?: string;
  is_resolved?: boolean;
}) {
  return useQuery<PaginatedResponse<StockAlert>, Error, PaginatedResponse<StockAlert>>({
    queryKey: ['reports', 'alerts', params],
    queryFn: () => apiService.get('/reports/alerts/', { params }),
    staleTime: 1 * 60 * 1000, // 1 minute
  });
}

export function useReportsSummary() {
  return useQuery({
    queryKey: ['reports', 'summary'],
    queryFn: () => apiService.get('/reports/summary/'),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

export function useExportReport() {
  const { toast } = useToast();

  return useMutation({
    mutationFn: ({ type, format, params }: {
      type: 'daily' | 'stock' | 'sales';
      format: 'pdf' | 'excel';
      params?: any
    }) => {
      const endpoint = `/reports/export/${type}-report/${format}/`;
      return apiService.get(endpoint, { params });
    },
    onSuccess: (data: any, variables) => {
      // Créer un lien de téléchargement
      const url = window.URL.createObjectURL(new Blob([data as BlobPart]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${variables.type}-report.${variables.format}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);

      toast({
        title: "Succès",
        description: "Rapport exporté avec succès",
        variant: "default",
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error.message || "Erreur lors de l'export",
        variant: "destructive",
      });
    },
  });
}

// ==================== HOOKS SETTINGS ====================

export function useSystemSettings() {
  return useQuery<any, Error>({
    queryKey: ['system-settings'],
    queryFn: () => apiService.get('/settings/system/'),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

export function useUpdateSystemSettings() {
  const queryClient = useQueryClient();
  const { toast } = useToast();
  
  return useMutation({
    mutationFn: (data: any) => apiService.patch('/settings/system/', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['system-settings'] });
      toast({
        title: "Paramètres sauvegardés",
        description: "Les paramètres système ont été mis à jour avec succès."
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error?.response?.data?.message || "Impossible de sauvegarder les paramètres.",
        variant: "destructive"
      });
    }
  });
}

export function useResetSystemSettings() {
  const queryClient = useQueryClient();
  const { toast } = useToast();
  
  return useMutation({
    mutationFn: () => apiService.post('/settings/reset/'),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['system-settings'] });
      toast({
        title: "Paramètres réinitialisés",
        description: "Tous les paramètres ont été restaurés aux valeurs par défaut."
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error?.response?.data?.message || "Impossible de réinitialiser les paramètres.",
        variant: "destructive"
      });
    }
  });
}

export function useCreateBackup() {
  const { toast } = useToast();
  
  return useMutation({
    mutationFn: () => apiService.post('/settings/backup/create/'),
    onSuccess: (data: any) => {
      toast({
        title: "Sauvegarde créée",
        description: `Sauvegarde créée avec succès: ${data.filename || 'backup.sql'}`
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error?.response?.data?.message || "Impossible de créer la sauvegarde.",
        variant: "destructive"
      });
    }
  });
}

export function useDeleteUser() {
  const queryClient = useQueryClient();
  const { toast } = useToast();
  
  return useMutation({
    mutationFn: (userId: string) => apiService.delete(`/accounts/users/${userId}/`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
      toast({
        title: "Utilisateur supprimé",
        description: "L'utilisateur a été supprimé avec succès"
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error?.response?.data?.message || "Impossible de supprimer l'utilisateur.",
        variant: "destructive"
      });
    }
  });
}

export function useSystemInfo() {
  return useQuery<any, Error>({
    queryKey: ['system-info'],
    queryFn: () => apiService.get('/settings/system-info/'),
    staleTime: 2 * 60 * 1000, // 2 minutes
    refetchInterval: 5 * 60 * 1000, // Refresh every 5 minutes
  });
}


// Hooks pour les réservations
export const useReservations = (params?: {
  date?: string;
  status?: string;
  table?: number;
}) => {
  return useQuery({
    queryKey: ['reservations', params],
    queryFn: () => apiService.get('/sales/reservations/', { params }),
    staleTime: 30000,
  });
};

export const useCreateReservation = () => {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: (data: {
      table: number;
      customer_name: string;
      customer_phone?: string;
      customer_email?: string;
      party_size: number;
      reservation_date: string;
      reservation_time: string;
      duration_minutes?: number;
      special_requests?: string;
    }) => apiService.post('/sales/reservations/', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['reservations'] });
      queryClient.invalidateQueries({ queryKey: ['tables'] });
      toast({
        title: "Succès",
        description: "Réservation créée avec succès",
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error.message || "Erreur lors de la création de la réservation",
        variant: "destructive",
      });
    },
  });
};

export const useConfirmReservation = () => {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: (reservationId: number) =>
      apiService.post(`/sales/reservations/${reservationId}/confirm/`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['reservations'] });
      toast({
        title: "Succès",
        description: "Réservation confirmée",
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error.message || "Erreur lors de la confirmation",
        variant: "destructive",
      });
    },
  });
};

export const useConvertOrderToSale = () => {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: ({ orderId, data }: {
      orderId: number;
      data: { payment_method: string; notes?: string }
    }) => apiService.post(`/orders/${orderId}/convert-to-sale/`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['orders'] });
      queryClient.invalidateQueries({ queryKey: ['sales'] });
      queryClient.invalidateQueries({ queryKey: ['tables'] });
      toast({
        title: "Succès",
        description: "Commande convertie en vente",
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error.message || "Erreur lors de la conversion",
        variant: "destructive",
      });
    },
  });
};

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
}

export function useUpdateOrder() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) =>
      apiService.patch(`/orders/${id}/`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['orders'] });
      toast({
        title: "Succès",
        description: "Commande mise à jour",
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
}

export function useUserProfile() {
  return useQuery({
    queryKey: ['profile'],
    queryFn: () => apiService.get('/accounts/profile/'),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}