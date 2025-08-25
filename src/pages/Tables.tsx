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
import {
  Calendar,
  Users,
  Clock,
  MapPin,
  CheckCircle,
  AlertCircle,
  Utensils
} from "lucide-react";
import { useTables, useOccupyTable, useFreeTable, useCreateReservation } from "@/hooks/use-api";
import { useToast } from "@/hooks/use-toast";

export default function Tables() {
  const [showReservationDialog, setShowReservationDialog] = useState(false);
  const [reservationData, setReservationData] = useState({
    tableId: "",
    customerName: "",
    customerPhone: "",
    customerEmail: "",
    time: "",
    date: "",
    partySize: "",
    specialRequests: ""
  });

  const { toast } = useToast();
  
  // Hooks API
  const { data: tablesData, isLoading: tablesLoading, refetch: refetchTables } = useTables();
  const occupyTableMutation = useOccupyTable();
  const freeTableMutation = useFreeTable();
  const createReservationMutation = useCreateReservation();

  // Extraire les tables des données paginées
  const tables = tablesData?.results || [];

  const occupyTable = (tableId: string, customerName: string) => {
    const numericId = parseInt(tableId);
    if (!isNaN(numericId)) {
      occupyTableMutation.mutate({
        tableId: numericId,
        customerName,
        partySize: 4
      });
    }
  };

  const freeTable = (tableId: string) => {
    const numericId = parseInt(tableId);
    if (!isNaN(numericId)) {
      freeTableMutation.mutate(numericId);
    }
  };

  const makeReservation = () => {
    if (!reservationData.tableId || !reservationData.customerName || 
        !reservationData.date || !reservationData.time || !reservationData.partySize) {
      toast({
        title: "Erreur",
        description: "Veuillez remplir tous les champs obligatoires",
        variant: "destructive"
      });
      return;
    }

    const reservationPayload = {
      table: parseInt(reservationData.tableId),
      customer_name: reservationData.customerName,
      customer_phone: reservationData.customerPhone || undefined,
      customer_email: reservationData.customerEmail || undefined,
      party_size: parseInt(reservationData.partySize),
      reservation_date: reservationData.date,
      reservation_time: reservationData.time + ":00", // Ajouter les secondes
      duration_minutes: 120,
      special_requests: reservationData.specialRequests || undefined
    };

    createReservationMutation.mutate(reservationPayload, {
      onSuccess: () => {
        setShowReservationDialog(false);
        setReservationData({
          tableId: "",
          customerName: "",
          customerPhone: "",
          customerEmail: "",
          time: "",
          date: "",
          partySize: "",
          specialRequests: ""
        });
        refetchTables();
      }
    });
  };

  const getOccupancyStats = () => {
    const occupied = tables.filter(t => t.status === "occupied").length;
    const reserved = tables.filter(t => t.status === "reserved").length;
    const available = tables.filter(t => t.status === "available").length;
    const total = tables.length;
    
    return { occupied, reserved, available, total, rate: total > 0 ? Math.round((occupied / total) * 100) : 0 };
  };

  const stats = getOccupancyStats();

  if (tablesLoading) {
    return (
      <div className="min-h-screen bg-gradient-surface flex">
        <Sidebar />
        <div className="flex-1 flex flex-col">
          <Header />
          <main className="flex-1 p-6 flex items-center justify-center">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
              <p>Chargement des tables...</p>
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
                    <Label>Table *</Label>
                    <Select value={reservationData.tableId} onValueChange={(value) => setReservationData(prev => ({...prev, tableId: value}))}>
                      <SelectTrigger>
                        <SelectValue placeholder="Sélectionner une table" />
                      </SelectTrigger>
                      <SelectContent>
                        {tables.filter(t => t.status === "available").map(table => (
                          <SelectItem key={table.id} value={table.id.toString()}>
                            Table {table.number} ({table.capacity} places)
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label>Nom du client *</Label>
                    <Input
                      placeholder="Nom du client"
                      value={reservationData.customerName}
                      onChange={(e) => setReservationData(prev => ({...prev, customerName: e.target.value}))}
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-2">
                    <div className="space-y-2">
                      <Label>Téléphone</Label>
                      <Input
                        placeholder="+257..."
                        value={reservationData.customerPhone}
                        onChange={(e) => setReservationData(prev => ({...prev, customerPhone: e.target.value}))}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label>Email</Label>
                      <Input
                        type="email"
                        placeholder="email@example.com"
                        value={reservationData.customerEmail}
                        onChange={(e) => setReservationData(prev => ({...prev, customerEmail: e.target.value}))}
                      />
                    </div>
                  </div>
                  <div className="grid grid-cols-3 gap-2">
                    <div className="space-y-2">
                      <Label>Date *</Label>
                      <Input
                        type="date"
                        value={reservationData.date}
                        onChange={(e) => setReservationData(prev => ({...prev, date: e.target.value}))}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label>Heure *</Label>
                      <Input
                        type="time"
                        value={reservationData.time}
                        onChange={(e) => setReservationData(prev => ({...prev, time: e.target.value}))}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label>Personnes *</Label>
                      <Input
                        type="number"
                        min="1"
                        max="20"
                        placeholder="4"
                        value={reservationData.partySize}
                        onChange={(e) => setReservationData(prev => ({...prev, partySize: e.target.value}))}
                      />
                    </div>
                  </div>
                  <div className="space-y-2">
                    <Label>Demandes spéciales</Label>
                    <Input
                      placeholder="Table près de la fenêtre, anniversaire..."
                      value={reservationData.specialRequests}
                      onChange={(e) => setReservationData(prev => ({...prev, specialRequests: e.target.value}))}
                    />
                  </div>
                  <Button 
                    onClick={makeReservation} 
                    className="w-full"
                    disabled={createReservationMutation.isPending}
                  >
                    {createReservationMutation.isPending ? "Création..." : "Confirmer la réservation"}
                  </Button>
                </div>
              </DialogContent>
            </Dialog>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Total Tables</CardTitle>
                <Utensils className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats.total}</div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Occupées</CardTitle>
                <Users className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-red-600">{stats.occupied}</div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Disponibles</CardTitle>
                <CheckCircle className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-green-600">{stats.available}</div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Taux d\'occupation</CardTitle>
                <AlertCircle className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats.rate}%</div>
              </CardContent>
            </Card>
          </div>

          {/* Tables Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {tables.map((table) => (
              <Card key={table.id} className={`cursor-pointer transition-all hover:shadow-md ${
                table.status === "occupied" ? "border-red-200 bg-red-50" :
                table.status === "reserved" ? "border-yellow-200 bg-yellow-50" :
                "border-green-200 bg-green-50"
              }`}>
                <CardHeader className="pb-3">
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-lg">Table {table.number}</CardTitle>
                    <Badge variant={
                      table.status === "occupied" ? "destructive" :
                      table.status === "reserved" ? "secondary" :
                      "default"
                    }>
                      {table.status === "occupied" ? "Occupée" :
                       table.status === "reserved" ? "Réservée" :
                       "Disponible"}
                    </Badge>
                  </div>
                  <div className="flex items-center gap-4 text-sm text-muted-foreground">
                    <div className="flex items-center gap-1">
                      <Users className="h-4 w-4" />
                      {table.capacity} places
                    </div>
                    {table.location && (
                      <div className="flex items-center gap-1">
                        <MapPin className="h-4 w-4" />
                        {table.location}
                      </div>
                    )}
                  </div>
                </CardHeader>
                <CardContent className="pt-0">
                  {table.status === "available" ? (
                    <Button 
                      onClick={() => {
                        const customerName = prompt("Nom du client:");
                        if (customerName) {
                          occupyTable(table.id.toString(), customerName);
                        }
                      }}
                      className="w-full"
                      size="sm"
                    >
                      Occuper
                    </Button>
                  ) : table.status === "occupied" ? (
                    <div className="space-y-2">
                      {table.customer && (
                        <div className="text-xs text-muted-foreground">
                          <strong>Client:</strong> {table.customer}
                        </div>
                      )}
                      {table.server && (
                        <div className="text-xs text-muted-foreground">
                          <strong>Serveur:</strong> {table.server}
                        </div>
                      )}
                      {table.occupied_since && (
                        <div className="flex items-center gap-1 text-xs text-muted-foreground">
                          <Clock className="h-3 w-3" />
                          Depuis {new Date(table.occupied_since).toLocaleTimeString()}
                        </div>
                      )}
                      <Button 
                        onClick={() => freeTable(table.id.toString())}
                        variant="outline"
                        className="w-full"
                        size="sm"
                      >
                        Libérer
                      </Button>
                    </div>
                  ) : (
                    <div className="text-center text-sm text-muted-foreground">
                      Réservée
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        </main>
      </div>
    </div>
  );
}