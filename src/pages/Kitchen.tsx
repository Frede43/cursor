import React, { useState, useEffect } from "react";
import { Sidebar } from "@/components/layout/Sidebar";
import { Header } from "@/components/layout/Header";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Progress } from "@/components/ui/progress";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { useToast } from "@/hooks/use-toast";
import {
  ChefHat,
  AlertTriangle,
  Package,
  DollarSign,
  Clock,
  TrendingUp,
  ShoppingCart,
  BarChart3,
  Utensils,
  RefreshCw,
  Plus,
  Edit,
  Trash2
} from "lucide-react";
import { useKitchenDashboard, useIngredients, useCreateIngredient, useSuppliers } from "@/hooks/use-api";
import { formatNumber, formatQuantity, formatUnitPrice } from "@/utils/formatters";

interface StockAlert {
  ingredient: string;
  current_stock: number;
  minimum_stock: number;
  unit: string;
  severity: 'critical' | 'warning';
}

interface ProductionForecast {
  recipe: string;
  max_portions: number;
  limiting_ingredient: string;
  cost_per_portion: number;
  prep_time: number;
}

interface KitchenData {
  stock_alerts: StockAlert[];
  production_forecast: ProductionForecast[];
  shopping_list: any[];
  profitability_analysis: any[];
  stock_value: {
    total_stock_value: number;
    items: any[];
  };
  summary: {
    critical_alerts: number;
    warning_alerts: number;
    total_stock_value: number;
    items_to_buy: number;
  };
}

export default function Kitchen() {
  const { toast } = useToast();
  const [showAddIngredient, setShowAddIngredient] = useState(false);
  const [newIngredient, setNewIngredient] = useState({
    nom: "",
    quantite_restante: "",
    unite: "kg",
    seuil_alerte: "",
    prix_unitaire: "",
    description: "",
    fournisseur: ""
  });

  // Hooks API
  const { data: kitchenData, isLoading: loading, refetch: refetchKitchen } = useKitchenDashboard();
  const { data: ingredientsData, refetch: refetchIngredients } = useIngredients();
  const { data: suppliersData } = useSuppliers();
  const createIngredientMutation = useCreateIngredient();

  // Calculer les statistiques réelles à partir des ingrédients
  const realStats = React.useMemo(() => {
    if (!ingredientsData || !Array.isArray((ingredientsData as any)?.results)) {
      return {
        critical_alerts: 0,
        warning_alerts: 0,
        total_stock_value: 0,
        items_to_buy: 0,
        stock_alerts: [],
        shopping_list: []
      };
    }

    const ingredients = (ingredientsData as any).results;
    let critical_alerts = 0;
    let warning_alerts = 0;
    let total_stock_value = 0;
    let items_to_buy = 0;
    const stock_alerts: any[] = [];
    const shopping_list: any[] = [];

    ingredients.forEach((ingredient: any) => {
      const quantity = parseFloat(ingredient.quantite_restante);
      const threshold = parseFloat(ingredient.seuil_alerte);
      const price = parseFloat(ingredient.prix_unitaire);

      // Calculer la valeur du stock
      total_stock_value += quantity * price;

      // Vérifier les alertes
      if (quantity <= 0) {
        critical_alerts++;
        stock_alerts.push({
          type: 'critical',
          ingredient: ingredient.nom,
          current_stock: quantity,
          threshold: threshold,
          unit: ingredient.unite,
          message: `Rupture de stock: ${ingredient.nom}`
        });
        shopping_list.push({
          ingredient: ingredient.nom,
          needed_quantity: threshold * 2, // Recommander 2x le seuil
          unit: ingredient.unite,
          estimated_cost: threshold * 2 * price,
          priority: 'high'
        });
        items_to_buy++;
      } else if (quantity <= threshold) {
        warning_alerts++;
        stock_alerts.push({
          type: 'warning',
          ingredient: ingredient.nom,
          current_stock: quantity,
          threshold: threshold,
          unit: ingredient.unite,
          message: `Stock faible: ${ingredient.nom} (${quantity} ${ingredient.unite})`
        });
        shopping_list.push({
          ingredient: ingredient.nom,
          needed_quantity: threshold - quantity + threshold, // Compléter + réserve
          unit: ingredient.unite,
          estimated_cost: (threshold - quantity + threshold) * price,
          priority: 'medium'
        });
        items_to_buy++;
      }
    });

    return {
      critical_alerts,
      warning_alerts,
      total_stock_value,
      items_to_buy,
      stock_alerts,
      shopping_list
    };
  }, [ingredientsData]);

  // Fonction pour recalculer automatiquement les prix d'achat
  const handleRecalculatePrices = async () => {
    try {
      const response = await fetch('/api/kitchen/recalculate-purchase-prices/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const result = await response.json();
        toast({
          title: "Recalcul réussi !",
          description: `${result.summary.products_updated} produits mis à jour avec les coûts réels des ingrédients`,
          variant: "default",
        });

        // Actualiser les données
        refetchKitchen();
        refetchIngredients();
      } else {
        throw new Error('Erreur lors du recalcul');
      }
    } catch (error) {
      toast({
        title: "Erreur",
        description: "Impossible de recalculer les prix automatiquement",
        variant: "destructive",
      });
    }
  };

  // Fonctions de gestion du formulaire
  const handleCreateIngredient = async () => {
    try {
      await createIngredientMutation.mutateAsync({
        nom: newIngredient.nom,
        quantite_restante: parseFloat(newIngredient.quantite_restante) || 0,
        unite: newIngredient.unite,
        seuil_alerte: parseFloat(newIngredient.seuil_alerte) || 1,
        prix_unitaire: parseFloat(newIngredient.prix_unitaire) || 0,
        description: newIngredient.description,
        fournisseur: newIngredient.fournisseur ? parseInt(newIngredient.fournisseur) : null
      });

      // Réinitialiser le formulaire
      setNewIngredient({
        nom: "",
        quantite_restante: "",
        unite: "kg",
        seuil_alerte: "",
        prix_unitaire: "",
        description: "",
        fournisseur: ""
      });
      setShowAddIngredient(false);
    } catch (error) {
      console.error('Erreur création ingrédient:', error);
    }
  };

  const refreshData = () => {
    refetchKitchen();
    refetchIngredients();
  };

  if (loading) {
    return (
      <div className="flex h-screen bg-background">
        <Sidebar />
        <div className="flex-1 flex flex-col overflow-hidden">
          <Header />
          <main className="flex-1 p-6 flex items-center justify-center">
            <div className="text-center">
              <Clock className="h-12 w-12 animate-spin mx-auto mb-4" />
              <p>Chargement des données de cuisine...</p>
            </div>
          </main>
        </div>
      </div>
    );
  }

  if (!kitchenData) {
    return (
      <div className="flex h-screen bg-background">
        <Sidebar />
        <div className="flex-1 flex flex-col overflow-hidden">
          <Header />
          <main className="flex-1 p-6 flex items-center justify-center">
            <div className="text-center">
              <AlertTriangle className="h-12 w-12 text-destructive mx-auto mb-4" />
              <p>Erreur de chargement des données</p>
              <Button onClick={() => {
                refetchKitchen();
                refetchIngredients();
              }} className="mt-4">
                Réessayer
              </Button>
            </div>
          </main>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-background">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />
        <main className="flex-1 p-6 overflow-y-auto">
          <div className="space-y-6">
            
            {/* En-tête */}
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold flex items-center gap-2">
                  <ChefHat className="h-8 w-8" />
                  Gestion de Cuisine
                </h1>
                <p className="text-muted-foreground">Interface technique complète</p>
              </div>
              <div className="flex gap-2">
                <Button onClick={refreshData} variant="outline">
                  <RefreshCw className="h-4 w-4 mr-2" />
                  Actualiser
                </Button>
                <Button onClick={handleRecalculatePrices} variant="outline" className="bg-blue-50 hover:bg-blue-100 border-blue-200">
                  <DollarSign className="h-4 w-4 mr-2" />
                  Recalculer Prix
                </Button>
                <Dialog open={showAddIngredient} onOpenChange={setShowAddIngredient}>
                  <DialogTrigger asChild>
                    <Button>
                      <Plus className="h-4 w-4 mr-2" />
                      Ajouter Ingrédient
                    </Button>
                  </DialogTrigger>
                  <DialogContent className="max-w-md">
                    <DialogHeader>
                      <DialogTitle>Nouvel Ingrédient</DialogTitle>
                      <DialogDescription>
                        Ajouter un nouvel ingrédient au stock cuisine
                      </DialogDescription>
                    </DialogHeader>

                    <div className="space-y-4">
                      <div className="space-y-2">
                        <Label htmlFor="nom">Nom de l'ingrédient *</Label>
                        <Input
                          id="nom"
                          value={newIngredient.nom}
                          onChange={(e) => setNewIngredient(prev => ({...prev, nom: e.target.value}))}
                          placeholder="Ex: Tomates, Oignons..."
                        />
                      </div>

                      <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <Label htmlFor="quantite">Quantité initiale *</Label>
                          <Input
                            id="quantite"
                            type="number"
                            step="0.001"
                            value={newIngredient.quantite_restante}
                            onChange={(e) => setNewIngredient(prev => ({...prev, quantite_restante: e.target.value}))}
                            placeholder="0.000"
                          />
                        </div>
                        <div className="space-y-2">
                          <Label htmlFor="unite">Unité *</Label>
                          <Select value={newIngredient.unite} onValueChange={(value) => setNewIngredient(prev => ({...prev, unite: value}))}>
                            <SelectTrigger>
                              <SelectValue />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="kg">Kilogramme</SelectItem>
                              <SelectItem value="g">Gramme</SelectItem>
                              <SelectItem value="L">Litre</SelectItem>
                              <SelectItem value="ml">Millilitre</SelectItem>
                              <SelectItem value="piece">Pièce</SelectItem>
                              <SelectItem value="portion">Portion</SelectItem>
                            </SelectContent>
                          </Select>
                        </div>
                      </div>

                      <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <Label htmlFor="seuil">Seuil d'alerte</Label>
                          <Input
                            id="seuil"
                            type="number"
                            step="0.001"
                            value={newIngredient.seuil_alerte}
                            onChange={(e) => setNewIngredient(prev => ({...prev, seuil_alerte: e.target.value}))}
                            placeholder="1.000"
                          />
                        </div>
                        <div className="space-y-2">
                          <Label htmlFor="prix">Prix unitaire (BIF)</Label>
                          <Input
                            id="prix"
                            type="number"
                            step="0.01"
                            value={newIngredient.prix_unitaire}
                            onChange={(e) => setNewIngredient(prev => ({...prev, prix_unitaire: e.target.value}))}
                            placeholder="0.00"
                          />
                        </div>
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="fournisseur">Fournisseur</Label>
                        <Select value={newIngredient.fournisseur} onValueChange={(value) => setNewIngredient(prev => ({...prev, fournisseur: value}))}>
                          <SelectTrigger>
                            <SelectValue placeholder="Sélectionner un fournisseur" />
                          </SelectTrigger>
                          <SelectContent>
                            {suppliersData?.results?.map((supplier: any) => (
                              <SelectItem key={supplier.id} value={supplier.id.toString()}>
                                {supplier.name}
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="description">Description</Label>
                        <Textarea
                          id="description"
                          value={newIngredient.description}
                          onChange={(e) => setNewIngredient(prev => ({...prev, description: e.target.value}))}
                          placeholder="Description optionnelle..."
                          rows={3}
                        />
                      </div>

                      <div className="flex justify-end gap-2">
                        <Button variant="outline" onClick={() => setShowAddIngredient(false)}>
                          Annuler
                        </Button>
                        <Button
                          onClick={handleCreateIngredient}
                          disabled={!newIngredient.nom || createIngredientMutation.isPending}
                        >
                          {createIngredientMutation.isPending ? (
                            <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                          ) : (
                            <Plus className="h-4 w-4 mr-2" />
                          )}
                          Créer
                        </Button>
                      </div>
                    </div>
                  </DialogContent>
                </Dialog>
              </div>
            </div>

            {/* Statistiques rapides */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <Card>
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-muted-foreground">Alertes Critiques</p>
                      <p className="text-2xl font-bold text-destructive">
                        {realStats.critical_alerts}
                      </p>
                    </div>
                    <AlertTriangle className="h-8 w-8 text-destructive" />
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-muted-foreground">Alertes Stock</p>
                      <p className="text-2xl font-bold text-orange-500">
                        {realStats.warning_alerts}
                      </p>
                    </div>
                    <Package className="h-8 w-8 text-orange-500" />
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-muted-foreground">Valeur Stock</p>
                      <p className="text-2xl font-bold text-green-600">
                        {realStats.total_stock_value.toLocaleString()} BIF
                      </p>
                    </div>
                    <DollarSign className="h-8 w-8 text-green-600" />
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-muted-foreground">À Acheter</p>
                      <p className="text-2xl font-bold text-blue-600">
                        {realStats.items_to_buy}
                      </p>
                    </div>
                    <ShoppingCart className="h-8 w-8 text-blue-600" />
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Onglets principaux */}
            <Tabs defaultValue="ingredients" className="space-y-4">
              <TabsList className="grid w-full grid-cols-5">
                <TabsTrigger value="ingredients" className="flex items-center gap-2">
                  <Package className="h-4 w-4" />
                  Ingrédients
                </TabsTrigger>
                <TabsTrigger value="alerts" className="flex items-center gap-2">
                  <AlertTriangle className="h-4 w-4" />
                  Alertes Stock
                </TabsTrigger>
                <TabsTrigger value="production" className="flex items-center gap-2">
                  <Utensils className="h-4 w-4" />
                  Production
                </TabsTrigger>
                <TabsTrigger value="profitability" className="flex items-center gap-2">
                  <TrendingUp className="h-4 w-4" />
                  Rentabilité
                </TabsTrigger>
                <TabsTrigger value="shopping" className="flex items-center gap-2">
                  <ShoppingCart className="h-4 w-4" />
                  Achats
                </TabsTrigger>
              </TabsList>

              {/* Onglet Alertes Stock */}

              {/* Onglet Ingrédients */}
              <TabsContent value="ingredients" className="space-y-4">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Package className="h-5 w-5" />
                      Stock des Ingrédients
                    </CardTitle>
                    <CardDescription>
                      Gérez votre stock d'ingrédients de cuisine
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    {(ingredientsData as any)?.results ? (
                      <div className="space-y-4">
                        {(ingredientsData as any)?.results?.map((ingredient: any) => (
                          <div key={ingredient.id} className="flex items-center justify-between p-4 border rounded-lg">
                            <div className="flex items-center gap-4">
                              <div className="h-12 w-12 bg-gradient-to-br from-green-500 to-green-600 rounded-lg flex items-center justify-center">
                                <Package className="h-6 w-6 text-white" />
                              </div>
                              <div>
                                <h3 className="font-semibold">{ingredient.nom}</h3>
                                <div className="flex items-center gap-4 text-sm text-muted-foreground">
                                  <span>Stock: {formatQuantity(ingredient.quantite_restante, ingredient.unite)}</span>
                                  <span>Seuil: {formatQuantity(ingredient.seuil_alerte, ingredient.unite)}</span>
                                  <span>Prix: {formatUnitPrice(ingredient.prix_unitaire, ingredient.unite)}</span>
                                </div>
                              </div>
                            </div>
                            <div className="flex items-center gap-2">
                              <Badge
                                variant={
                                  ingredient.quantite_restante <= 0 ? "destructive" :
                                  ingredient.quantite_restante <= ingredient.seuil_alerte ? "warning" :
                                  "success"
                                }
                              >
                                {ingredient.quantite_restante <= 0 ? "Rupture" :
                                 ingredient.quantite_restante <= ingredient.seuil_alerte ? "Stock faible" :
                                 "OK"}
                              </Badge>
                              <Button variant="outline" size="sm">
                                <Edit className="h-4 w-4" />
                              </Button>
                            </div>
                          </div>
                        ))}

                        {(ingredientsData as any)?.results?.length === 0 && (
                          <div className="text-center py-8">
                            <Package className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                            <p className="text-muted-foreground">Aucun ingrédient trouvé</p>
                            <p className="text-sm text-muted-foreground">Commencez par ajouter des ingrédients à votre stock</p>
                          </div>
                        )}
                      </div>
                    ) : (
                      <div className="flex items-center justify-center py-8">
                        <RefreshCw className="h-6 w-6 animate-spin mr-2" />
                        Chargement des ingrédients...
                      </div>
                    )}
                  </CardContent>
                </Card>
              </TabsContent>
              <TabsContent value="alerts" className="space-y-4">
                <Card>
                  <CardHeader>
                    <CardTitle>Alertes de Stock</CardTitle>
                    <CardDescription>
                      Ingrédients nécessitant un réapprovisionnement
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    {realStats.stock_alerts.length === 0 ? (
                      <div className="text-center py-8">
                        <Package className="h-12 w-12 text-green-500 mx-auto mb-4" />
                        <p className="text-lg font-semibold text-green-600">Tous les stocks sont OK !</p>
                        <p className="text-muted-foreground">Aucune alerte de stock actuellement</p>
                      </div>
                    ) : (
                      <div className="space-y-3">
                        {realStats.stock_alerts.map((alert, index) => (
                          <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                            <div className="flex items-center gap-3">
                              <div className={`w-3 h-3 rounded-full ${
                                alert.type === 'critical' ? 'bg-red-500' : 'bg-orange-500'
                              }`} />
                              <div>
                                <h4 className="font-medium">{alert.ingredient}</h4>
                                <p className="text-sm text-muted-foreground">
                                  Stock: {formatQuantity(alert.current_stock, alert.unit)} / Seuil: {formatQuantity(alert.threshold, alert.unit)}
                                </p>
                              </div>
                            </div>
                            <div className="text-right">
                              <Badge variant={alert.type === 'critical' ? 'destructive' : 'secondary'}>
                                {alert.type === 'critical' ? 'Critique' : 'Attention'}
                              </Badge>
                              <p className="text-xs text-muted-foreground mt-1">
                                Seuil: {formatQuantity(alert.threshold, alert.unit)}
                              </p>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </CardContent>
                </Card>
              </TabsContent>

              {/* Onglet Production */}
              <TabsContent value="production" className="space-y-4">
                <Card>
                  <CardHeader>
                    <CardTitle>Prévisions de Production</CardTitle>
                    <CardDescription>
                      Capacité de production basée sur les stocks actuels
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {((kitchenData as any)?.production_forecast || []).map((forecast: any, index: number) => (
                        <div key={index} className="p-4 border rounded-lg">
                          <div className="flex items-center justify-between mb-3">
                            <h4 className="font-semibold text-lg">{forecast.recipe}</h4>
                            <Badge variant="outline">
                              {forecast.max_portions} portions possibles
                            </Badge>
                          </div>
                          
                          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                            <div>
                              <p className="text-muted-foreground">Coût par portion</p>
                              <p className="font-medium">{forecast.cost_per_portion.toLocaleString()} BIF</p>
                            </div>
                            <div>
                              <p className="text-muted-foreground">Temps de préparation</p>
                              <p className="font-medium">{forecast.prep_time} minutes</p>
                            </div>
                            <div>
                              <p className="text-muted-foreground">Ingrédient limitant</p>
                              <p className="font-medium text-orange-600">{forecast.limiting_ingredient}</p>
                            </div>
                          </div>
                          
                          <div className="mt-3">
                            <div className="flex justify-between text-xs mb-1">
                              <span>Capacité de production</span>
                              <span>{forecast.max_portions} / 50 portions</span>
                            </div>
                            <Progress value={(forecast.max_portions / 50) * 100} className="h-2" />
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              {/* Onglet Rentabilité */}
              <TabsContent value="profitability" className="space-y-4">
                <Card>
                  <CardHeader>
                    <CardTitle>Analyse de Rentabilité</CardTitle>
                    <CardDescription>
                      Marges et rentabilité des articles du menu
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {((kitchenData as any)?.profitability_analysis || []).slice(0, 10).map((item: any, index: number) => (
                        <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                          <div>
                            <h4 className="font-medium">{item.item}</h4>
                            <p className="text-sm text-muted-foreground">{item.category}</p>
                          </div>
                          <div className="text-right">
                            <div className="flex items-center gap-4">
                              <div>
                                <p className="text-sm text-muted-foreground">Prix de vente</p>
                                <p className="font-medium">{item.selling_price.toLocaleString()} BIF</p>
                              </div>
                              <div>
                                <p className="text-sm text-muted-foreground">Coût</p>
                                <p className="font-medium">{item.cost_price.toLocaleString()} BIF</p>
                              </div>
                              <div>
                                <p className="text-sm text-muted-foreground">Marge</p>
                                <Badge variant={item.margin_percentage > 50 ? 'default' : 'secondary'}>
                                  {item.margin_percentage.toFixed(1)}%
                                </Badge>
                              </div>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              {/* Onglet Liste d'Achats */}
              <TabsContent value="shopping" className="space-y-4">
                <Card>
                  <CardHeader>
                    <CardTitle>Liste de Courses</CardTitle>
                    <CardDescription>
                      Ingrédients à commander pour maintenir les stocks
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    {realStats.shopping_list.length === 0 ? (
                      <div className="text-center py-8">
                        <ShoppingCart className="h-12 w-12 text-green-500 mx-auto mb-4" />
                        <p className="text-lg font-semibold text-green-600">Aucun achat nécessaire !</p>
                        <p className="text-muted-foreground">Tous les stocks sont suffisants</p>
                      </div>
                    ) : (
                      <div className="space-y-3">
                        {realStats.shopping_list.map((item, index) => (
                          <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                            <div>
                              <h4 className="font-medium">{item.ingredient}</h4>
                              <p className="text-sm text-muted-foreground">
                                Priorité: {item.priority === 'high' ? 'Haute' : item.priority === 'medium' ? 'Moyenne' : 'Basse'}
                              </p>
                            </div>
                            <div className="text-right">
                              <p className="font-medium">
                                {formatQuantity(item.needed_quantity, item.unit)}
                              </p>
                              <p className="text-sm text-muted-foreground">
                                ~{formatNumber(item.estimated_cost).toLocaleString()} BIF
                              </p>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          </div>
        </main>
      </div>
    </div>
  );
}
