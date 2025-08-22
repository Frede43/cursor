import { useState, useEffect } from "react";
import { Sidebar } from "@/components/layout/Sidebar";
import { Header } from "@/components/layout/Header";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { 
  Settings as SettingsIcon, 
  Save, 
  Globe, 
  DollarSign,
  Bell,
  Printer,
  Database,
  Shield,
  Download,
  Upload,
  AlertTriangle,
  CheckCircle,
  Loader2
} from "lucide-react";
import { useSystemSettings, useUpdateSystemSettings, useResetSystemSettings, useCreateBackup, useSystemInfo } from "@/hooks/use-api";
import { useToast } from "@/hooks/use-toast";

interface SystemSettings {
  general: {
    businessName: string;
    currency: string;
    taxRate: number;
    language: string;
    timezone: string;
  };
  notifications: {
    lowStockAlerts: boolean;
    salesNotifications: boolean;
    systemAlerts: boolean;
    emailReports: boolean;
    stockThreshold: number;
  };
  printing: {
    receiptPrinter: string;
    autoprint: boolean;
    receiptTemplate: string;
  };
  security: {
    sessionTimeout: number;
    passwordPolicy: boolean;
    twoFactorAuth: boolean;
    auditLog: boolean;
  };
  backup: {
    autoBackup: boolean;
    backupFrequency: string;
    lastBackup: string;
  };
}

const defaultSettings: SystemSettings = {
  general: {
    businessName: "Bar Stock Wise",
    currency: "FBu",
    taxRate: 5,
    language: "fr",
    timezone: "Africa/Bujumbura"
  },
  notifications: {
    lowStockAlerts: true,
    salesNotifications: true,
    systemAlerts: true,
    emailReports: false,
    stockThreshold: 20
  },
  printing: {
    receiptPrinter: "HP LaserJet Pro",
    autoprint: true,
    receiptTemplate: "standard"
  },
  security: {
    sessionTimeout: 30,
    passwordPolicy: true,
    twoFactorAuth: false,
    auditLog: true
  },
  backup: {
    autoBackup: true,
    backupFrequency: "daily",
    lastBackup: "2024-08-14 02:00:00"
  }
};

export default function Settings() {
  const [settings, setSettings] = useState(defaultSettings);
  const [hasChanges, setHasChanges] = useState(false);
  const { toast } = useToast();
  
  // API Hooks
  const { data: systemSettings, isLoading: settingsLoading, refetch: refetchSettings } = useSystemSettings();
  const { data: systemInfo, isLoading: infoLoading } = useSystemInfo();
  const updateSettingsMutation = useUpdateSystemSettings();
  const resetSettingsMutation = useResetSystemSettings();
  const createBackupMutation = useCreateBackup();
  
  // Load settings from API when available
  useEffect(() => {
    if (systemSettings) {
      const mappedSettings = {
        general: {
          businessName: systemSettings.restaurant?.name || defaultSettings.general.businessName,
          currency: systemSettings.restaurant?.currency || defaultSettings.general.currency,
          taxRate: systemSettings.restaurant?.tax_rate || defaultSettings.general.taxRate,
          language: systemSettings.system?.language || defaultSettings.general.language,
          timezone: systemSettings.system?.timezone || defaultSettings.general.timezone
        },
        notifications: {
          lowStockAlerts: systemSettings.notifications?.low_stock_alerts ?? defaultSettings.notifications.lowStockAlerts,
          salesNotifications: systemSettings.notifications?.email_enabled ?? defaultSettings.notifications.salesNotifications,
          systemAlerts: systemSettings.notifications?.email_enabled ?? defaultSettings.notifications.systemAlerts,
          emailReports: systemSettings.notifications?.daily_reports ?? defaultSettings.notifications.emailReports,
          stockThreshold: 20 // This could be added to backend model
        },
        printing: {
          receiptPrinter: systemSettings.printing?.printer_name || defaultSettings.printing.receiptPrinter,
          autoprint: systemSettings.printing?.auto_print_receipts ?? defaultSettings.printing.autoprint,
          receiptTemplate: "standard" // This could be added to backend model
        },
        security: {
          sessionTimeout: 30, // This could be added to backend model
          passwordPolicy: true, // This could be added to backend model
          twoFactorAuth: false, // This could be added to backend model
          auditLog: true // This could be added to backend model
        },
        backup: {
          autoBackup: systemSettings.system?.backup_frequency !== "never",
          backupFrequency: systemSettings.system?.backup_frequency || defaultSettings.backup.backupFrequency,
          lastBackup: systemInfo?.last_backup || defaultSettings.backup.lastBackup
        }
      };
      setSettings(mappedSettings);
      setHasChanges(false);
    }
  }, [systemSettings, systemInfo]);

  const updateSetting = (section: keyof SystemSettings, key: string, value: any) => {
    setSettings(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        [key]: value
      }
    }));
    setHasChanges(true);
  };

  const saveSettings = async () => {
    const apiData = {
      restaurant: {
        name: settings.general.businessName,
        currency: settings.general.currency,
        tax_rate: settings.general.taxRate
      },
      notifications: {
        low_stock_alerts: settings.notifications.lowStockAlerts,
        email_enabled: settings.notifications.salesNotifications,
        daily_reports: settings.notifications.emailReports
      },
      printing: {
        printer_name: settings.printing.receiptPrinter,
        auto_print_receipts: settings.printing.autoprint
      },
      system: {
        language: settings.general.language,
        timezone: settings.general.timezone,
        backup_frequency: settings.backup.backupFrequency
      }
    };
    
    try {
      await updateSettingsMutation.mutateAsync(apiData);
      setHasChanges(false);
      refetchSettings();
    } catch (error) {
      console.error('Error saving settings:', error);
    }
  };

  const resetSettings = async () => {
    if (confirm("Êtes-vous sûr de vouloir réinitialiser tous les paramètres ?")) {
      try {
        await resetSettingsMutation.mutateAsync();
        setHasChanges(false);
        refetchSettings();
      } catch (error) {
        console.error('Error resetting settings:', error);
      }
    }
  };

  const createBackup = async () => {
    try {
      await createBackupMutation.mutateAsync();
      // Update last backup time in local state
      updateSetting("backup", "lastBackup", new Date().toLocaleString());
    } catch (error) {
      console.error('Error creating backup:', error);
    }
  };

  const restoreBackup = () => {
    toast({
      title: "Fonctionnalité en développement",
      description: "La restauration de sauvegarde sera bientôt disponible.",
      variant: "default"
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
                Paramètres système
              </h1>
              <p className="text-muted-foreground">
                Configuration générale et préférences du système
              </p>
            </div>
            <div className="flex gap-2">
              {hasChanges && (
                <Alert className="w-auto">
                  <AlertTriangle className="h-4 w-4" />
                  <AlertDescription>Modifications non sauvegardées</AlertDescription>
                </Alert>
              )}
              <Button 
                onClick={saveSettings} 
                disabled={!hasChanges || updateSettingsMutation.isPending} 
                className="gap-2"
              >
                {updateSettingsMutation.isPending ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  <Save className="h-4 w-4" />
                )}
                {updateSettingsMutation.isPending ? "Sauvegarde..." : "Sauvegarder"}
              </Button>
            </div>
          </div>

          <Tabs defaultValue="general" className="space-y-6">
            <TabsList className="grid w-full grid-cols-5">
              <TabsTrigger value="general">Général</TabsTrigger>
              <TabsTrigger value="notifications">Notifications</TabsTrigger>
              <TabsTrigger value="printing">Impression</TabsTrigger>
              <TabsTrigger value="security">Sécurité</TabsTrigger>
              <TabsTrigger value="backup">Sauvegarde</TabsTrigger>
            </TabsList>

            {/* General Settings */}
            <TabsContent value="general">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Globe className="h-5 w-5" />
                    Paramètres généraux
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label>Nom de l'établissement</Label>
                      <Input
                        value={settings.general.businessName}
                        onChange={(e) => updateSetting("general", "businessName", e.target.value)}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label>Devise</Label>
                      <Select 
                        value={settings.general.currency} 
                        onValueChange={(value) => updateSetting("general", "currency", value)}
                      >
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="FBu">Franc Burundais (FBu)</SelectItem>
                          <SelectItem value="USD">Dollar US ($)</SelectItem>
                          <SelectItem value="EUR">Euro (€)</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="space-y-2">
                      <Label>Taux de taxe (%)</Label>
                      <Input
                        type="number"
                        value={settings.general.taxRate}
                        onChange={(e) => updateSetting("general", "taxRate", parseFloat(e.target.value))}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label>Langue</Label>
                      <Select 
                        value={settings.general.language} 
                        onValueChange={(value) => updateSetting("general", "language", value)}
                      >
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="fr">Français</SelectItem>
                          <SelectItem value="en">English</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    <div className="space-y-2">
                      <Label>Fuseau horaire</Label>
                      <Select 
                        value={settings.general.timezone} 
                        onValueChange={(value) => updateSetting("general", "timezone", value)}
                      >
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="Africa/Bujumbura">Bujumbura (UTC+2)</SelectItem>
                          <SelectItem value="Europe/Paris">Paris (UTC+1)</SelectItem>
                          <SelectItem value="UTC">UTC (UTC+0)</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Notifications Settings */}
            <TabsContent value="notifications">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Bell className="h-5 w-5" />
                    Paramètres de notification
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <Label>Alertes de stock faible</Label>
                        <p className="text-sm text-muted-foreground">Recevoir des notifications quand le stock est bas</p>
                      </div>
                      <Switch
                        checked={settings.notifications.lowStockAlerts}
                        onCheckedChange={(checked) => updateSetting("notifications", "lowStockAlerts", checked)}
                      />
                    </div>

                    <div className="flex items-center justify-between">
                      <div>
                        <Label>Notifications de ventes</Label>
                        <p className="text-sm text-muted-foreground">Notifications pour les nouvelles ventes</p>
                      </div>
                      <Switch
                        checked={settings.notifications.salesNotifications}
                        onCheckedChange={(checked) => updateSetting("notifications", "salesNotifications", checked)}
                      />
                    </div>

                    <div className="flex items-center justify-between">
                      <div>
                        <Label>Alertes système</Label>
                        <p className="text-sm text-muted-foreground">Notifications pour les erreurs et maintenance</p>
                      </div>
                      <Switch
                        checked={settings.notifications.systemAlerts}
                        onCheckedChange={(checked) => updateSetting("notifications", "systemAlerts", checked)}
                      />
                    </div>

                    <div className="flex items-center justify-between">
                      <div>
                        <Label>Rapports par email</Label>
                        <p className="text-sm text-muted-foreground">Envoi automatique des rapports quotidiens</p>
                      </div>
                      <Switch
                        checked={settings.notifications.emailReports}
                        onCheckedChange={(checked) => updateSetting("notifications", "emailReports", checked)}
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label>Seuil d'alerte de stock (unités)</Label>
                    <Input
                      type="number"
                      value={settings.notifications.stockThreshold}
                      onChange={(e) => updateSetting("notifications", "stockThreshold", parseInt(e.target.value))}
                      className="w-32"
                    />
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Printing Settings */}
            <TabsContent value="printing">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Printer className="h-5 w-5" />
                    Paramètres d'impression
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <Label>Imprimante de reçus</Label>
                    <Select 
                      value={settings.printing.receiptPrinter} 
                      onValueChange={(value) => updateSetting("printing", "receiptPrinter", value)}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="HP LaserJet Pro">HP LaserJet Pro</SelectItem>
                        <SelectItem value="Epson TM-T20">Epson TM-T20</SelectItem>
                        <SelectItem value="Canon PIXMA">Canon PIXMA</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="flex items-center justify-between">
                    <div>
                      <Label>Impression automatique</Label>
                      <p className="text-sm text-muted-foreground">Imprimer automatiquement les reçus après chaque vente</p>
                    </div>
                    <Switch
                      checked={settings.printing.autoprint}
                      onCheckedChange={(checked) => updateSetting("printing", "autoprint", checked)}
                    />
                  </div>

                  <div className="space-y-2">
                    <Label>Modèle de reçu</Label>
                    <Select 
                      value={settings.printing.receiptTemplate} 
                      onValueChange={(value) => updateSetting("printing", "receiptTemplate", value)}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="standard">Standard</SelectItem>
                        <SelectItem value="detailed">Détaillé</SelectItem>
                        <SelectItem value="minimal">Minimal</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Security Settings */}
            <TabsContent value="security">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Shield className="h-5 w-5" />
                    Paramètres de sécurité
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="space-y-2">
                    <Label>Délai d'expiration de session (minutes)</Label>
                    <Input
                      type="number"
                      value={settings.security.sessionTimeout}
                      onChange={(e) => updateSetting("security", "sessionTimeout", parseInt(e.target.value))}
                      className="w-32"
                    />
                  </div>

                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <Label>Politique de mot de passe renforcée</Label>
                        <p className="text-sm text-muted-foreground">Exiger des mots de passe complexes</p>
                      </div>
                      <Switch
                        checked={settings.security.passwordPolicy}
                        onCheckedChange={(checked) => updateSetting("security", "passwordPolicy", checked)}
                      />
                    </div>

                    <div className="flex items-center justify-between">
                      <div>
                        <Label>Authentification à deux facteurs</Label>
                        <p className="text-sm text-muted-foreground">Sécurité renforcée pour les connexions</p>
                      </div>
                      <Switch
                        checked={settings.security.twoFactorAuth}
                        onCheckedChange={(checked) => updateSetting("security", "twoFactorAuth", checked)}
                      />
                    </div>

                    <div className="flex items-center justify-between">
                      <div>
                        <Label>Journal d'audit</Label>
                        <p className="text-sm text-muted-foreground">Enregistrer toutes les actions utilisateur</p>
                      </div>
                      <Switch
                        checked={settings.security.auditLog}
                        onCheckedChange={(checked) => updateSetting("security", "auditLog", checked)}
                      />
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Backup Settings */}
            <TabsContent value="backup">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Database className="h-5 w-5" />
                    Sauvegarde et restauration
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <Label>Sauvegarde automatique</Label>
                      <p className="text-sm text-muted-foreground">Sauvegarder automatiquement les données</p>
                    </div>
                    <Switch
                      checked={settings.backup.autoBackup}
                      onCheckedChange={(checked) => updateSetting("backup", "autoBackup", checked)}
                    />
                  </div>

                  <div className="space-y-2">
                    <Label>Fréquence de sauvegarde</Label>
                    <Select 
                      value={settings.backup.backupFrequency} 
                      onValueChange={(value) => updateSetting("backup", "backupFrequency", value)}
                    >
                      <SelectTrigger className="w-48">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="hourly">Toutes les heures</SelectItem>
                        <SelectItem value="daily">Quotidienne</SelectItem>
                        <SelectItem value="weekly">Hebdomadaire</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-4">
                    <div>
                      <p className="text-sm text-muted-foreground">Dernière sauvegarde</p>
                      <p className="font-medium">
                        {systemInfo?.last_backup 
                          ? new Date(systemInfo.last_backup).toLocaleString('fr-FR')
                          : settings.backup.lastBackup
                        }
                      </p>
                    </div>

                    <div className="flex gap-2">
                      <Button 
                        onClick={createBackup} 
                        variant="outline" 
                        className="gap-2"
                        disabled={createBackupMutation.isPending}
                      >
                        {createBackupMutation.isPending ? (
                          <Loader2 className="h-4 w-4 animate-spin" />
                        ) : (
                          <Download className="h-4 w-4" />
                        )}
                        {createBackupMutation.isPending ? "Création..." : "Créer une sauvegarde"}
                      </Button>
                      <Button onClick={restoreBackup} variant="outline" className="gap-2">
                        <Upload className="h-4 w-4" />
                        Restaurer
                      </Button>
                    </div>
                  </div>

                  <Alert>
                    <CheckCircle className="h-4 w-4" />
                    <AlertDescription>
                      Les sauvegardes sont stockées de manière sécurisée et chiffrées. 
                      Conservez toujours une copie locale de vos données importantes.
                    </AlertDescription>
                  </Alert>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>

          {/* Danger Zone */}
          <Card className="border-destructive/20">
            <CardHeader>
              <CardTitle className="text-destructive">Zone de danger</CardTitle>
              <CardDescription>
                Actions irréversibles - utilisez avec précaution
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between p-4 border border-destructive/20 rounded-lg">
                <div>
                  <h4 className="font-medium">Réinitialiser les paramètres</h4>
                  <p className="text-sm text-muted-foreground">
                    Restaurer tous les paramètres aux valeurs par défaut
                  </p>
                </div>
                <Button 
                  variant="destructive" 
                  onClick={resetSettings}
                  disabled={resetSettingsMutation.isPending}
                >
                  {resetSettingsMutation.isPending ? (
                    <>
                      <Loader2 className="h-4 w-4 animate-spin mr-2" />
                      Réinitialisation...
                    </>
                  ) : (
                    "Réinitialiser"
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>
        </main>
      </div>
    </div>
  );
}
