import { useState } from "react";
import { Sidebar } from "@/components/layout/Sidebar";
import { Header } from "@/components/layout/Header";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Textarea } from "@/components/ui/textarea";
import {
  Truck,
  Plus,
  Package,
  Calendar,
  User,
  FileText,
  CheckCircle,
  Clock,
  AlertTriangle,
  Eye,
  Check,
  X,
  Trash2
} from "lucide-react";
import { useSupplies, useSuppliers, useProducts, useCreateSupply, useValidateSupply, useRejectSupply } from "@/hooks/use-api";
import { useToast } from "@/hooks/use-toast";

interface Supply {
  id: string;
  supplierName: string;
  deliveryDate: string;
  status: "pending" | "delivered" | "validated" | "rejected";
  items: {
    productName: string;
    quantityOrdered: number;
    quantityReceived: number;
    unitPrice: number;
  }[];
  totalAmount: number;
  notes?: string;
}

const mockSupplies: Supply[] = [
  {
    id: "1",
    supplierName: "Brarudi SA",
    deliveryDate: "2024-08-14",
    status: "delivered",
    items: [
      { productName: "Bière Mutzig", quantityOrdered: 48, quantityReceived: 48, unitPrice: 800 },
      { productName: "Primus", quantityOrdered: 24, quantityReceived: 24, unitPrice: 750 }
    ],
    totalAmount: 56400,
    notes: "Livraison conforme, produits en bon état"
  },
  {
    id: "2",
    supplierName: "Distillerie Centrale",
    deliveryDate: "2024-08-15",
    status: "pending",
    items: [
      { productName: "Whisky JW Red", quantityOrdered: 12, quantityReceived: 0, unitPrice: 35000 },
      { productName: "Vodka Smirnoff", quantityOrdered: 6, quantityReceived: 0, unitPrice: 40000 }
    ],
    totalAmount: 660000
  }
];

const mockSuppliers = [
  { id: "1", name: "Brarudi SA", category: "Bières" },
  { id: "2", name: "Distillerie Centrale", category: "Liqueurs" },
  { id: "3", name: "Coca-Cola Burundi", category: "Boissons" }
];

export default function Supplies() {
  const [showNewSupplyDialog, setShowNewSupplyDialog] = useState(false);
  const [selectedSupply, setSelectedSupply] = useState<Supply | null>(null);
  const [newSupply, setNewSupply] = useState({
    supplier: "",
    deliveryDate: "",
    notes: "",
    items: [{ product: "", quantityOrdered: 1, unitPrice: 0 }]
  });
  const { toast } = useToast();

  // Récupérer les données des approvisionnements depuis l'API
  const {
    data: suppliesData,
    isLoading: suppliesLoading,
    error: suppliesError,
    refetch: refetchSupplies
  } = useSupplies();

  // Récupérer les fournisseurs
  const {
    data: suppliersData,
    isLoading: suppliersLoading
  } = useSuppliers({ is_active: true });

  // Récupérer les produits
  const {
    data: productsData,
    isLoading: productsLoading
  } = useProducts();

  // Hooks pour les mutations
  const createSupplyMutation = useCreateSupply();
  const validateSupplyMutation = useValidateSupply();
  const rejectSupplyMutation = useRejectSupply();

  // Mapper les données de l'API
  const supplies = (suppliesData as any)?.results?.map((supply: any) => ({
    id: supply.id.toString(),
    supplierName: supply.supplier?.name || supply.supplier_name || "Fournisseur inconnu",
    deliveryDate: supply.delivery_date || supply.order_date,
    status: supply.status === 'received' ? 'delivered' : supply.status === 'validated' ? 'validated' : supply.status === 'cancelled' ? 'rejected' : 'pending',
    totalAmount: supply.total_amount || 0,
    items: supply.items?.map((item: any) => ({
      productName: item.product?.name || item.product_name || 'Produit inconnu',
      quantityOrdered: item.quantity_ordered || 0,
      quantityReceived: item.quantity_received || 0,
      unitPrice: item.unit_price || 0
    })) || [],
    notes: supply.notes
  })) || [];

  const getStatusInfo = (status: Supply["status"]) => {
    switch (status) {
      case "pending":
        return { variant: "warning" as const, label: "En attente", icon: Clock };
      case "delivered":
        return { variant: "secondary" as const, label: "Livrée", icon: Truck };
      case "validated":
        return { variant: "success" as const, label: "Validée", icon: CheckCircle };
      case "rejected":
        return { variant: "destructive" as const, label: "Rejetée", icon: AlertTriangle };
    }
  };

  const validateDelivery = (supplyId: string) => {
    validateSupplyMutation.mutate(parseInt(supplyId));
  };

  const rejectDelivery = (supplyId: string) => {
    rejectSupplyMutation.mutate(parseInt(supplyId));
  };

  // Fonctions de gestion du formulaire
  const addItem = () => {
    setNewSupply(prev => ({
      ...prev,
      items: [...prev.items, { product: "", quantityOrdered: 1, unitPrice: 0 }]
    }));
  };

  const removeItem = (index: number) => {
    setNewSupply(prev => ({
      ...prev,
      items: prev.items.filter((_, i) => i !== index)
    }));
  };

  const updateItem = (index: number, field: string, value: any) => {
    setNewSupply(prev => ({
      ...prev,
      items: prev.items.map((item, i) =>
        i === index ? { ...item, [field]: value } : item
      )
    }));
  };

  const calculateTotal = () => {
    return newSupply.items.reduce((total, item) => {
      return total + (item.quantityOrdered * item.unitPrice);
    }, 0);
  };

  const addNewSupply = () => {
    // Validation
    if (!newSupply.supplier || !newSupply.deliveryDate) {
      toast({
        title: "Erreur",
        description: "Veuillez sélectionner un fournisseur et une date de livraison.",
        variant: "destructive"
      });
      return;
    }

    if (newSupply.items.some(item => !item.product || item.quantityOrdered <= 0 || item.unitPrice <= 0)) {
      toast({
        title: "Erreur",
        description: "Veuillez remplir tous les champs des articles avec des valeurs valides.",
        variant: "destructive"
      });
      return;
    }

    const supplyData = {
      supplier: parseInt(newSupply.supplier),
      delivery_date: newSupply.deliveryDate,
      notes: newSupply.notes,
      status: 'pending',
      items: newSupply.items.map(item => ({
        product: parseInt(item.product),
        quantity_ordered: item.quantityOrdered,
        quantity_received: 0,
        unit_price: item.unitPrice
      }))
    };

    createSupplyMutation.mutate(supplyData, {
      onSuccess: () => {
        toast({
          title: "Succès",
          description: "Approvisionnement créé avec succès.",
        });
        setShowNewSupplyDialog(false);
        setNewSupply({
          supplier: "",
          deliveryDate: "",
          notes: "",
          items: [{ product: "", quantityOrdered: 1, unitPrice: 0 }]
        });
        refetchSupplies();
      },
      onError: (error: any) => {
        toast({
          title: "Erreur",
          description: error.message || "Erreur lors de la création de l'approvisionnement.",
          variant: "destructive"
        });
      }
    });
  };

  return (
    <div className="min-h-screen bg-gradient-surface flex">
      <Sidebar />
      
      <div className="flex-1 flex flex-col">
        <Header />
        
        <main className="flex-1 p-6 space-y-6">
          {/* Header */}
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-foreground mb-2">
                Approvisionnements
              </h1>
              <p className="text-muted-foreground">
                Gérez vos livraisons et mettez à jour vos stocks
              </p>
            </div>
            <Dialog open={showNewSupplyDialog} onOpenChange={setShowNewSupplyDialog}>
              <DialogTrigger asChild>
                <Button className="gap-2">
                  <Plus className="h-4 w-4" />
                  Nouvelle livraison
                </Button>
              </DialogTrigger>
              <DialogContent className="max-w-2xl">
                <DialogHeader>
                  <DialogTitle>Nouvelle livraison</DialogTitle>
                  <DialogDescription>
                    Enregistrez une nouvelle livraison de marchandises
                  </DialogDescription>
                </DialogHeader>
                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label>Fournisseur *</Label>
                      <Select value={newSupply.supplier} onValueChange={(value) => setNewSupply(prev => ({...prev, supplier: value}))}>
                        <SelectTrigger>
                          <SelectValue placeholder="Sélectionner un fournisseur" />
                        </SelectTrigger>
                        <SelectContent>
                          {suppliersLoading ? (
                            <SelectItem value="loading" disabled>Chargement...</SelectItem>
                          ) : (
                            (suppliersData as any)?.results?.map((supplier: any) => (
                              <SelectItem key={supplier.id} value={supplier.id.toString()}>
                                {supplier.name}
                              </SelectItem>
                            )) || []
                          )}
                        </SelectContent>
                      </Select>
                    </div>
                    <div className="space-y-2">
                      <Label>Date de livraison *</Label>
                      <Input
                        type="date"
                        value={newSupply.deliveryDate}
                        onChange={(e) => setNewSupply(prev => ({...prev, deliveryDate: e.target.value}))}
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label>Notes (optionnel)</Label>
                    <Input
                      placeholder="Notes sur l'approvisionnement..."
                      value={newSupply.notes}
                      onChange={(e) => setNewSupply(prev => ({...prev, notes: e.target.value}))}
                    />
                  </div>

                  <div className="space-y-2">
                    <Label>Produits *</Label>
                    {newSupply.items.map((item, index) => (
                      <div key={index} className="grid grid-cols-4 gap-2 items-end">
                        <div>
                          <Select value={item.product} onValueChange={(value) => updateItem(index, 'product', value)}>
                            <SelectTrigger>
                              <SelectValue placeholder="Produit" />
                            </SelectTrigger>
                            <SelectContent>
                              {productsLoading ? (
                                <SelectItem value="loading" disabled>Chargement...</SelectItem>
                              ) : (
                                (productsData as any)?.results?.map((product: any) => (
                                  <SelectItem key={product.id} value={product.id.toString()}>
                                    {product.name} - {product.selling_price} FBu
                                  </SelectItem>
                                )) || []
                              )}
                            </SelectContent>
                          </Select>
                        </div>
                        <div>
                          <Input
                            placeholder="Qté"
                            type="number"
                            min="1"
                            value={item.quantityOrdered}
                            onChange={(e) => updateItem(index, 'quantityOrdered', parseInt(e.target.value) || 1)}
                          />
                        </div>
                        <div>
                          <Input
                            placeholder="Prix unitaire (FBu)"
                            type="number"
                            min="0"
                            step="0.01"
                            value={item.unitPrice}
                            onChange={(e) => updateItem(index, 'unitPrice', parseFloat(e.target.value) || 0)}
                          />
                        </div>
                        <div className="flex items-center gap-2">
                          <span className="text-sm font-medium">
                            {(item.quantityOrdered * item.unitPrice).toLocaleString()} FBu
                          </span>
                          {newSupply.items.length > 1 && (
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => removeItem(index)}
                              className="text-red-600 hover:text-red-700"
                            >
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          )}
                        </div>
                      </div>
                    ))}
                    <div className="flex justify-between items-center">
                      <Button
                        variant="outline"
                        onClick={addItem}
                        className="flex-1 mr-4"
                      >
                        <Plus className="h-4 w-4 mr-2" />
                        Ajouter un produit
                      </Button>
                      <div className="text-right">
                        <div className="text-sm text-gray-600">Total</div>
                        <div className="text-lg font-bold">
                          {calculateTotal().toLocaleString()} FBu
                        </div>
                      </div>
                    </div>
                  </div>

                  <Button 
                    onClick={addNewSupply} 
                    className="w-full"
                    disabled={createSupplyMutation.isPending}
                  >
                    {createSupplyMutation.isPending ? "Enregistrement..." : "Enregistrer la livraison"}
                  </Button>
                </div>
              </DialogContent>
            </Dialog>
          </div>

          {/* Supplies List */}
          <div className="space-y-4">
            {suppliesLoading ? (
              <div className="flex items-center justify-center py-8">
                <div className="text-center">
                  <Package className="h-12 w-12 mx-auto mb-4 opacity-50" />
                  <p>Chargement des approvisionnements...</p>
                </div>
              </div>
            ) : supplies.length === 0 ? (
              <div className="flex items-center justify-center py-8">
                <div className="text-center">
                  <Package className="h-12 w-12 mx-auto mb-4 opacity-50" />
                  <p>Aucun approvisionnement trouvé</p>
                  <p className="text-sm text-muted-foreground">Créez votre première livraison</p>
                </div>
              </div>
            ) : supplies.map((supply) => {
              const statusInfo = getStatusInfo(supply.status);
              const StatusIcon = statusInfo.icon;
              
              return (
                <Card key={supply.id}>
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <div>
                        <CardTitle className="flex items-center gap-2">
                          <Truck className="h-5 w-5" />
                          {supply.supplierName}
                        </CardTitle>
                        <CardDescription className="flex items-center gap-2">
                          <Calendar className="h-4 w-4" />
                          Livraison: {supply.deliveryDate}
                        </CardDescription>
                      </div>
                      <div className="text-right">
                        <Badge variant={statusInfo.variant} className="gap-1">
                          <StatusIcon className="h-3 w-3" />
                          {statusInfo.label}
                        </Badge>
                        <p className="text-lg font-bold mt-1">
                          {supply.totalAmount.toLocaleString()} FBu
                        </p>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {/* Items */}
                      <div className="space-y-2">
                        <h4 className="font-medium">Produits livrés:</h4>
                        {supply.items.map((item, index) => (
                          <div key={index} className="flex items-center justify-between p-2 bg-muted rounded">
                            <span className="font-medium">{item.productName}</span>
                            <div className="text-right">
                              <span className="text-sm">
                                {item.quantityReceived}/{item.quantityOrdered} unités
                              </span>
                              <p className="text-xs text-muted-foreground">
                                {item.unitPrice} FBu/unité
                              </p>
                            </div>
                          </div>
                        ))}
                      </div>

                      {/* Notes */}
                      {supply.notes && (
                        <div className="p-3 bg-muted rounded">
                          <p className="text-sm">{supply.notes}</p>
                        </div>
                      )}

                      {/* Actions */}
                      {supply.status === "delivered" && (
                        <div className="flex gap-2">
                          <Button 
                            onClick={() => validateDelivery(supply.id)}
                            className="gap-2"
                            disabled={validateSupplyMutation.isPending}
                          >
                            <CheckCircle className="h-4 w-4" />
                            {validateSupplyMutation.isPending ? "Validation..." : "Valider et mettre à jour le stock"}
                          </Button>
                          <Button 
                            variant="destructive"
                            onClick={() => rejectDelivery(supply.id)}
                            className="gap-2"
                            disabled={rejectSupplyMutation.isPending}
                          >
                            <AlertTriangle className="h-4 w-4" />
                            {rejectSupplyMutation.isPending ? "Rejet..." : "Rejeter"}
                          </Button>
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </main>
      </div>
    </div>
  );
}
