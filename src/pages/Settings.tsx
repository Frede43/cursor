import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Textarea } from '@/components/ui/textarea';
import {
  Settings as SettingsIcon, Save, RotateCcw, Bell,
  Printer, Shield, Database, Palette
} from 'lucide-react';
import { useSystemSettingsNew, useUpdateSystemSettingsNew } from '@/hooks/use-api';
import { useToast } from '@/hooks/use-toast';

export default function Settings() {
  const [activeTab, setActiveTab] = useState('general');
  const [localSettings, setLocalSettings] = useState<Record<string, any>>({});
  const { toast } = useToast();

  const { data: systemSettings, isLoading } = useSystemSettingsNew();
  const updateSettings = useUpdateSystemSettingsNew();

  useEffect(() => {
    if (systemSettings) {
      setLocalSettings(systemSettings);
    }
  }, [systemSettings]);

  const handleSettingChange = (key: string, value: any) => {
    setLocalSettings(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const handleSaveSettings = async () => {
    try {
      await updateSettings.mutateAsync(localSettings);
    } catch (error) {
      console.error('Erreur sauvegarde paramètres:', error);
    }
  };

  const handleResetSettings = () => {
    if (systemSettings) {
      setLocalSettings(systemSettings);
      toast({
        title: "Paramètres réinitialisés",
        description: "Les modifications ont été annulées",
      });
    }
  };

  if (isLoading) {
    return (
      <div className="container mx-auto p-6">
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
            <p className="text-muted-foreground">Chargement des paramètres...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Paramètres Système</h1>
          <p className="text-muted-foreground">
            Configuration et personnalisation de l'application
          </p>
        </div>
        <SettingsIcon className="h-8 w-8 text-muted-foreground" />
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="general">Général</TabsTrigger>
          <TabsTrigger value="notifications">Notifications</TabsTrigger>
          <TabsTrigger value="printing">Impression</TabsTrigger>
          <TabsTrigger value="security">Sécurité</TabsTrigger>
        </TabsList>

        <TabsContent value="general" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Palette className="h-5 w-5" />
                Paramètres Généraux
              </CardTitle>
              <CardDescription>
                Configuration de base de l'application
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-2">
                  <Label htmlFor="app_name">Nom de l'application</Label>
                  <Input
                    id="app_name"
                    value={localSettings.app_name || 'BarStockWise'}
                    onChange={(e) => handleSettingChange('app_name', e.target.value)}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="company_name">Nom de l'entreprise</Label>
                  <Input
                    id="company_name"
                    value={localSettings.company_name || ''}
                    onChange={(e) => handleSettingChange('company_name', e.target.value)}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="currency">Devise</Label>
                  <Select
                    value={localSettings.currency || 'BIF'}
                    onValueChange={(value) => handleSettingChange('currency', value)}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="BIF">Franc Burundais (BIF)</SelectItem>
                      <SelectItem value="USD">Dollar US (USD)</SelectItem>
                      <SelectItem value="EUR">Euro (EUR)</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="timezone">Fuseau horaire</Label>
                  <Select
                    value={localSettings.timezone || 'Africa/Bujumbura'}
                    onValueChange={(value) => handleSettingChange('timezone', value)}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="Africa/Bujumbura">Bujumbura</SelectItem>
                      <SelectItem value="UTC">UTC</SelectItem>
                      <SelectItem value="Europe/Paris">Paris</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="company_address">Adresse de l'entreprise</Label>
                <Textarea
                  id="company_address"
                  value={localSettings.company_address || ''}
                  onChange={(e) => handleSettingChange('company_address', e.target.value)}
                  rows={3}
                />
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="notifications" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Bell className="h-5 w-5" />
                Paramètres de Notifications
              </CardTitle>
              <CardDescription>
                Configuration des alertes et notifications
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>Notifications de stock</Label>
                    <p className="text-sm text-muted-foreground">
                      Recevoir des alertes quand le stock est bas
                    </p>
                  </div>
                  <Switch
                    checked={localSettings.stock_alerts !== false}
                    onCheckedChange={(checked) => handleSettingChange('stock_alerts', checked)}
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>Notifications de ventes</Label>
                    <p className="text-sm text-muted-foreground">
                      Recevoir des notifications pour les nouvelles ventes
                    </p>
                  </div>
                  <Switch
                    checked={localSettings.sales_notifications !== false}
                    onCheckedChange={(checked) => handleSettingChange('sales_notifications', checked)}
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>Notifications système</Label>
                    <p className="text-sm text-muted-foreground">
                      Recevoir des alertes système importantes
                    </p>
                  </div>
                  <Switch
                    checked={localSettings.system_alerts !== false}
                    onCheckedChange={(checked) => handleSettingChange('system_alerts', checked)}
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="notification_email">Email pour notifications</Label>
                <Input
                  id="notification_email"
                  type="email"
                  value={localSettings.notification_email || ''}
                  onChange={(e) => handleSettingChange('notification_email', e.target.value)}
                />
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="printing" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Printer className="h-5 w-5" />
                Paramètres d'Impression
              </CardTitle>
              <CardDescription>
                Configuration des imprimantes et formats
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-2">
                  <Label htmlFor="receipt_printer">Imprimante reçus</Label>
                  <Input
                    id="receipt_printer"
                    value={localSettings.receipt_printer || ''}
                    onChange={(e) => handleSettingChange('receipt_printer', e.target.value)}
                    placeholder="Nom de l'imprimante"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="report_printer">Imprimante rapports</Label>
                  <Input
                    id="report_printer"
                    value={localSettings.report_printer || ''}
                    onChange={(e) => handleSettingChange('report_printer', e.target.value)}
                    placeholder="Nom de l'imprimante"
                  />
                </div>
              </div>

              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>Impression automatique des reçus</Label>
                    <p className="text-sm text-muted-foreground">
                      Imprimer automatiquement après chaque vente
                    </p>
                  </div>
                  <Switch
                    checked={localSettings.auto_print_receipts === true}
                    onCheckedChange={(checked) => handleSettingChange('auto_print_receipts', checked)}
                  />
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="security" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Shield className="h-5 w-5" />
                Paramètres de Sécurité
              </CardTitle>
              <CardDescription>
                Configuration de la sécurité et des accès
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>Authentification à deux facteurs</Label>
                    <p className="text-sm text-muted-foreground">
                      Activer la 2FA pour plus de sécurité
                    </p>
                  </div>
                  <Switch
                    checked={localSettings.two_factor_auth === true}
                    onCheckedChange={(checked) => handleSettingChange('two_factor_auth', checked)}
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>Déconnexion automatique</Label>
                    <p className="text-sm text-muted-foreground">
                      Déconnecter après une période d'inactivité
                    </p>
                  </div>
                  <Switch
                    checked={localSettings.auto_logout !== false}
                    onCheckedChange={(checked) => handleSettingChange('auto_logout', checked)}
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="session_timeout">Délai de session (minutes)</Label>
                <Input
                  id="session_timeout"
                  type="number"
                  value={localSettings.session_timeout || 30}
                  onChange={(e) => handleSettingChange('session_timeout', parseInt(e.target.value))}
                />
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Boutons de sauvegarde globaux */}
      <div className="flex justify-end gap-2 pt-6 border-t">
        <Button variant="outline" onClick={handleResetSettings}>
          <RotateCcw className="h-4 w-4 mr-2" />
          Annuler les modifications
        </Button>
        <Button onClick={handleSaveSettings} disabled={updateSettings.isPending}>
          <Save className="h-4 w-4 mr-2" />
          Sauvegarder tous les paramètres
        </Button>
      </div>
    </div>
  );
}