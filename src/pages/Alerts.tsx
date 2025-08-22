import { useState } from "react";
import { Sidebar } from "@/components/layout/Sidebar";
import { Header } from "@/components/layout/Header";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Label } from "@/components/ui/label";
import { useAlerts, useResolveAlert, useArchiveAlert } from "@/hooks/use-api";
import { useToast } from "@/hooks/use-toast";
import { 
  AlertTriangle, 
  Bell, 
  CheckCircle, 
  X,
  Clock,
  Package,
  DollarSign,
  Users,
  Settings,
  Filter,
  Archive,
  Trash2
} from "lucide-react";

interface Alert {
  id: number;
  type: "stock" | "sales" | "system" | "security" | "maintenance";
  priority: "low" | "medium" | "high" | "critical";
  title: string;
  message: string;
  created_at: string;
  status: "active" | "resolved" | "archived";
  related_product?: any;
  related_sale?: any;
  created_by?: any;
  resolved_by?: any;
}


export default function Alerts() {
  const [selectedType, setSelectedType] = useState("all");
  const [selectedPriority, setSelectedPriority] = useState("all");
  const [selectedStatus, setSelectedStatus] = useState("all");
  const { toast } = useToast();
  
  const { data: alertsData, isLoading, refetch } = useAlerts({
    type: selectedType !== "all" ? selectedType : undefined,
    priority: selectedPriority !== "all" ? selectedPriority : undefined,
    status: selectedStatus !== "all" ? selectedStatus : undefined
  });
  
  const resolveAlertMutation = useResolveAlert();
  const archiveAlertMutation = useArchiveAlert();
  
  const alerts = alertsData?.results || [];

  const alertTypes = [
    { value: "all", label: "Tous les types", icon: Bell },
    { value: "stock", label: "Stock", icon: Package },
    { value: "sales", label: "Ventes", icon: DollarSign },
    { value: "system", label: "Système", icon: Settings },
    { value: "security", label: "Sécurité", icon: AlertTriangle },
    { value: "maintenance", label: "Maintenance", icon: Settings }
  ];

  const priorities = [
    { value: "all", label: "Toutes priorités" },
    { value: "critical", label: "Critique" },
    { value: "high", label: "Élevée" },
    { value: "medium", label: "Moyenne" },
    { value: "low", label: "Faible" }
  ];

  const statuses = [
    { value: "all", label: "Tous statuts" },
    { value: "active", label: "Actives" },
    { value: "resolved", label: "Résolues" },
    { value: "archived", label: "Archivées" }
  ];

  const getPriorityInfo = (priority: Alert["priority"]) => {
    switch (priority) {
      case "critical":
        return { variant: "destructive" as const, label: "Critique", color: "text-destructive" };
      case "high":
        return { variant: "destructive" as const, label: "Élevée", color: "text-destructive" };
      case "medium":
        return { variant: "warning" as const, label: "Moyenne", color: "text-warning" };
      case "low":
        return { variant: "secondary" as const, label: "Faible", color: "text-secondary" };
    }
  };

  const getStatusInfo = (status: Alert["status"]) => {
    switch (status) {
      case "active":
        return { variant: "destructive" as const, label: "Active", icon: Bell };
      case "resolved":
        return { variant: "success" as const, label: "Résolue", icon: CheckCircle };
      case "archived":
        return { variant: "secondary" as const, label: "Archivée", icon: Archive };
      default:
        return { variant: "secondary" as const, label: "Inconnue", icon: Bell };
    }
  };

  const getTypeIcon = (type: Alert["type"]) => {
    const typeInfo = alertTypes.find(t => t.value === type);
    return typeInfo?.icon || Bell;
  };

  const filteredAlerts = alerts;

  const handleResolveAlert = async (alertId: number) => {
    try {
      await resolveAlertMutation.mutateAsync(alertId);
      refetch();
    } catch (error) {
      console.error('Erreur lors de la résolution de l\'alerte:', error);
    }
  };

  const handleArchiveAlert = async (alertId: number) => {
    try {
      await archiveAlertMutation.mutateAsync(alertId);
      refetch();
    } catch (error) {
      console.error('Erreur lors de l\'archivage de l\'alerte:', error);
    }
  };

  const getAlertStats = () => {
    const active = alerts.filter(a => a.status === "active").length;
    const critical = alerts.filter(a => a.priority === "critical" && a.status !== "resolved").length;
    const resolved = alerts.filter(a => a.status === "resolved").length;
    
    return { active, critical, resolved };
  };

  const stats = getAlertStats();
  
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-surface flex">
        <Sidebar />
        <div className="flex-1 flex flex-col">
          <Header />
          <main className="flex-1 p-6 flex items-center justify-center">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
              <p className="text-muted-foreground">Chargement des alertes...</p>
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
                Centre d'alertes
              </h1>
              <p className="text-muted-foreground">
                Notifications centralisées et gestion des alertes système
              </p>
            </div>
            <Button onClick={() => refetch()} variant="outline" className="gap-2">
              <CheckCircle className="h-4 w-4" />
              Actualiser
            </Button>
          </div>

          {/* Alert Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-4">
                  <div className="h-12 w-12 bg-gradient-to-br from-destructive to-destructive/80 rounded-lg flex items-center justify-center">
                    <Bell className="h-6 w-6 text-destructive-foreground" />
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Actives</p>
                    <p className="text-2xl font-bold text-destructive">{stats.active}</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-4">
                  <div className="h-12 w-12 bg-gradient-to-br from-destructive to-destructive/80 rounded-lg flex items-center justify-center">
                    <AlertTriangle className="h-6 w-6 text-destructive-foreground" />
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Critiques</p>
                    <p className="text-2xl font-bold text-destructive">{stats.critical}</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-4">
                  <div className="h-12 w-12 bg-gradient-to-br from-warning to-warning/80 rounded-lg flex items-center justify-center">
                    <Clock className="h-6 w-6 text-warning-foreground" />
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Résolues</p>
                    <p className="text-2xl font-bold text-success">{stats.resolved}</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-4">
                  <div className="h-12 w-12 bg-gradient-to-br from-primary to-primary-glow rounded-lg flex items-center justify-center">
                    <Bell className="h-6 w-6 text-primary-foreground" />
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Total alertes</p>
                    <p className="text-2xl font-bold">{alerts.length}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Filters */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Filter className="h-5 w-5" />
                Filtres
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="space-y-2">
                  <Label>Type d'alerte</Label>
                  <Select value={selectedType} onValueChange={setSelectedType}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {alertTypes.map(type => (
                        <SelectItem key={type.value} value={type.value}>
                          {type.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label>Priorité</Label>
                  <Select value={selectedPriority} onValueChange={setSelectedPriority}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {priorities.map(priority => (
                        <SelectItem key={priority.value} value={priority.value}>
                          {priority.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label>Statut</Label>
                  <Select value={selectedStatus} onValueChange={setSelectedStatus}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {statuses.map(status => (
                        <SelectItem key={status.value} value={status.value}>
                          {status.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Alerts List */}
          <Card>
            <CardHeader>
              <CardTitle>Alertes ({filteredAlerts.length})</CardTitle>
              <CardDescription>
                Notifications triées par priorité et date
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {filteredAlerts
                  .sort((a, b) => {
                    // Sort by priority first, then by timestamp
                    const priorityOrder = { critical: 4, high: 3, medium: 2, low: 1 };
                    const priorityDiff = priorityOrder[b.priority] - priorityOrder[a.priority];
                    if (priorityDiff !== 0) return priorityDiff;
                    return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
                  })
                  .map((alert) => {
                    const priorityInfo = getPriorityInfo(alert.priority);
                    const statusInfo = getStatusInfo(alert.status);
                    const TypeIcon = getTypeIcon(alert.type);
                    const StatusIcon = statusInfo.icon;
                    
                    return (
                      <div
                        key={alert.id}
                        className={`flex items-start gap-4 p-4 border rounded-lg transition-colors ${
                          alert.status === "active" ? "bg-primary/5 border-primary/20" : "hover:bg-muted/50"
                        }`}
                      >
                        <div className={`h-10 w-10 rounded-lg flex items-center justify-center ${
                          alert.priority === "critical" ? "bg-destructive" :
                          alert.priority === "high" ? "bg-destructive/80" :
                          alert.priority === "medium" ? "bg-warning" :
                          "bg-secondary"
                        }`}>
                          <TypeIcon className="h-5 w-5 text-white" />
                        </div>

                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-2">
                            <h3 className={`font-semibold ${alert.status === "active" ? "text-primary" : ""}`}>
                              {alert.title}
                            </h3>
                            <Badge variant={priorityInfo.variant}>{priorityInfo.label}</Badge>
                            <Badge variant={statusInfo.variant} className="gap-1">
                              <StatusIcon className="h-3 w-3" />
                              {statusInfo.label}
                            </Badge>
                          </div>
                          
                          <p className="text-muted-foreground mb-2">{alert.message}</p>
                          
                          <div className="flex items-center gap-4 text-sm text-muted-foreground">
                            <span className="flex items-center gap-1">
                              <Clock className="h-3 w-3" />
                              {new Date(alert.created_at).toLocaleString('fr-FR')}
                            </span>
                            {alert.related_product && (
                              <span>Produit: {alert.related_product.name}</span>
                            )}
                            {alert.related_sale && (
                              <span>Vente: #{alert.related_sale.id}</span>
                            )}
                          </div>
                        </div>

                        <div className="flex gap-2">
                          {alert.status === "active" && (
                            <Button 
                              size="sm"
                              onClick={() => handleResolveAlert(alert.id)}
                              disabled={resolveAlertMutation.isPending}
                              className="gap-1"
                            >
                              <CheckCircle className="h-4 w-4" />
                              Résoudre
                            </Button>
                          )}

                          <Button 
                            variant="outline" 
                            size="sm"
                            onClick={() => handleArchiveAlert(alert.id)}
                            disabled={archiveAlertMutation.isPending}
                          >
                            <Archive className="h-4 w-4" />
                          </Button>
                        </div>
                      </div>
                    );
                  })}

                {filteredAlerts.length === 0 && (
                  <div className="text-center py-12">
                    <Bell className="h-16 w-16 text-muted-foreground mx-auto mb-4" />
                    <h3 className="text-lg font-semibold mb-2">Aucune alerte</h3>
                    <p className="text-muted-foreground">
                      Aucune alerte ne correspond aux filtres sélectionnés
                    </p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </main>
      </div>
    </div>
  );
}
