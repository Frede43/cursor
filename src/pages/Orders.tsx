import { useState, useEffect } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { Sidebar } from "@/components/layout/Sidebar";
import { Header } from "@/components/layout/Header";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Progress } from "@/components/ui/progress";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Textarea } from "@/components/ui/textarea";
import { useOrders, useUpdateOrderStatus, useKitchenQueue, useTables, useMenuItems, useCreateOrder } from "@/hooks/use-api";
import { useToast } from "@/hooks/use-toast";
import { Order, OrderItem } from "@/types/api";
import {
  Clock,
  CheckCircle,
  AlertTriangle,
  ChefHat,
  Bell,
  Timer,
  Users,
  Package,
  Play,
  Pause,
  Check,
  Plus,
  Search,
  Filter,
  RefreshCw,
  Minus,
  X
} from "lucide-react";


export default function Orders() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [currentTime, setCurrentTime] = useState(new Date());
  const [selectedStatus, setSelectedStatus] = useState("all");
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedTable, setSelectedTable] = useState("all");
  const [showNewOrderDialog, setShowNewOrderDialog] = useState(false);
  const [newOrder, setNewOrder] = useState({
    table_id: "",
    notes: "",
    priority: "normal" as const,
    items: [] as { menu_item_id: number; quantity: number; notes: string }[]
  });
  const { toast } = useToast();

  // Récupérer les paramètres de table depuis l'URL
  const preSelectedTable = searchParams.get('table');
  const preSelectedTableNumber = searchParams.get('tableNumber');
  const preSelectedServer = searchParams.get('server');
  const preSelectedCapacity = searchParams.get('capacity');
  const preSelectedLocation = searchParams.get('location');
  
  const { data: ordersData, isLoading, refetch } = useOrders({
    status: selectedStatus !== "all" ? selectedStatus : undefined
  });
  
  const { data: kitchenData } = useKitchenQueue();
  const { data: tablesData } = useTables();
  const { data: menuItemsData } = useMenuItems();
  const updateOrderMutation = useUpdateOrderStatus();
  const createOrderMutation = useCreateOrder();
  
  const orders = ordersData?.results || [];
  const kitchenOrders = (kitchenData as Order[]) || [];
  const tables = tablesData?.results || [];
  const menuItems = menuItemsData?.results || [];

  // Extract unique servers from orders
  const servers = Array.from(new Set(orders.map(order => `${order.server.first_name} ${order.server.last_name}`)));

  // Filtered orders based on search and filters
  const filteredOrders = orders.filter(order => {
    const matchesSearch = searchTerm === "" || 
      order.order_number.toLowerCase().includes(searchTerm.toLowerCase()) ||
      `${order.server.first_name} ${order.server.last_name}`.toLowerCase().includes(searchTerm.toLowerCase()) ||
      order.table.number.toString().includes(searchTerm);
    
    const matchesTable = selectedTable === "all" || order.table.id.toString() === selectedTable;
    
    return matchesSearch && matchesTable;
  });

  // Update current time every minute
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 60000);
    return () => clearInterval(timer);
  }, []);

  // Notification pour table pré-sélectionnée
  useEffect(() => {
    if (preSelectedTable && preSelectedTableNumber && preSelectedServer) {
      toast({
        title: "Table pré-sélectionnée",
        description: `Table ${preSelectedTableNumber} (${preSelectedCapacity} places) - ${preSelectedServer}`,
        variant: "default",
      });
    }
  }, [preSelectedTable, preSelectedTableNumber, preSelectedServer, preSelectedCapacity, toast]);



  const getStatusInfo = (status: Order["status"]) => {
    switch (status) {
      case "pending":
        return { variant: "warning" as const, label: "En attente", icon: Clock, color: "bg-warning" };
      case "preparing":
        return { variant: "secondary" as const, label: "Préparation", icon: ChefHat, color: "bg-secondary" };
      case "ready":
        return { variant: "success" as const, label: "Prête", icon: Bell, color: "bg-success" };
      case "served":
        return { variant: "default" as const, label: "Servie", icon: CheckCircle, color: "bg-muted" };
      case "cancelled":
        return { variant: "destructive" as const, label: "Annulée", icon: AlertTriangle, color: "bg-destructive" };
    }
  };

  const getPriorityInfo = (priority: Order["priority"]) => {
    switch (priority) {
      case "normal":
        return { variant: "secondary" as const, label: "Normal" };
      case "high":
        return { variant: "warning" as const, label: "Prioritaire" };
      case "urgent":
        return { variant: "destructive" as const, label: "Urgent" };
    }
  };

  const handleUpdateOrderStatus = async (orderId: number, action: string) => {
    try {
      await updateOrderMutation.mutateAsync({ orderId, action });
      refetch();
    } catch (error) {
      console.error('Erreur lors de la mise à jour du statut:', error);
    }
  };

  const getElapsedTime = (createdAt: string) => {
    const orderDate = new Date(createdAt);
    const elapsed = Math.floor((currentTime.getTime() - orderDate.getTime()) / (1000 * 60));
    return Math.max(0, elapsed);
  };

  const getOrdersByStatus = (status: Order["status"]) => {
    return filteredOrders.filter(order => order.status === status);
  };

  const addItemToOrder = (menuItemId: number) => {
    const existingItem = newOrder.items.find(item => item.menu_item_id === menuItemId);
    if (existingItem) {
      setNewOrder(prev => ({
        ...prev,
        items: prev.items.map(item =>
          item.menu_item_id === menuItemId
            ? { ...item, quantity: item.quantity + 1 }
            : item
        )
      }));
    } else {
      setNewOrder(prev => ({
        ...prev,
        items: [...prev.items, { menu_item_id: menuItemId, quantity: 1, notes: "" }]
      }));
    }
  };

  const removeItemFromOrder = (menuItemId: number) => {
    setNewOrder(prev => ({
      ...prev,
      items: prev.items.filter(item => item.menu_item_id !== menuItemId)
    }));
  };

  const updateItemQuantity = (menuItemId: number, quantity: number) => {
    if (quantity <= 0) {
      removeItemFromOrder(menuItemId);
      return;
    }
    setNewOrder(prev => ({
      ...prev,
      items: prev.items.map(item =>
        item.menu_item_id === menuItemId
          ? { ...item, quantity }
          : item
      )
    }));
  };

  const createNewOrderHandler = async () => {
    if (!newOrder.table_id || newOrder.items.length === 0) {
      toast({
        title: "Erreur",
        description: "Veuillez sélectionner une table et ajouter des articles",
        variant: "destructive"
      });
      return;
    }

    try {
      await createOrderMutation.mutateAsync(newOrder);
      setShowNewOrderDialog(false);
      setNewOrder({
        table_id: "",
        notes: "",
        priority: "normal",
        items: []
      });
      refetch();
    } catch (error) {
      // Error handling is done in the mutation hook
    }
  };

  const getAveragePreparationTime = () => {
    const servedOrders = orders.filter(order => order.estimated_time);
    if (servedOrders.length === 0) return 0;
    const total = servedOrders.reduce((sum, order) => sum + (order.estimated_time || 0), 0);
    return Math.round(total / servedOrders.length);
  };

  const getTimeProgress = (order: Order) => {
    if (!order.estimated_time) return 0;
    const elapsed = getElapsedTime(order.created_at);
    return Math.min((elapsed / order.estimated_time) * 100, 100);
  };

  const createNewOrder = () => {
    if (preSelectedTable && preSelectedTableNumber && preSelectedServer) {
      // Simuler la création d'une nouvelle commande
      toast({
        title: "Commande créée !",
        description: `Nouvelle commande créée pour table ${preSelectedTableNumber}`,
        variant: "default",
      });

      // Supprimer les paramètres de l'URL après création
      window.history.replaceState({}, '', '/orders');
    } else {
      toast({
        title: "Erreur",
        description: "Informations de table manquantes",
        variant: "destructive",
      });
    }
  };

  const processOrderPayment = async (order: Order) => {
    try {
      // Préparer les données pour la vente (conversion Order → Sale)
      const saleItems = order.items.map(item => ({
        menu_item_id: item.product.id,
        quantity: item.quantity
      }));

      // Naviguer vers Sales avec les données de la commande
      const saleData = {
        orderId: order.id,
        tableId: order.table.id,
        tableNumber: order.table.number,
        serverId: order.server.id,
        serverName: `${order.server.first_name} ${order.server.last_name}`,
        items: saleItems,
        totalAmount: order.total_amount
      };

      // Encoder les données pour l'URL
      const encodedData = encodeURIComponent(JSON.stringify(saleData));
      navigate(`/sales?orderData=${encodedData}`);

      toast({
        title: "Redirection vers encaissement",
        description: `Commande ${order.order_number} prête pour encaissement`,
        variant: "default",
      });

    } catch (error) {
      toast({
        title: "Erreur",
        description: "Impossible de traiter l'encaissement",
        variant: "destructive",
      });
    }
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
                Gestion des commandes
              </h1>
              <p className="text-muted-foreground">
                Suivi en temps réel des commandes et optimisation des délais
              </p>
            </div>
            <div className="flex items-center gap-4">
              <div className="text-right">
                <p className="text-sm text-muted-foreground">Temps moyen de préparation</p>
                <p className="text-xl font-bold">{getAveragePreparationTime()} min</p>
              </div>
              <Dialog open={showNewOrderDialog} onOpenChange={setShowNewOrderDialog}>
                <DialogTrigger asChild>
                  <Button className="gap-2">
                    <Plus className="h-4 w-4" />
                    Nouvelle commande
                  </Button>
                </DialogTrigger>
                <DialogContent className="max-w-4xl max-h-[80vh] overflow-y-auto">
                  <DialogHeader>
                    <DialogTitle>Créer une nouvelle commande</DialogTitle>
                    <DialogDescription>
                      Sélectionnez une table et ajoutez des articles au menu
                    </DialogDescription>
                  </DialogHeader>
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {/* Order Details */}
                    <div className="space-y-4">
                      <div className="space-y-2">
                        <Label>Table</Label>
                        <Select value={newOrder.table_id} onValueChange={(value) => setNewOrder(prev => ({...prev, table_id: value}))}>
                          <SelectTrigger>
                            <SelectValue placeholder="Sélectionner une table" />
                          </SelectTrigger>
                          <SelectContent>
                            {tables.map((table: any) => (
                              <SelectItem key={table.id} value={table.id.toString()}>
                                Table {table.number} ({table.capacity} places) - {table.location}
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                      </div>
                      
                      <div className="space-y-2">
                        <Label>Priorité</Label>
                        <Select value={newOrder.priority} onValueChange={(value: any) => setNewOrder(prev => ({...prev, priority: value}))}>
                          <SelectTrigger>
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="normal">Normal</SelectItem>
                            <SelectItem value="high">Prioritaire</SelectItem>
                            <SelectItem value="urgent">Urgent</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>

                      <div className="space-y-2">
                        <Label>Notes (optionnel)</Label>
                        <Textarea
                          placeholder="Instructions spéciales..."
                          value={newOrder.notes}
                          onChange={(e) => setNewOrder(prev => ({...prev, notes: e.target.value}))}
                        />
                      </div>

                      {/* Order Items */}
                      <div className="space-y-2">
                        <Label>Articles commandés ({newOrder.items.length})</Label>
                        <div className="border rounded-lg p-4 max-h-48 overflow-y-auto">
                          {newOrder.items.length === 0 ? (
                            <p className="text-muted-foreground text-center py-4">Aucun article ajouté</p>
                          ) : (
                            <div className="space-y-2">
                              {newOrder.items.map((item) => {
                                const menuItem = menuItems.find((mi: any) => mi.id === item.menu_item_id);
                                return (
                                  <div key={item.menu_item_id} className="flex items-center justify-between p-2 bg-muted rounded">
                                    <div>
                                      <span className="font-medium">{menuItem?.name}</span>
                                      <span className="text-sm text-muted-foreground ml-2">
                                        {menuItem?.price?.toLocaleString()} FBu
                                      </span>
                                    </div>
                                    <div className="flex items-center gap-2">
                                      <Button
                                        size="sm"
                                        variant="outline"
                                        onClick={() => updateItemQuantity(item.menu_item_id, item.quantity - 1)}
                                      >
                                        <Minus className="h-3 w-3" />
                                      </Button>
                                      <span className="w-8 text-center">{item.quantity}</span>
                                      <Button
                                        size="sm"
                                        variant="outline"
                                        onClick={() => updateItemQuantity(item.menu_item_id, item.quantity + 1)}
                                      >
                                        <Plus className="h-3 w-3" />
                                      </Button>
                                      <Button
                                        size="sm"
                                        variant="destructive"
                                        onClick={() => removeItemFromOrder(item.menu_item_id)}
                                      >
                                        <X className="h-3 w-3" />
                                      </Button>
                                    </div>
                                  </div>
                                );
                              })}
                            </div>
                          )}
                        </div>
                      </div>
                    </div>

                    {/* Menu Items */}
                    <div className="space-y-4">
                      <Label>Menu - Cliquez pour ajouter</Label>
                      <div className="border rounded-lg p-4 max-h-96 overflow-y-auto">
                        <div className="grid gap-2">
                          {menuItems.map((item: any) => (
                            <div
                              key={item.id}
                              className="flex items-center justify-between p-3 border rounded-lg hover:bg-muted cursor-pointer transition-colors"
                              onClick={() => addItemToOrder(item.id)}
                            >
                              <div>
                                <h4 className="font-medium">{item.name}</h4>
                                <p className="text-sm text-muted-foreground">{item.description}</p>
                                <p className="text-sm font-semibold text-primary">
                                  {item.price?.toLocaleString()} FBu
                                </p>
                              </div>
                              <Plus className="h-4 w-4 text-muted-foreground" />
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="flex justify-end gap-2 pt-4">
                    <Button variant="outline" onClick={() => setShowNewOrderDialog(false)}>
                      Annuler
                    </Button>
                    <Button 
                      onClick={createNewOrderHandler}
                      disabled={createOrderMutation.isPending}
                    >
                      {createOrderMutation.isPending ? "Création..." : "Créer la commande"}
                    </Button>
                  </div>
                </DialogContent>
              </Dialog>
            </div>
          </div>

          {/* Information table pré-sélectionnée */}
          {preSelectedTable && preSelectedTableNumber && preSelectedServer && (
            <Card className="border-blue-200 bg-blue-50">
              <CardContent className="pt-6">
                <div className="flex items-center gap-4">
                  <div className="h-12 w-12 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center">
                    <Users className="h-6 w-6 text-white" />
                  </div>
                  <div className="flex-1">
                    <h3 className="font-semibold text-blue-900">Table pré-sélectionnée</h3>
                    <p className="text-blue-700">
                      Table {preSelectedTableNumber} ({preSelectedCapacity} places) • Zone {preSelectedLocation}
                    </p>
                    <p className="text-sm text-blue-600">
                      Serveur: {preSelectedServer}
                    </p>
                  </div>
                  <Button
                    variant="outline"
                    size="sm"
                    className="border-blue-300 text-blue-700 hover:bg-blue-100"
                    onClick={() => createNewOrder()}
                  >
                    <Package className="h-4 w-4 mr-2" />
                    Créer commande
                  </Button>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Search and Filters */}
          <Card>
            <CardContent className="pt-6">
              <div className="flex flex-col md:flex-row gap-4">
                <div className="flex-1">
                  <div className="relative">
                    <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                    <Input
                      placeholder="Rechercher par numéro, serveur, table..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="pl-10"
                    />
                  </div>
                </div>
                <div className="flex gap-2">
                  <Select value={selectedTable} onValueChange={setSelectedTable}>
                    <SelectTrigger className="w-48">
                      <SelectValue placeholder="Toutes les tables" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">Toutes les tables</SelectItem>
                      {tables.map((table: any) => (
                        <SelectItem key={table.id} value={table.id.toString()}>
                          Table {table.number}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  <Button variant="outline" onClick={() => refetch()}>
                    <RefreshCw className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Stats Overview */}
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-4">
                  <div className="h-12 w-12 bg-gradient-to-br from-warning to-warning/80 rounded-lg flex items-center justify-center">
                    <Clock className="h-6 w-6 text-warning-foreground" />
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">En attente</p>
                    <p className="text-2xl font-bold text-warning">{getOrdersByStatus("pending").length}</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-4">
                  <div className="h-12 w-12 bg-gradient-to-br from-secondary to-secondary/80 rounded-lg flex items-center justify-center">
                    <ChefHat className="h-6 w-6 text-secondary-foreground" />
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Préparation</p>
                    <p className="text-2xl font-bold text-secondary">{getOrdersByStatus("preparing").length}</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-4">
                  <div className="h-12 w-12 bg-gradient-to-br from-success to-success/80 rounded-lg flex items-center justify-center">
                    <Bell className="h-6 w-6 text-success-foreground" />
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Prêtes</p>
                    <p className="text-2xl font-bold text-success">{getOrdersByStatus("ready").length}</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-4">
                  <div className="h-12 w-12 bg-gradient-to-br from-primary to-primary-glow rounded-lg flex items-center justify-center">
                    <CheckCircle className="h-6 w-6 text-primary-foreground" />
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Servies</p>
                    <p className="text-2xl font-bold">{getOrdersByStatus("served").length}</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-4">
                  <div className="h-12 w-12 bg-gradient-to-br from-muted to-muted/80 rounded-lg flex items-center justify-center">
                    <Timer className="h-6 w-6 text-muted-foreground" />
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Temps moyen</p>
                    <p className="text-2xl font-bold">{getAveragePreparationTime()} min</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          <Tabs defaultValue="active" className="space-y-6">
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="active">Commandes actives</TabsTrigger>
              <TabsTrigger value="kitchen">Interface cuisine</TabsTrigger>
              <TabsTrigger value="served">Servies</TabsTrigger>
              <TabsTrigger value="analytics">Analyses</TabsTrigger>
            </TabsList>

            {/* Active Orders */}
            <TabsContent value="active">
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Pending Orders */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Clock className="h-5 w-5 text-warning" />
                      En attente ({getOrdersByStatus("pending").length})
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    {getOrdersByStatus("pending").map(order => {
                      const statusInfo = getStatusInfo(order.status);
                      const priorityInfo = getPriorityInfo(order.priority);
                      const elapsed = getElapsedTime(order.created_at);
                      
                      return (
                        <Card key={order.id} className="border-warning/20">
                          <CardContent className="p-4">
                            <div className="flex items-center justify-between mb-2">
                              <div className="flex items-center gap-2">
                                <Badge variant="outline">Table {order.table.number}</Badge>
                                <Badge variant={priorityInfo.variant}>{priorityInfo.label}</Badge>
                              </div>
                              <span className="text-sm text-muted-foreground">{new Date(order.created_at).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}</span>
                            </div>
                            
                            <div className="space-y-2 mb-3">
                              {order.items.map(item => (
                                <div key={item.id} className="flex justify-between text-sm">
                                  <span>{item.product.name} x{item.quantity}</span>
                                  {item.notes && <span className="text-muted-foreground italic">{item.notes}</span>}
                                </div>
                              ))}
                            </div>

                            <div className="flex items-center justify-between">
                              <span className="text-sm text-muted-foreground">
                                Attente: {elapsed} min
                              </span>
                              <Button 
                                size="sm"
                                onClick={() => handleUpdateOrderStatus(order.id, "start_preparing")}
                                className="gap-1"
                              >
                                <Play className="h-3 w-3" />
                                Démarrer
                              </Button>
                            </div>
                          </CardContent>
                        </Card>
                      );
                    })}
                  </CardContent>
                </Card>

                {/* Preparing Orders */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <ChefHat className="h-5 w-5 text-secondary" />
                      En préparation ({getOrdersByStatus("preparing").length})
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    {getOrdersByStatus("preparing").map(order => {
                      const elapsed = getElapsedTime(order.created_at);
                      const progress = order.estimated_time ? (elapsed / order.estimated_time) * 100 : 0;
                      
                      return (
                        <Card key={order.id} className="border-secondary/20">
                          <CardContent className="p-4">
                            <div className="flex items-center justify-between mb-2">
                              <div className="flex items-center gap-2">
                                <Badge variant="outline">Table {order.table.number}</Badge>
                                <Badge variant="secondary">En cours</Badge>
                              </div>
                              <span className="text-sm text-muted-foreground">{new Date(order.created_at).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}</span>
                            </div>
                            
                            <div className="space-y-2 mb-3">
                              {order.items.map(item => (
                                <div key={item.id} className="flex justify-between text-sm">
                                  <span>{item.product.name} x{item.quantity}</span>
                                  {item.notes && <span className="text-muted-foreground italic">{item.notes}</span>}
                                </div>
                              ))}
                            </div>

                            <div className="space-y-2">
                              <div className="flex justify-between text-sm">
                                <span>Progression:</span>
                                <span>{elapsed}/{order.estimated_time || 0} min</span>
                              </div>
                              <Progress value={progress} className="h-2" />
                              <Button 
                                size="sm"
                                onClick={() => handleUpdateOrderStatus(order.id, "mark_ready")}
                                className="w-full gap-1"
                              >
                                <Check className="h-3 w-3" />
                                Marquer prête
                              </Button>
                            </div>
                          </CardContent>
                        </Card>
                      );
                    })}
                  </CardContent>
                </Card>

                {/* Ready Orders */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Bell className="h-5 w-5 text-success" />
                      Prêtes à servir ({getOrdersByStatus("ready").length})
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    {getOrdersByStatus("ready").map(order => {
                      const elapsed = getElapsedTime(order.created_at);
                      
                      return (
                        <Card key={order.id} className="border-success/20">
                          <CardContent className="p-4">
                            <div className="flex items-center justify-between mb-2">
                              <div className="flex items-center gap-2">
                                <Badge variant="outline">Table {order.table.number}</Badge>
                                <Badge variant="success">Prête</Badge>
                              </div>
                              <span className="text-sm text-muted-foreground">{new Date(order.created_at).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}</span>
                            </div>
                            
                            <div className="text-sm text-muted-foreground mb-3">
                              <p>Serveur: {order.server.first_name} {order.server.last_name}</p>
                              {order.items.map(item => (
                                <div key={item.id} className="flex justify-between text-sm">
                                  <span>{item.product.name} x{item.quantity}</span>
                                </div>
                              ))}
                            </div>

                            <div className="flex items-center justify-between">
                              <span className="text-sm text-muted-foreground">
                                Prête depuis: {elapsed - (order.estimated_time || 0)} min
                              </span>
                              <div className="flex gap-2">
                                <Button
                                  size="sm"
                                  variant="outline"
                                  onClick={() => handleUpdateOrderStatus(order.id, "serve")}
                                  className="gap-1"
                                >
                                  <CheckCircle className="h-3 w-3" />
                                  Servie
                                </Button>
                                <Button
                                  size="sm"
                                  onClick={() => processOrderPayment(order)}
                                  className="gap-1 bg-green-600 hover:bg-green-700"
                                >
                                  <Package className="h-3 w-3" />
                                  Encaisser
                                </Button>
                              </div>
                            </div>
                          </CardContent>
                        </Card>
                      );
                    })}
                  </CardContent>
                </Card>
              </div>
            </TabsContent>

            {/* Kitchen Interface */}
            <TabsContent value="kitchen">
              <Card>
                <CardHeader>
                  <CardTitle>Interface cuisine - Vue d'ensemble</CardTitle>
                  <CardDescription>
                    Vue optimisée pour la cuisine avec toutes les commandes en cours
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {kitchenOrders.map(order => {
                      const elapsed = getElapsedTime(order.created_at);
                      const progress = order.estimated_time ? (elapsed / order.estimated_time) * 100 : 0;
                      
                      return (
                        <Card key={order.id} className="p-4">
                          <div className="flex items-center justify-between mb-4">
                            <Badge variant="outline">Table {order.table.number}</Badge>
                            <Badge variant={getPriorityInfo(order.priority).variant}>
                              {getPriorityInfo(order.priority).label}
                            </Badge>
                          </div>
                          
                          <div className="text-sm text-muted-foreground mb-4">
                            <p>Commande: {new Date(order.created_at).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}</p>
                            <p>Temps estimé: {order.estimated_time || 0} min</p>
                          </div>

                          <div className="space-y-2 mb-4">
                            {order.items.map(item => (
                              <div key={item.id} className="bg-muted p-2 rounded">
                                <div className="flex justify-between">
                                  <span className="text-primary font-bold">x{item.quantity}</span>
                                  <span className="text-sm text-muted-foreground">{item.product.name}</span>
                                </div>
                                {item.notes && (
                                  <p className="text-xs text-muted-foreground mt-1">📝 {item.notes}</p>
                                )}
                              </div>
                            ))}
                          </div>

                          <div className="flex gap-2">
                            {(order.status === "pending" || order.status === "confirmed") && (
                              <Button 
                                size="sm" 
                                onClick={() => handleUpdateOrderStatus(order.id, "start_preparing")}
                                disabled={updateOrderMutation.isPending}
                                className="flex-1"
                              >
                                <Play className="h-4 w-4 mr-1" />
                                Commencer
                              </Button>
                            )}
                            
                            {order.status === "preparing" && (
                              <Button 
                                size="sm" 
                                onClick={() => handleUpdateOrderStatus(order.id, "mark_ready")}
                                disabled={updateOrderMutation.isPending}
                                className="flex-1"
                              >
                                <Check className="h-4 w-4 mr-1" />
                                Terminer
                              </Button>
                            )}
                            
                            {order.status === "ready" && (
                              <Button 
                                size="sm" 
                                onClick={() => handleUpdateOrderStatus(order.id, "serve")}
                                disabled={updateOrderMutation.isPending}
                                className="flex-1"
                              >
                                <CheckCircle className="h-4 w-4 mr-1" />
                                Servir
                              </Button>
                            )}
                            
                            {order.status !== "served" && order.status !== "cancelled" && (
                              <Button 
                                size="sm" 
                                variant="outline"
                                onClick={() => handleUpdateOrderStatus(order.id, "cancel")}
                                disabled={updateOrderMutation.isPending}
                                className="text-destructive hover:text-destructive"
                              >
                                Annuler
                              </Button>
                            )}
                          </div>
                        </Card>
                      );
                    })}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Served Orders */}
            <TabsContent value="served">
              <Card>
                <CardHeader>
                  <CardTitle>Commandes servies aujourd'hui</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {getOrdersByStatus("served").map(order => (
                      <div key={order.id} className="flex items-center justify-between p-4 border rounded-lg">
                        <div>
                          <div className="flex items-center gap-2 mb-1">
                            <Badge variant="outline">Table {order.table.number}</Badge>
                            <Badge variant="default">Servie</Badge>
                          </div>
                          <div className="text-sm text-muted-foreground mb-3">
                            <p>Serveur: {order.server.first_name} {order.server.last_name}</p>
                            <p>Commande: {new Date(order.created_at).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}</p>
                          </div>
                          <div className="flex items-center justify-between mb-3">
                            <span className="font-semibold">
                              {order.total_amount.toLocaleString()} FBu
                            </span>
                            <span className="text-sm text-muted-foreground">
                              {getElapsedTime(order.created_at)} min
                            </span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Analytics */}
            <TabsContent value="analytics">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Performance du service</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="flex justify-between items-center">
                        <span>Temps moyen de préparation</span>
                        <span className="font-bold">{getAveragePreparationTime()} min</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span>Commandes en retard</span>
                        <span className="font-bold text-destructive">
                          {orders.filter(order => order.estimated_time && getElapsedTime(order.created_at) > order.estimated_time).length}
                        </span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span>Taux de satisfaction</span>
                        <span className="font-bold text-success">94%</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle>Répartition par serveur</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {servers.map(server => {
                        const serverOrders = orders.filter(order => `${order.server.first_name} ${order.server.last_name}` === server);
                        return (
                          <div key={server} className="flex justify-between items-center p-2 bg-muted rounded">
                            <span className="font-medium">{server}</span>
                            <span className="text-sm">{serverOrders.length} commandes</span>
                          </div>
                        );
                      })}
                    </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>
          </Tabs>
        </main>
      </div>
    </div>
  );
}
