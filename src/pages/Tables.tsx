import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Sidebar } from "@/components/layout/Sidebar";
import { Header } from "@/components/layout/Header";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useToast } from "@/hooks/use-toast";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Users,
  Clock,
  User,
  Calendar,
  MapPin,
  Settings,
  Eye,
  Edit,
  CheckCircle,
  AlertTriangle,
  ShoppingCart,
  Plus,
  Loader2
} from "lucide-react";
import { useTables, useOrders, useCreateOrder, useUpdateTableStatus } from "@/hooks/use-api";
import { Table as TableType } from "@/types/api";

// Interface locale pour l'état des tables avec données supplémentaires
interface LocalTableData {
  currentOrder?: {
    items: number;
    total: number;
  };
  occupiedSince?: string;
  reservationTime?: string;
}

// Interface étendue pour les données mock avec propriétés supplémentaires
interface ExtendedTable extends TableType {
  seats?: number;
  zone?: string;
  customer?: string;
  server?: string;
  occupiedSince?: string;
  reservationTime?: string;
}

// Données mock supprimées - utilisation de l'API
const mockTables: any[] = [
  {
    id: "1",
    number: 1,
    seats: 4,
    status: "occupied",
    server: "Marie Uwimana",
    customer: "Famille Nkurunziza",
    occupiedSince: "14:30",
    zone: "intérieur",
    currentOrder: { items: 5, total: 12500 }
  },
  {
    id: "2",
    number: 2,
    seats: 2,
    status: "available",
    zone: "intérieur"
  },
  {
    id: "3",
    number: 3,
    seats: 6,
    status: "reserved",
    reservationTime: "18:00",
    customer: "M. Ndayisenga",
    zone: "terrasse"
  },
  {
    id: "4",
    number: 4,
    seats: 4,
    status: "cleaning",
    zone: "intérieur"
  },
  {
    id: "5",
    number: 5,
    seats: 8,
    status: "occupied",
    server: "Jean Nkurunziza",
    customer: "Groupe d'affaires",
    occupiedSince: "13:15",
    zone: "vip",
    currentOrder: { items: 12, total: 85000 }
  }
];

const servers = ["Marie Uwimana", "Jean Nkurunziza", "Paul Ndayisenga"];

export default function Tables() {
  const navigate = useNavigate();
  const { toast } = useToast();
  
  // API Hooks
  const { data: tablesData, isLoading: tablesLoading, error: tablesError } = useTables();
  const { data: ordersData, isLoading: ordersLoading } = useOrders();
  const updateTableStatus = useUpdateTableStatus();
  
  // Local state
  const [selectedTable, setSelectedTable] = useState<TableType | null>(null);
  const [isOrderDialogOpen, setIsOrderDialogOpen] = useState(false);
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [filterStatus, setFilterStatus] = useState<string>("all");
  const [filterZone, setFilterZone] = useState<string>("all");
  const [localTableData, setLocalTableData] = useState<Record<number, LocalTableData>>({});
  const [showReservationDialog, setShowReservationDialog] = useState(false);
  
  // Récupérer les tables depuis l'API
  const tables = tablesData?.results || [];
  
  const [reservationData, setReservationData] = useState({
    tableId: "",
    customerName: "",
    time: "",
    date: "",
    seats: ""
  });

  // Gestion des erreurs API
  useEffect(() => {
    if (tablesError) {
      toast({
        title: "Erreur",
        description: "Impossible de charger les tables depuis l'API.",
        variant: "destructive",
      });
    }
  }, [tablesError, toast]);

  // Associer les commandes aux tables
  const getTableWithOrders = (table: TableType) => {
    const tableOrders = ordersData?.results?.filter(order => order.table.id === table.id) || [];
    const currentOrder = tableOrders.find(order => ['pending', 'confirmed', 'preparing'].includes(order.status));
    
    return {
      ...table,
      currentOrder: currentOrder ? {
        items: currentOrder.items.length,
        total: currentOrder.total_amount
      } : undefined,
      hasActiveOrder: !!currentOrder
    };
  };



  const getStatusInfo = (status: TableType["status"] | "cleaning") => {
    switch (status) {
      case "available":
        return { variant: "success" as const, label: "Libre", color: "bg-success" };
      case "occupied":
        return { variant: "destructive" as const, label: "Occupée", color: "bg-destructive" };
      case "reserved":
        return { variant: "warning" as const, label: "Réservée", color: "bg-warning" };
      case "maintenance":
        return { variant: "secondary" as const, label: "Maintenance", color: "bg-secondary" };
      case "cleaning":
        return { variant: "secondary" as const, label: "Nettoyage", color: "bg-secondary" };
      default:
        return { variant: "secondary" as const, label: "Inconnu", color: "bg-secondary" };
    }
  };

  const getZoneLabel = (zone: string) => {
    switch (zone) {
      case "terrasse": return "Terrasse";
      case "intérieur": return "Intérieur";
      case "vip": return "VIP";
      default: return zone;
    }
  };

  const handleUpdateTableStatus = async (tableId: number, newStatus: TableType["status"]) => {
    try {
      await updateTableStatus.mutateAsync({ tableId, status: newStatus });
      
      // Mettre à jour les données locales
      setLocalTableData(prev => ({
        ...prev,
        [tableId]: {
          ...prev[tableId],
          occupiedSince: newStatus === "occupied" ? new Date().toLocaleTimeString() : undefined
        }
      }));
    } catch (error) {
      toast({
        title: "Erreur",
        description: "Impossible de mettre à jour le statut de la table",
        variant: "destructive",
      });
    }
  };

  // Fonction pour assigner un serveur à une table
  const assignServer = async (tableId: number, serverName: string) => {
    // TODO: Implémenter l'API pour assigner un serveur
    console.log(`Assigning server ${serverName} to table ${tableId}`);
    toast({
      title: "Serveur assigné",
      description: `${serverName} a été assigné à la table ${tableId}`,
      variant: "default",
    });
  };

  const createOrderForTable = (table: TableType) => {
    // Vérifications
    if (table.status !== "occupied") {
      toast({
        title: "Table non occupée",
        description: "Veuillez d'abord marquer la table comme occupée",
        variant: "destructive",
      });
      return;
    }

    // Navigation vers Orders avec paramètres
    const params = new URLSearchParams({
      table: table.id.toString(),
      tableNumber: table.number.toString(),
      capacity: table.capacity.toString(),
      location: table.location || ""
    });

    navigate(`/orders?${params.toString()}`);

    toast({
      title: "Redirection vers commandes",
      description: `Création d'une commande pour la table ${table.number}`,
      variant: "default",
    });
  };

  const makeReservation = () => {
    // TODO: Implement reservation logic
    console.log("Making reservation:", reservationData);
    setShowReservationDialog(false);
    setReservationData({
      tableId: "",
      customerName: "",
      time: "",
      date: "",
      seats: ""
    });
  };

  const getOccupancyStats = () => {
    const occupied = tables.filter(t => t.status === "occupied").length;
    const reserved = tables.filter(t => t.status === "reserved").length;
    const available = tables.filter(t => t.status === "available").length;
    const total = tables.length;
    
    return { occupied, reserved, available, total, rate: Math.round((occupied / total) * 100) };
  };

  const stats = getOccupancyStats();

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
                Gestion des tables
              </h1>
              <p className="text-muted-foreground">
                Plan de salle interactif et gestion des réservations
              </p>
            </div>
            <Dialog open={showReservationDialog} onOpenChange={setShowReservationDialog}>
              <DialogTrigger asChild>
                <Button className="gap-2">
                  <Calendar className="h-4 w-4" />
                  Nouvelle réservation
                </Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Nouvelle réservation</DialogTitle>
                  <DialogDescription>
                    Réserver une table pour un client
                  </DialogDescription>
                </DialogHeader>
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label>Table</Label>
                    <Select value={reservationData.tableId} onValueChange={(value) => setReservationData(prev => ({...prev, tableId: value}))}>
                      <SelectTrigger>
                        <SelectValue placeholder="Sélectionner une table" />
                      </SelectTrigger>
                      <SelectContent>
                        {tables.filter(t => t.status === "available").map(table => (
                          <SelectItem key={table.id} value={table.id.toString()}>
                            Table {table.number} ({table.capacity} places) - {getZoneLabel(table.location || "intérieur")}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label>Nom du client</Label>
                    <Input
                      placeholder="Nom du client"
                      value={reservationData.customerName}
                      onChange={(e) => setReservationData(prev => ({...prev, customerName: e.target.value}))}
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-2">
                    <div className="space-y-2">
                      <Label>Date</Label>
                      <Input
                        type="date"
                        value={reservationData.date}
                        onChange={(e) => setReservationData(prev => ({...prev, date: e.target.value}))}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label>Heure</Label>
                      <Input
                        type="time"
                        value={reservationData.time}
                        onChange={(e) => setReservationData(prev => ({...prev, time: e.target.value}))}
                      />
                    </div>
                  </div>
                  <Button onClick={makeReservation} className="w-full">
                    Confirmer la réservation
                  </Button>
                </div>
              </DialogContent>
            </Dialog>
          </div>

          {/* Occupancy Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-4">
                  <div className="h-12 w-12 bg-gradient-to-br from-success to-success/80 rounded-lg flex items-center justify-center">
                    <CheckCircle className="h-6 w-6 text-success-foreground" />
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Tables libres</p>
                    <p className="text-2xl font-bold text-success">{stats.available}</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-4">
                  <div className="h-12 w-12 bg-gradient-to-br from-destructive to-destructive/80 rounded-lg flex items-center justify-center">
                    <Users className="h-6 w-6 text-destructive-foreground" />
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Occupées</p>
                    <p className="text-2xl font-bold text-destructive">{stats.occupied}</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-4">
                  <div className="h-12 w-12 bg-gradient-to-br from-warning to-warning/80 rounded-lg flex items-center justify-center">
                    <Calendar className="h-6 w-6 text-warning-foreground" />
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Réservées</p>
                    <p className="text-2xl font-bold text-warning">{stats.reserved}</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-4">
                  <div className="h-12 w-12 bg-gradient-to-br from-primary to-primary-glow rounded-lg flex items-center justify-center">
                    <Users className="h-6 w-6 text-primary-foreground" />
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Taux d'occupation</p>
                    <p className="text-2xl font-bold">{stats.rate}%</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Indicateur de chargement */}
          {tablesLoading && (
            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center justify-center py-12">
                  <div className="flex items-center gap-3">
                    <Clock className="h-6 w-6 animate-spin text-primary" />
                    <span className="text-lg">Chargement des tables...</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Floor Plan */}
          {tablesLoading ? (
            <Card>
              <CardHeader>
                <CardTitle>Chargement des tables...</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
                  {[...Array(8)].map((_, i) => (
                    <Skeleton key={i} className="h-24 w-full" />
                  ))}
                </div>
              </CardContent>
            </Card>
          ) : (
          <Card>
            <CardHeader>
              <CardTitle>Plan de salle</CardTitle>
              <CardDescription>
                Cliquez sur une table pour voir les détails ou modifier son statut
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                {/* Statistiques en temps réel */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 p-4 bg-muted/30 rounded-lg">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600">
                      {tables.filter(t => t.status === 'available').length}
                    </div>
                    <div className="text-xs text-muted-foreground">Disponibles</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-red-600">
                      {tables.filter(t => t.status === 'occupied').length}
                    </div>
                    <div className="text-xs text-muted-foreground">Occupées</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-yellow-600">
                      {tables.filter(t => t.status === 'reserved').length}
                    </div>
                    <div className="text-xs text-muted-foreground">Réservées</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-orange-600">
                      {tables.filter(t => t.status === 'maintenance').length}
                    </div>
                    <div className="text-xs text-muted-foreground">Maintenance</div>
                  </div>
              </div>

              {/* Zone Intérieur */}
              <div>
                <h3 className="font-semibold mb-3 flex items-center gap-2">
                  <MapPin className="h-4 w-4" />
                  Zone Intérieur
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
                  {tables.filter(t => t.location === "intérieur" || !t.location).map(table => {
                    const tableWithOrders = getTableWithOrders(table);
                    const statusInfo = getStatusInfo(table.status);
                    return (
                      <Dialog key={table.id}>
                        <DialogTrigger asChild>
                          <Card className={`cursor-pointer hover:shadow-md transition-all ${statusInfo.color}/10 border-2 border-${statusInfo.color.replace('bg-', '')}/20`}>
                            <CardContent className="p-4 text-center">
                              <div className={`h-8 w-8 ${statusInfo.color} rounded-full flex items-center justify-center mx-auto mb-2`}>
                                <span className="text-white font-bold text-sm">{table.number}</span>
                              </div>
                              <Badge variant={statusInfo.variant} className="text-xs mb-1">
                                {statusInfo.label}
                              </Badge>
                              <p className="text-xs text-muted-foreground">{table.capacity} places</p>
                              {tableWithOrders.currentOrder && (
                                <p className="text-xs font-medium mt-1 text-blue-600">
                                  {tableWithOrders.currentOrder.items} articles - {tableWithOrders.currentOrder.total} BIF
                                </p>
                              )}
                            </CardContent>
                          </Card>
                          </DialogTrigger>
                          <DialogContent>
                            <DialogHeader>
                              <DialogTitle>Table {table.number}</DialogTitle>
                              <DialogDescription>
                                Gestion de la table {table.number} ({table.capacity} places)
                              </DialogDescription>
                            </DialogHeader>
                            <div className="space-y-4">
                              <div className="grid grid-cols-2 gap-4">
                                <div>
                                  <p className="text-sm text-muted-foreground">Statut actuel</p>
                                  <Badge variant={statusInfo.variant}>{statusInfo.label}</Badge>
                                </div>
                                <div>
                                  <p className="text-sm text-muted-foreground">Zone</p>
                                  <p className="font-medium">{table.location || "Intérieur"}</p>
                                </div>
                              </div>

                              {tableWithOrders.currentOrder && (
                                <div className="space-y-2">
                                  <div>
                                    <p className="text-sm text-muted-foreground">Commande en cours</p>
                                    <p className="font-medium">
                                      {tableWithOrders.currentOrder.items} articles - {tableWithOrders.currentOrder.total.toLocaleString()} BIF
                                    </p>
                                  </div>
                                </div>
                              )}

                              <div className="flex gap-2 pt-4">
                                <Button 
                                  size="sm" 
                                  variant="outline"
                                  onClick={() => handleUpdateTableStatus(table.id, table.status === "available" ? "occupied" : "available")}
                                  disabled={updateTableStatus.isPending}
                                >
                                  {updateTableStatus.isPending ? (
                                    <Loader2 className="h-4 w-4 animate-spin" />
                                  ) : (
                                    table.status === "available" ? "Occuper" : "Libérer"
                                  )}
                                </Button>
                                {table.status === "occupied" && (
                                  <Button 
                                    size="sm" 
                                    onClick={() => createOrderForTable(table)}
                                    className="gap-2"
                                  >
                                    <ShoppingCart className="h-4 w-4" />
                                    Nouvelle commande
                                  </Button>
                                )}
                              </div>
                            </div>
                          </DialogContent>
                        </Dialog>
                      );
                    })}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
          )}
        </main>
      </div>
    </div>
  );
}
