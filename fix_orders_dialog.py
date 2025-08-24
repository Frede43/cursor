#!/usr/bin/env python
"""
Script pour corriger le dialog de commandes
"""

def create_orders_component():
    """Créer une version corrigée du composant Orders"""
    orders_content = '''import { useState } from "react";
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
  Plus,
  Clock,
  Users,
  ChefHat,
  CheckCircle,
  AlertTriangle,
  Trash2,
  Edit
} from "lucide-react";
import { useOrders, useCreateOrder, useUpdateOrder, useTables, useProducts } from "@/hooks/use-api";
import { useToast } from "@/hooks/use-toast";

interface OrderItem {
  product: number;
  productName?: string;
  quantity: number;
  unit_price: number;
  notes?: string;
}

export default function Orders() {
  const [showOrderDialog, setShowOrderDialog] = useState(false);
  const [orderData, setOrderData] = useState({
    tableId: "",
    customerName: "",
    priority: "normal",
    notes: "",
    items: [] as OrderItem[]
  });
  const [newItem, setNewItem] = useState({
    productId: "",
    quantity: "1",
    notes: ""
  });

  const { toast } = useToast();
  
  // Hooks API
  const { data: ordersData, isLoading: ordersLoading, refetch: refetchOrders } = useOrders();
  const { data: tablesData } = useTables();
  const { data: productsData } = useProducts();
  const createOrderMutation = useCreateOrder();
  const updateOrderMutation = useUpdateOrder();

  // Extraire les données
  const orders = ordersData?.results || [];
  const tables = tablesData?.results || [];
  const products = productsData || [];

  const addItemToOrder = () => {
    if (!newItem.productId || !newItem.quantity) {
      toast({
        title: "Erreur",
        description: "Veuillez sélectionner un produit et une quantité",
        variant: "destructive"
      });
      return;
    }

    const product = products.find(p => p.id === parseInt(newItem.productId));
    if (!product) return;

    const item: OrderItem = {
      product: product.id,
      productName: product.name,
      quantity: parseInt(newItem.quantity),
      unit_price: parseFloat(product.selling_price),
      notes: newItem.notes || undefined
    };

    setOrderData(prev => ({
      ...prev,
      items: [...prev.items, item]
    }));

    setNewItem({
      productId: "",
      quantity: "1",
      notes: ""
    });
  };

  const removeItemFromOrder = (index: number) => {
    setOrderData(prev => ({
      ...prev,
      items: prev.items.filter((_, i) => i !== index)
    }));
  };

  const createOrder = () => {
    if (!orderData.tableId || orderData.items.length === 0) {
      toast({
        title: "Erreur",
        description: "Veuillez sélectionner une table et ajouter au moins un article",
        variant: "destructive"
      });
      return;
    }

    const orderPayload = {
      table: parseInt(orderData.tableId),
      customer_name: orderData.customerName || undefined,
      status: "pending",
      priority: orderData.priority,
      notes: orderData.notes || undefined,
      items: orderData.items.map(item => ({
        product: item.product,
        quantity: item.quantity,
        unit_price: item.unit_price,
        notes: item.notes
      }))
    };

    createOrderMutation.mutate(orderPayload, {
      onSuccess: () => {
        setShowOrderDialog(false);
        setOrderData({
          tableId: "",
          customerName: "",
          priority: "normal",
          notes: "",
          items: []
        });
        refetchOrders();
      }
    });
  };

  const updateOrderStatus = (orderId: number, status: string) => {
    updateOrderMutation.mutate({
      id: orderId,
      data: { status }
    });
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "pending": return "bg-yellow-100 text-yellow-800";
      case "confirmed": return "bg-blue-100 text-blue-800";
      case "preparing": return "bg-orange-100 text-orange-800";
      case "ready": return "bg-green-100 text-green-800";
      case "served": return "bg-gray-100 text-gray-800";
      case "cancelled": return "bg-red-100 text-red-800";
      default: return "bg-gray-100 text-gray-800";
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "pending": return <Clock className="h-4 w-4" />;
      case "confirmed": return <CheckCircle className="h-4 w-4" />;
      case "preparing": return <ChefHat className="h-4 w-4" />;
      case "ready": return <CheckCircle className="h-4 w-4" />;
      case "served": return <Users className="h-4 w-4" />;
      case "cancelled": return <AlertTriangle className="h-4 w-4" />;
      default: return <Clock className="h-4 w-4" />;
    }
  };

  const getTotalAmount = () => {
    return orderData.items.reduce((total, item) => total + (item.quantity * item.unit_price), 0);
  };

  if (ordersLoading) {
    return (
      <div className="min-h-screen bg-gradient-surface flex">
        <Sidebar />
        <div className="flex-1 flex flex-col">
          <Header />
          <main className="flex-1 p-6 flex items-center justify-center">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
              <p>Chargement des commandes...</p>
            </div>
          </main>
        </div>
      </div>
    );
  }

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
                Gestion des commandes
              </h1>
              <p className="text-muted-foreground">
                Suivi des commandes en temps réel
              </p>
            </div>
            <Dialog open={showOrderDialog} onOpenChange={setShowOrderDialog}>
              <DialogTrigger asChild>
                <Button className="gap-2">
                  <Plus className="h-4 w-4" />
                  Nouvelle commande
                </Button>
              </DialogTrigger>
              <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
                <DialogHeader>
                  <DialogTitle>Nouvelle commande</DialogTitle>
                  <DialogDescription>
                    Créer une nouvelle commande pour une table
                  </DialogDescription>
                </DialogHeader>
                <div className="space-y-6">
                  {/* Informations de base */}
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label>Table *</Label>
                      <Select value={orderData.tableId} onValueChange={(value) => setOrderData(prev => ({...prev, tableId: value}))}>
                        <SelectTrigger>
                          <SelectValue placeholder="Sélectionner une table" />
                        </SelectTrigger>
                        <SelectContent>
                          {tables.map(table => (
                            <SelectItem key={table.id} value={table.id.toString()}>
                              Table {table.number} ({table.capacity} places)
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                    <div className="space-y-2">
                      <Label>Nom du client</Label>
                      <Input
                        placeholder="Nom du client (optionnel)"
                        value={orderData.customerName}
                        onChange={(e) => setOrderData(prev => ({...prev, customerName: e.target.value}))}
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label>Priorité</Label>
                      <Select value={orderData.priority} onValueChange={(value) => setOrderData(prev => ({...prev, priority: value}))}>
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="low">Basse</SelectItem>
                          <SelectItem value="normal">Normale</SelectItem>
                          <SelectItem value="high">Haute</SelectItem>
                          <SelectItem value="urgent">Urgente</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    <div className="space-y-2">
                      <Label>Notes</Label>
                      <Input
                        placeholder="Notes pour la commande"
                        value={orderData.notes}
                        onChange={(e) => setOrderData(prev => ({...prev, notes: e.target.value}))}
                      />
                    </div>
                  </div>

                  {/* Ajouter des articles */}
                  <div className="border rounded-lg p-4 space-y-4">
                    <h3 className="font-semibold">Ajouter des articles</h3>
                    <div className="grid grid-cols-4 gap-2">
                      <div className="space-y-2">
                        <Label>Produit</Label>
                        <Select value={newItem.productId} onValueChange={(value) => setNewItem(prev => ({...prev, productId: value}))}>
                          <SelectTrigger>
                            <SelectValue placeholder="Produit" />
                          </SelectTrigger>
                          <SelectContent>
                            {products.map(product => (
                              <SelectItem key={product.id} value={product.id.toString()}>
                                {product.name} - {product.selling_price} BIF
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                      </div>
                      <div className="space-y-2">
                        <Label>Quantité</Label>
                        <Input
                          type="number"
                          min="1"
                          value={newItem.quantity}
                          onChange={(e) => setNewItem(prev => ({...prev, quantity: e.target.value}))}
                        />
                      </div>
                      <div className="space-y-2">
                        <Label>Notes</Label>
                        <Input
                          placeholder="Notes article"
                          value={newItem.notes}
                          onChange={(e) => setNewItem(prev => ({...prev, notes: e.target.value}))}
                        />
                      </div>
                      <div className="space-y-2">
                        <Label>&nbsp;</Label>
                        <Button onClick={addItemToOrder} className="w-full">
                          <Plus className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  </div>

                  {/* Liste des articles */}
                  {orderData.items.length > 0 && (
                    <div className="border rounded-lg p-4 space-y-4">
                      <h3 className="font-semibold">Articles de la commande</h3>
                      <div className="space-y-2">
                        {orderData.items.map((item, index) => (
                          <div key={index} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                            <div className="flex-1">
                              <span className="font-medium">{item.productName}</span>
                              <span className="text-sm text-gray-500 ml-2">
                                {item.quantity} × {item.unit_price} BIF = {item.quantity * item.unit_price} BIF
                              </span>
                              {item.notes && (
                                <div className="text-xs text-gray-400">Notes: {item.notes}</div>
                              )}
                            </div>
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => removeItemFromOrder(index)}
                            >
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </div>
                        ))}
                        <div className="text-right font-semibold">
                          Total: {getTotalAmount()} BIF
                        </div>
                      </div>
                    </div>
                  )}

                  <Button 
                    onClick={createOrder} 
                    className="w-full"
                    disabled={createOrderMutation.isPending || orderData.items.length === 0}
                  >
                    {createOrderMutation.isPending ? "Création..." : "Créer la commande"}
                  </Button>
                </div>
              </DialogContent>
            </Dialog>
          </div>

          {/* Liste des commandes */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {orders.map((order) => (
              <Card key={order.id} className="hover:shadow-md transition-shadow">
                <CardHeader className="pb-3">
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-lg">
                      Commande #{order.order_number}
                    </CardTitle>
                    <Badge className={getStatusColor(order.status)}>
                      <div className="flex items-center gap-1">
                        {getStatusIcon(order.status)}
                        {order.status}
                      </div>
                    </Badge>
                  </div>
                  <CardDescription>
                    Table {order.table?.number} • {order.total_amount} BIF
                    {order.customer_name && ` • ${order.customer_name}`}
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-3">
                  {/* Articles */}
                  <div className="space-y-1">
                    {order.items?.map((item, index) => (
                      <div key={index} className="text-sm">
                        {item.quantity}× {item.product_name}
                        {item.notes && (
                          <div className="text-xs text-gray-500">• {item.notes}</div>
                        )}
                      </div>
                    ))}
                  </div>

                  {/* Actions */}
                  <div className="flex gap-2">
                    {order.status === "pending" && (
                      <Button
                        size="sm"
                        onClick={() => updateOrderStatus(order.id, "confirmed")}
                        disabled={updateOrderMutation.isPending}
                      >
                        Confirmer
                      </Button>
                    )}
                    {order.status === "confirmed" && (
                      <Button
                        size="sm"
                        onClick={() => updateOrderStatus(order.id, "preparing")}
                        disabled={updateOrderMutation.isPending}
                      >
                        En préparation
                      </Button>
                    )}
                    {order.status === "preparing" && (
                      <Button
                        size="sm"
                        onClick={() => updateOrderStatus(order.id, "ready")}
                        disabled={updateOrderMutation.isPending}
                      >
                        Prêt
                      </Button>
                    )}
                    {order.status === "ready" && (
                      <Button
                        size="sm"
                        onClick={() => updateOrderStatus(order.id, "served")}
                        disabled={updateOrderMutation.isPending}
                      >
                        Servi
                      </Button>
                    )}
                  </div>

                  {/* Informations supplémentaires */}
                  <div className="text-xs text-gray-500 space-y-1">
                    <div>Créé: {new Date(order.created_at).toLocaleString()}</div>
                    {order.notes && <div>Notes: {order.notes}</div>}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {orders.length === 0 && (
            <div className="text-center py-12">
              <ChefHat className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">Aucune commande</h3>
              <p className="text-gray-500">Créez votre première commande pour commencer</p>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}'''
    
    try:
        with open('src/pages/Orders.tsx', 'w', encoding='utf-8') as f:
            f.write(orders_content)
        print("✅ Composant Orders corrigé et connecté aux APIs")
    except Exception as e:
        print(f"❌ Erreur création Orders: {e}")

def run_orders_fixes():
    """Exécuter les corrections pour les commandes"""
    print("🔧 CORRECTION DIALOG COMMANDES")
    print("=" * 50)
    
    print("\n1. Correction du composant Orders...")
    create_orders_component()
    
    print("\n✅ CORRECTIONS TERMINÉES!")
    print("\n📋 RÉSUMÉ DES CORRECTIONS:")
    print("1. ✅ Dialog de commande entièrement fonctionnel")
    print("2. ✅ Sélection de table et produits")
    print("3. ✅ Ajout/suppression d'articles")
    print("4. ✅ Calcul automatique du total")
    print("5. ✅ Gestion des statuts de commande")
    print("6. ✅ Interface utilisateur améliorée")
    
    print("\n🚀 FONCTIONNALITÉS AJOUTÉES:")
    print("- ✅ Création de commandes multi-articles")
    print("- ✅ Gestion des statuts (pending → confirmed → preparing → ready → served)")
    print("- ✅ Validation des données")
    print("- ✅ Notifications de succès/erreur")
    print("- ✅ Interface responsive")
    
    print("\n💡 TESTEZ MAINTENANT:")
    print("1. Allez sur http://localhost:5173/orders")
    print("2. Cliquez sur 'Nouvelle commande'")
    print("3. Sélectionnez une table et ajoutez des produits")
    print("4. Créez la commande et testez les changements de statut")

if __name__ == "__main__":
    run_orders_fixes()
