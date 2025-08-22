import { useState, useEffect } from "react";
import { Sidebar } from "@/components/layout/Sidebar";
import { Header } from "@/components/layout/Header";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { 
  Activity, 
  Server, 
  Database, 
  Wifi,
  HardDrive,
  Cpu,
  MemoryStick,
  RefreshCw,
  AlertTriangle,
  CheckCircle,
  Clock,
  Zap,
  FileText
} from "lucide-react";

interface SystemMetrics {
  api: {
    status: "online" | "offline" | "degraded";
    responseTime: number;
    uptime: number;
    requestsPerMinute: number;
  };
  database: {
    status: "online" | "offline" | "degraded";
    connections: number;
    queryTime: number;
    size: number;
  };
  server: {
    cpu: number;
    memory: number;
    disk: number;
    network: number;
  };
  services: {
    name: string;
    status: "running" | "stopped" | "error";
    uptime: string;
    lastRestart: string;
  }[];
}

const mockMetrics: SystemMetrics = {
  api: {
    status: "online",
    responseTime: 145,
    uptime: 99.8,
    requestsPerMinute: 42
  },
  database: {
    status: "online",
    connections: 8,
    queryTime: 23,
    size: 2.4
  },
  server: {
    cpu: 35,
    memory: 68,
    disk: 45,
    network: 12
  },
  services: [
    { name: "API Server", status: "running", uptime: "7d 14h 32m", lastRestart: "2024-08-07 09:15" },
    { name: "Database", status: "running", uptime: "15d 8h 45m", lastRestart: "2024-07-30 14:20" },
    { name: "Backup Service", status: "running", uptime: "7d 14h 32m", lastRestart: "2024-08-07 09:15" },
    { name: "Print Service", status: "error", uptime: "0m", lastRestart: "2024-08-14 16:30" }
  ]
};

const systemLogs = [
  { timestamp: "2024-08-14 16:45", level: "ERROR", service: "Print Service", message: "Connexion à l'imprimante échouée" },
  { timestamp: "2024-08-14 16:30", level: "WARN", service: "API Server", message: "Temps de réponse élevé détecté (>200ms)" },
  { timestamp: "2024-08-14 15:20", level: "INFO", service: "Database", message: "Sauvegarde automatique terminée avec succès" },
  { timestamp: "2024-08-14 14:15", level: "INFO", service: "API Server", message: "Nouveau utilisateur connecté: marie.uwimana" },
  { timestamp: "2024-08-14 13:45", level: "WARN", service: "Database", message: "Nombre de connexions élevé (>10)" }
];

export default function Monitoring() {
  const [metrics, setMetrics] = useState(mockMetrics);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [autoRefresh, setAutoRefresh] = useState(true);

  useEffect(() => {
    if (!autoRefresh) return;

    const interval = setInterval(() => {
      // Simulate real-time updates
      setMetrics(prev => ({
        ...prev,
        api: {
          ...prev.api,
          responseTime: Math.floor(Math.random() * 100) + 100,
          requestsPerMinute: Math.floor(Math.random() * 20) + 30
        },
        server: {
          ...prev.server,
          cpu: Math.floor(Math.random() * 30) + 20,
          memory: Math.floor(Math.random() * 20) + 60,
          network: Math.floor(Math.random() * 20) + 5
        }
      }));
    }, 5000);

    return () => clearInterval(interval);
  }, [autoRefresh]);

  const refreshMetrics = async () => {
    setIsRefreshing(true);
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));
    setIsRefreshing(false);
  };

  const getStatusInfo = (status: string) => {
    switch (status) {
      case "online":
      case "running":
        return { variant: "success" as const, label: "En ligne", icon: CheckCircle };
      case "offline":
      case "stopped":
        return { variant: "destructive" as const, label: "Hors ligne", icon: AlertTriangle };
      case "degraded":
      case "error":
        return { variant: "warning" as const, label: "Dégradé", icon: AlertTriangle };
      default:
        return { variant: "secondary" as const, label: status, icon: Clock };
    }
  };

  const getLogLevelInfo = (level: string) => {
    switch (level) {
      case "ERROR":
        return { variant: "destructive" as const, color: "text-destructive" };
      case "WARN":
        return { variant: "warning" as const, color: "text-warning" };
      case "INFO":
        return { variant: "secondary" as const, color: "text-secondary" };
      default:
        return { variant: "secondary" as const, color: "text-muted-foreground" };
    }
  };

  const restartService = (serviceName: string) => {
    // TODO: Implement service restart logic
    console.log(`Restarting service: ${serviceName}`);
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
                Surveillance système
              </h1>
              <p className="text-muted-foreground">
                Monitoring en temps réel des performances et services
              </p>
            </div>
            <div className="flex gap-2">
              <Button
                variant="outline"
                onClick={() => setAutoRefresh(!autoRefresh)}
                className={autoRefresh ? "bg-success/10" : ""}
              >
                {autoRefresh ? "Auto-refresh ON" : "Auto-refresh OFF"}
              </Button>
              <Button onClick={refreshMetrics} disabled={isRefreshing} className="gap-2">
                <RefreshCw className={`h-4 w-4 ${isRefreshing ? 'animate-spin' : ''}`} />
                Actualiser
              </Button>
            </div>
          </div>

          {/* System Status Overview */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-4">
                  <div className="h-12 w-12 bg-gradient-to-br from-success to-success/80 rounded-lg flex items-center justify-center">
                    <Server className="h-6 w-6 text-success-foreground" />
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">API Server</p>
                    <div className="flex items-center gap-2">
                      <Badge variant={getStatusInfo(metrics.api.status).variant}>
                        {getStatusInfo(metrics.api.status).label}
                      </Badge>
                      <span className="text-sm">{metrics.api.responseTime}ms</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-4">
                  <div className="h-12 w-12 bg-gradient-to-br from-primary to-primary-glow rounded-lg flex items-center justify-center">
                    <Database className="h-6 w-6 text-primary-foreground" />
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Base de données</p>
                    <div className="flex items-center gap-2">
                      <Badge variant={getStatusInfo(metrics.database.status).variant}>
                        {getStatusInfo(metrics.database.status).label}
                      </Badge>
                      <span className="text-sm">{metrics.database.connections} conn.</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-4">
                  <div className="h-12 w-12 bg-gradient-to-br from-warning to-warning/80 rounded-lg flex items-center justify-center">
                    <Activity className="h-6 w-6 text-warning-foreground" />
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Uptime global</p>
                    <div className="flex items-center gap-2">
                      <span className="text-xl font-bold text-success">{metrics.api.uptime}%</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          <Tabs defaultValue="performance" className="space-y-6">
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="performance">Performance</TabsTrigger>
              <TabsTrigger value="services">Services</TabsTrigger>
              <TabsTrigger value="logs">Logs</TabsTrigger>
              <TabsTrigger value="maintenance">Maintenance</TabsTrigger>
            </TabsList>

            {/* Performance Tab */}
            <TabsContent value="performance">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Cpu className="h-5 w-5" />
                      Ressources serveur
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-sm font-medium">CPU</span>
                        <span className="text-sm">{metrics.server.cpu}%</span>
                      </div>
                      <Progress value={metrics.server.cpu} className="h-2" />
                    </div>

                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-sm font-medium">Mémoire</span>
                        <span className="text-sm">{metrics.server.memory}%</span>
                      </div>
                      <Progress value={metrics.server.memory} className="h-2" />
                    </div>

                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-sm font-medium">Disque</span>
                        <span className="text-sm">{metrics.server.disk}%</span>
                      </div>
                      <Progress value={metrics.server.disk} className="h-2" />
                    </div>

                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-sm font-medium">Réseau</span>
                        <span className="text-sm">{metrics.server.network} MB/s</span>
                      </div>
                      <Progress value={metrics.server.network * 5} className="h-2" />
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Zap className="h-5 w-5" />
                      Métriques de performance
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div className="text-center p-4 bg-muted rounded-lg">
                        <p className="text-2xl font-bold">{metrics.api.responseTime}ms</p>
                        <p className="text-sm text-muted-foreground">Temps de réponse API</p>
                      </div>
                      <div className="text-center p-4 bg-muted rounded-lg">
                        <p className="text-2xl font-bold">{metrics.api.requestsPerMinute}</p>
                        <p className="text-sm text-muted-foreground">Requêtes/min</p>
                      </div>
                      <div className="text-center p-4 bg-muted rounded-lg">
                        <p className="text-2xl font-bold">{metrics.database.queryTime}ms</p>
                        <p className="text-sm text-muted-foreground">Temps requête DB</p>
                      </div>
                      <div className="text-center p-4 bg-muted rounded-lg">
                        <p className="text-2xl font-bold">{metrics.database.size}GB</p>
                        <p className="text-sm text-muted-foreground">Taille DB</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>

            {/* Services Tab */}
            <TabsContent value="services">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Server className="h-5 w-5" />
                    État des services
                  </CardTitle>
                  <CardDescription>
                    Surveillance des services critiques du système
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {metrics.services.map((service, index) => {
                      const statusInfo = getStatusInfo(service.status);
                      const StatusIcon = statusInfo.icon;
                      
                      return (
                        <div
                          key={index}
                          className="flex items-center justify-between p-4 border rounded-lg"
                        >
                          <div className="flex items-center gap-4">
                            <div className={`h-10 w-10 rounded-lg flex items-center justify-center ${
                              service.status === "running" ? "bg-success" :
                              service.status === "error" ? "bg-destructive" :
                              "bg-secondary"
                            }`}>
                              <StatusIcon className="h-5 w-5 text-white" />
                            </div>
                            <div>
                              <h3 className="font-semibold">{service.name}</h3>
                              <p className="text-sm text-muted-foreground">
                                Uptime: {service.uptime}
                              </p>
                            </div>
                          </div>

                          <div className="text-right">
                            <Badge variant={statusInfo.variant} className="mb-2">
                              {statusInfo.label}
                            </Badge>
                            <p className="text-sm text-muted-foreground">
                              Dernier redémarrage: {service.lastRestart}
                            </p>
                            {service.status === "error" && (
                              <Button 
                                size="sm" 
                                onClick={() => restartService(service.name)}
                                className="mt-2 gap-1"
                              >
                                <RefreshCw className="h-3 w-3" />
                                Redémarrer
                              </Button>
                            )}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Logs Tab */}
            <TabsContent value="logs">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <FileText className="h-5 w-5" />
                    Logs système
                  </CardTitle>
                  <CardDescription>
                    Historique des événements et erreurs système
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {systemLogs.map((log, index) => {
                      const levelInfo = getLogLevelInfo(log.level);
                      
                      return (
                        <div
                          key={index}
                          className="flex items-start gap-4 p-3 border rounded-lg hover:bg-muted/50 transition-colors"
                        >
                          <Badge variant={levelInfo.variant} className="mt-1">
                            {log.level}
                          </Badge>
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-1">
                              <span className="font-medium">{log.service}</span>
                              <span className="text-sm text-muted-foreground">{log.timestamp}</span>
                            </div>
                            <p className="text-sm">{log.message}</p>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Maintenance Tab */}
            <TabsContent value="maintenance">
              <div className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Actions de maintenance</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <Button variant="outline" className="h-20 flex-col gap-2">
                        <Database className="h-6 w-6" />
                        <span>Optimiser la base de données</span>
                      </Button>
                      <Button variant="outline" className="h-20 flex-col gap-2">
                        <HardDrive className="h-6 w-6" />
                        <span>Nettoyer les fichiers temporaires</span>
                      </Button>
                      <Button variant="outline" className="h-20 flex-col gap-2">
                        <RefreshCw className="h-6 w-6" />
                        <span>Redémarrer tous les services</span>
                      </Button>
                      <Button variant="outline" className="h-20 flex-col gap-2">
                        <FileText className="h-6 w-6" />
                        <span>Archiver les anciens logs</span>
                      </Button>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle>Planification de maintenance</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="flex items-center justify-between p-3 border rounded-lg">
                        <div>
                          <h4 className="font-medium">Sauvegarde quotidienne</h4>
                          <p className="text-sm text-muted-foreground">Prochaine: Demain à 02:00</p>
                        </div>
                        <Badge variant="success">Planifiée</Badge>
                      </div>
                      <div className="flex items-center justify-between p-3 border rounded-lg">
                        <div>
                          <h4 className="font-medium">Optimisation DB</h4>
                          <p className="text-sm text-muted-foreground">Prochaine: Dimanche à 01:00</p>
                        </div>
                        <Badge variant="secondary">Hebdomadaire</Badge>
                      </div>
                      <div className="flex items-center justify-between p-3 border rounded-lg">
                        <div>
                          <h4 className="font-medium">Nettoyage logs</h4>
                          <p className="text-sm text-muted-foreground">Prochaine: 1er septembre</p>
                        </div>
                        <Badge variant="warning">Mensuelle</Badge>
                      </div>
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
