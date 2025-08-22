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
  Plus
} from "lucide-react";
import { useTables, useOrders, useCreateOrder } from "@/hooks/use-api";

interface Table {
  id: string;
  number: number;
  seats: number;
  status: "available" | "occupied" | "reserved" | "cleaning";
  server?: string;
  customer?: string;
  occupiedSince?: string;
  reservationTime?: string;
  zone: "terrasse" | "intérieur" | "vip";
  currentOrder?: {
    items: number;
    total: number;
  };
}

const mockTables: Table[] = [
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
  const [selectedTable, setSelectedTable] = useState<Table | null>(null);
  const [showReservationDialog, setShowReservationDialog] = useState(false);
  const [tables, setTables] = useState<Table[]>([]);
  const [loading, setLoading] = useState(true);
  const { toast } = useToast();
  const [reservationData, setReservationData] = useState({
    tableId: "",
    customerName: "",
    time: "",
    date: "",
    seats: ""
  });

  // Charger les vraies données des tables
  useEffect(() => {
    fetchTables();
  }, []);

  const fetchTables = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://127.0.0.1:8000/api/sales/tables/');

      if (response.ok) {
        const data = await response.json();
        setTables(data.results || []);
        toast({
          title: "Tables chargées",
          description: `${data.results?.length || 0} tables récupérées`,
          variant: "default",
        });
      } else {
        throw new Error('Erreur API');
      }
    } catch (error) {
      toast({
        title: "Erreur",
        description: "Impossible de charger les tables. Utilisation des données de démonstration.",
        variant: "destructive",
      });
      // Fallback vers les données mockées
      setTables(mockTables);
    } finally {
      setLoading(false);
    }
  };



  const getStatusInfo = (status: Table["status"]) => {
    switch (status) {
      case "available":
        return { variant: "success" as const, label: "Libre", color: "bg-success" };
      case "occupied":
        return { variant: "destructive" as const, label: "Occupée", color: "bg-destructive" };
      case "reserved":
        return { variant: "warning" as const, label: "Réservée", color: "bg-warning" };
      case "cleaning":
        return { variant: "secondary" as const, label: "Nettoyage", color: "bg-secondary" };
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

  const updateTableStatus = (tableId: string, newStatus: Table["status"]) => {
    setTables(prev => prev.map(table => 
      table.id === tableId 
        ? { ...table, status: newStatus, occupiedSince: newStatus === "occupied" ? new Date().toLocaleTimeString() : undefined }
        : table
    ));
  };

  const assignServer = (tableId: string, serverName: string) => {
    setTables(prev => prev.map(table =>
      table.id === tableId ? { ...table, server: serverName } : table
    ));
  };

  const createOrderForTable = (table: Table) => {
    // Vérifications
    if (table.status !== "occupied") {
      toast({
        title: "Table non occupée",
        description: "Veuillez d'abord marquer la table comme occupée",
        variant: "destructive",
      });
      return;
    }

    if (!table.server) {
      toast({
        title: "Serveur non assigné",
        description: "Veuillez d'abord assigner un serveur à cette table",
        variant: "destructive",
      });
      return;
    }

    // Navigation vers Orders avec paramètres
    const params = new URLSearchParams({
      table: table.id,
      tableNumber: table.number,
      server: table.server,
      capacity: table.capacity.toString(),
      location: table.location
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
                          <SelectItem key={table.id} value={table.id}>
                            Table {table.number} ({table.seats} places) - {getZoneLabel(table.zone)}
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
          {loading && (
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
          {!loading && (
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
                      {tables.filter(t => t.status === 'cleaning').length}
                    </div>
                    <div className="text-xs text-muted-foreground">Nettoyage</div>
                  </div>
                </div>

                {/* Zone Intérieur */}
                <div>
                  <h3 className="font-semibold mb-3 flex items-center gap-2">
                    <MapPin className="h-4 w-4" />
                    Zone Intérieur
                  </h3>
                  <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
                    {tables.filter(t => t.location === "intérieur").map(table => {
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
                                {table.server && (
                                  <p className="text-xs font-medium mt-1">{table.server}</p>
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
                                  <p className="font-medium">{getZoneLabel(table.zone)}</p>
                                </div>
                              </div>

                              {table.status === "occupied" && (
                                <div className="space-y-2">
                                  <div>
                                    <p className="text-sm text-muted-foreground">Client</p>
                                    <p className="font-medium">{table.customer}</p>
                                  </div>
                                  <div>
                                    <p className="text-sm text-muted-foreground">Serveur</p>
                                    <p className="font-medium">{table.server}</p>
                                  </div>
                                  <div>
                                    <p className="text-sm text-muted-foreground">Occupée depuis</p>
                                    <p className="font-medium">{table.occupiedSince}</p>
                                  </div>
                                  {table.currentOrder && (
                                    <div>
                                      <p className="text-sm text-muted-foreground">Commande en cours</p>
                                      <p className="font-medium">
                                        {table.currentOrder.items} articles - {table.currentOrder.total.toLocaleString()} FBu
                                      </p>
                                    </div>
                                  )}
                                </div>
                              )}

                              {table.status === "reserved" && (
                                <div className="space-y-2">
                                  <div>
                                    <p className="text-sm text-muted-foreground">Réservée pour</p>
                                    <p className="font-medium">{table.customer}</p>
                                  </div>
                                  <div>
                                    <p className="text-sm text-muted-foreground">Heure de réservation</p>
                                    <p className="font-medium">{table.reservationTime}</p>
                                  </div>
                                </div>
                              )}

                              <div className="space-y-2">
                                <Label>Changer le statut</Label>
                                <div className="grid grid-cols-2 gap-2">
                                  <Button
                                    variant="outline"
                                    onClick={() => updateTableStatus(table.id, "available")}
                                    disabled={table.status === "available"}
                                  >
                                    Libérer
                                  </Button>
                                  <Button
                                    variant="outline"
                                    onClick={() => updateTableStatus(table.id, "occupied")}
                                    disabled={table.status === "occupied"}
                                  >
                                    Occuper
                                  </Button>
                                  <Button
                                    variant="outline"
                                    onClick={() => updateTableStatus(table.id, "cleaning")}
                                    disabled={table.status === "cleaning"}
                                  >
                                    Nettoyage
                                  </Button>
                                  <Button
                                    variant="outline"
                                    onClick={() => updateTableStatus(table.id, "reserved")}
                                    disabled={table.status === "reserved"}
                                  >
                                    Réserver
                                  </Button>
                                </div>
                              </div>

                              {table.status === "occupied" && (
                                <div className="space-y-2">
                                  <Label>Assigner un serveur</Label>
                                  <Select value={table.server || ""} onValueChange={(value) => assignServer(table.id, value)}>
                                    <SelectTrigger>
                                      <SelectValue placeholder="Sélectionner un serveur" />
                                    </SelectTrigger>
                                    <SelectContent>
                                      {servers.map(server => (
                                        <SelectItem key={server} value={server}>{server}</SelectItem>
                                      ))}
                                    </SelectContent>
                                  </Select>
                                </div>
                              )}

                              {/* Bouton Nouvelle Commande */}
                              {table.status === "occupied" && table.server && (
                                <div className="pt-4 border-t">
                                  <Button
                                    onClick={() => createOrderForTable(table)}
                                    className="w-full"
                                    size="lg"
                                  >
                                    <ShoppingCart className="h-4 w-4 mr-2" />
                                    Nouvelle commande
                                  </Button>
                                  <p className="text-xs text-muted-foreground text-center mt-2">
                                    Créer une commande pour cette table
                                  </p>
                                </div>
                              )}
                            </div>
                          </DialogContent>
                        </Dialog>
                      );
                    })}
                  </div>
                </div>

                {/* Zone Terrasse */}
                <div>
                  <h3 className="font-semibold mb-3 flex items-center gap-2">
                    <MapPin className="h-4 w-4" />
                    Zone Terrasse
                  </h3>
                  <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
                    {tables.filter(t => t.location === "terrasse").map(table => {
                      const statusInfo = getStatusInfo(table.status);
                      return (
                        <Dialog key={table.id}>
                          <DialogTrigger asChild>
                            <Card className={`cursor-pointer hover:shadow-md transition-all ${statusInfo.color}/10`}>
                              <CardContent className="p-4 text-center">
                                <div className={`h-8 w-8 ${statusInfo.color} rounded-full flex items-center justify-center mx-auto mb-2`}>
                                  <span className="text-white font-bold text-sm">{table.number}</span>
                                </div>
                                <Badge variant={statusInfo.variant} className="text-xs mb-1">
                                  {statusInfo.label}
                                </Badge>
                                <p className="text-xs text-muted-foreground">{table.seats} places</p>
                              </CardContent>
                            </Card>
                          </DialogTrigger>
                          <DialogContent>
                            <DialogHeader>
                              <DialogTitle>Table {table.number}</DialogTitle>
                              <DialogDescription>
                                Gestion de la table {table.number} ({table.seats} places) - Terrasse
                              </DialogDescription>
                            </DialogHeader>
                            <div className="space-y-4">
                              <div className="grid grid-cols-2 gap-4">
                                <div>
                                  <p className="text-sm text-muted-foreground">Statut</p>
                                  <Badge variant={statusInfo.variant}>{statusInfo.label}</Badge>
                                </div>
                                <div>
                                  <p className="text-sm text-muted-foreground">Zone</p>
                                  <p className="font-medium">Terrasse</p>
                                </div>
                              </div>

                              {table.status === "occupied" && (
                                <div className="space-y-2">
                                  <div>
                                    <p className="text-sm text-muted-foreground">Client</p>
                                    <p className="font-medium">{table.customer}</p>
                                  </div>
                                  <div>
                                    <p className="text-sm text-muted-foreground">Serveur</p>
                                    <p className="font-medium">{table.server}</p>
                                  </div>
                                </div>
                              )}

                              <div className="space-y-2">
                                <Label>Changer le statut</Label>
                                <div className="grid grid-cols-2 gap-2">
                                  <Button
                                    variant="outline"
                                    onClick={() => updateTableStatus(table.id, "available")}
                                    disabled={table.status === "available"}
                                  >
                                    Libérer
                                  </Button>
                                  <Button
                                    variant="outline"
                                    onClick={() => updateTableStatus(table.id, "occupied")}
                                    disabled={table.status === "occupied"}
                                  >
                                    Occuper
                                  </Button>
                                </div>
                              </div>

                              <div className="space-y-2">
                                <Label>Assigner un serveur</Label>
                                <Select onValueChange={(value) => assignServer(table.id, value)}>
                                  <SelectTrigger>
                                    <SelectValue placeholder={table.server || "Sélectionner un serveur"} />
                                  </SelectTrigger>
                                  <SelectContent>
                                    <SelectItem value="Marie Uwimana">Marie Uwimana</SelectItem>
                                    <SelectItem value="Jean Nkurunziza">Jean Nkurunziza</SelectItem>
                                    <SelectItem value="Alice Ndayisenga">Alice Ndayisenga</SelectItem>
                                    <SelectItem value="Paul Hakizimana">Paul Hakizimana</SelectItem>
                                  </SelectContent>
                                </Select>
                              </div>

                              {/* Bouton Nouvelle Commande */}
                              {table.status === "occupied" && table.server && (
                                <div className="pt-4 border-t">
                                  <Button
                                    onClick={() => createOrderForTable(table)}
                                    className="w-full"
                                    size="lg"
                                  >
                                    <ShoppingCart className="h-4 w-4 mr-2" />
                                    Nouvelle commande
                                  </Button>
                                  <p className="text-xs text-muted-foreground text-center mt-2">
                                    Créer une commande pour cette table
                                  </p>
                                </div>
                              )}
                            </div>
                          </DialogContent>
                        </Dialog>
                      );
                    })}
                  </div>
                </div>

                {/* Zone VIP */}
                <div>
                  <h3 className="font-semibold mb-3 flex items-center gap-2">
                    <MapPin className="h-4 w-4" />
                    Zone VIP
                  </h3>
                  <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
                    {tables.filter(t => t.location === "vip").map(table => {
                      const statusInfo = getStatusInfo(table.status);
                      return (
                        <Dialog key={table.id}>
                          <DialogTrigger asChild>
                            <Card className={`cursor-pointer hover:shadow-md transition-all ${statusInfo.color}/10 border-accent/30`}>
                              <CardContent className="p-4 text-center">
                                <div className={`h-8 w-8 ${statusInfo.color} rounded-full flex items-center justify-center mx-auto mb-2`}>
                                  <span className="text-white font-bold text-sm">{table.number}</span>
                                </div>
                                <Badge variant={statusInfo.variant} className="text-xs mb-1">
                                  {statusInfo.label}
                                </Badge>
                                <p className="text-xs text-muted-foreground">{table.seats} places</p>
                                <Badge variant="accent" className="text-xs mt-1">VIP</Badge>
                              </CardContent>
                            </Card>
                          </DialogTrigger>
                          <DialogContent>
                            <DialogHeader>
                              <DialogTitle>Table {table.number} VIP</DialogTitle>
                              <DialogDescription>
                                Gestion de la table VIP {table.number} ({table.seats} places)
                              </DialogDescription>
                            </DialogHeader>
                            <div className="space-y-4">
                              <div className="grid grid-cols-2 gap-4">
                                <div>
                                  <p className="text-sm text-muted-foreground">Statut</p>
                                  <Badge variant={statusInfo.variant}>{statusInfo.label}</Badge>
                                </div>
                                <div>
                                  <p className="text-sm text-muted-foreground">Zone</p>
                                  <Badge variant="accent">VIP</Badge>
                                </div>
                              </div>

                              {table.status === "occupied" && (
                                <div className="space-y-2">
                                  <div>
                                    <p className="text-sm text-muted-foreground">Client</p>
                                    <p className="font-medium">{table.customer}</p>
                                  </div>
                                  <div>
                                    <p className="text-sm text-muted-foreground">Serveur</p>
                                    <p className="font-medium">{table.server}</p>
                                  </div>
                                </div>
                              )}

                              <div className="space-y-2">
                                <Label>Changer le statut</Label>
                                <div className="grid grid-cols-2 gap-2">
                                  <Button
                                    variant="outline"
                                    onClick={() => updateTableStatus(table.id, "available")}
                                    disabled={table.status === "available"}
                                  >
                                    Libérer
                                  </Button>
                                  <Button
                                    variant="outline"
                                    onClick={() => updateTableStatus(table.id, "occupied")}
                                    disabled={table.status === "occupied"}
                                  >
                                    Occuper
                                  </Button>
                                </div>
                              </div>

                              <div className="space-y-2">
                                <Label>Assigner un serveur</Label>
                                <Select onValueChange={(value) => assignServer(table.id, value)}>
                                  <SelectTrigger>
                                    <SelectValue placeholder={table.server || "Sélectionner un serveur"} />
                                  </SelectTrigger>
                                  <SelectContent>
                                    <SelectItem value="Marie Uwimana">Marie Uwimana</SelectItem>
                                    <SelectItem value="Jean Nkurunziza">Jean Nkurunziza</SelectItem>
                                    <SelectItem value="Alice Ndayisenga">Alice Ndayisenga</SelectItem>
                                    <SelectItem value="Paul Hakizimana">Paul Hakizimana</SelectItem>
                                  </SelectContent>
                                </Select>
                              </div>

                              {/* Bouton Nouvelle Commande */}
                              {table.status === "occupied" && table.server && (
                                <div className="pt-4 border-t">
                                  <Button
                                    onClick={() => createOrderForTable(table)}
                                    className="w-full"
                                    size="lg"
                                  >
                                    <ShoppingCart className="h-4 w-4 mr-2" />
                                    Nouvelle commande
                                  </Button>
                                  <p className="text-xs text-muted-foreground text-center mt-2">
                                    Créer une commande pour cette table
                                  </p>
                                </div>
                              )}
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

          {/* Statistics */}
          {!loading && (
          <Card>
            <CardHeader>
              <CardTitle>Statistiques d'occupation</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="text-center p-4 bg-muted rounded-lg">
                  <p className="text-2xl font-bold">{stats.total}</p>
                  <p className="text-sm text-muted-foreground">Total tables</p>
                </div>
                <div className="text-center p-4 bg-success/10 rounded-lg">
                  <p className="text-2xl font-bold text-success">{stats.available}</p>
                  <p className="text-sm text-muted-foreground">Libres</p>
                </div>
                <div className="text-center p-4 bg-destructive/10 rounded-lg">
                  <p className="text-2xl font-bold text-destructive">{stats.occupied}</p>
                  <p className="text-sm text-muted-foreground">Occupées</p>
                </div>
                <div className="text-center p-4 bg-primary/10 rounded-lg">
                  <p className="text-2xl font-bold text-primary">{stats.rate}%</p>
                  <p className="text-sm text-muted-foreground">Taux d'occupation</p>
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
