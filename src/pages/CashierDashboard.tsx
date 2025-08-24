import { useState, useEffect, useMemo } from "react";
import { Sidebar } from "@/components/layout/Sidebar";
import { Header } from "@/components/layout/Header";
import { StatsCard } from "@/components/dashboard/StatsCard";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/stable-card";
import { Button } from "@/components/ui/button";
import {
  DollarSign,
  ShoppingCart,
  Clock,
  RefreshCw,
  Receipt,
  TrendingUp,
  Users,
  BarChart3
} from "lucide-react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from "recharts";
import { useSalesStats, useDashboardStats } from "@/hooks/use-api";
import { useToast } from "@/hooks/use-toast";
import { useAuth } from "@/hooks/use-auth";
import { SalesStats, DashboardStats } from "@/types/api";
import { ErrorBoundary } from "@/components/ErrorBoundary";
import { useNavigate } from "react-router-dom";

const CashierDashboard = () => {
  const { toast } = useToast();
  const { user } = useAuth();
  const navigate = useNavigate();
  
  // Hooks pour récupérer les données depuis l'API
  const {
    data: salesStats,
    isLoading: salesLoading,
    refetch: refetchSales
  } = useSalesStats();
  
  const {
    data: dashboardStats,
    isLoading: statsLoading,
    refetch: refetchStats
  } = useDashboardStats();

  // Mémorisation des données de ventes pour éviter les re-rendus inutiles
  const formattedSalesData = useMemo(() => {
    if ((salesStats as SalesStats)?.hourly_sales) {
      return (salesStats as SalesStats).hourly_sales!.map((item) => ({
        time: `${item.hour}:00`,
        sales: item.total_amount || 0
      }));
    }
    return [];
  }, [salesStats]);

  // Mémorisation des données des produits les plus vendus
  const formattedTopProducts = useMemo(() => {
    if ((salesStats as SalesStats)?.top_products) {
      return (salesStats as SalesStats).top_products!.slice(0, 5).map((item) => ({
        name: item.product_name,
        sales: item.quantity_sold || item.sales || 0
      }));
    }
    return [];
  }, [salesStats]);

  // Statistiques spécifiques au caissier
  const cashierStats = useMemo(() => {
    const stats = dashboardStats as DashboardStats;
    const sales = salesStats as SalesStats;
    
    return {
      todaySales: stats?.today_sales || stats?.today?.revenue || 0,
      todayOrders: stats?.today?.sales || 0,
      avgOrderValue: stats?.today?.revenue && stats?.today?.sales ? 
        Math.round(stats.today.revenue / stats.today.sales) : 0,
      completedSales: stats?.today?.sales || 0,
      pendingSales: stats?.today?.pending_sales || stats?.pending_orders || 0,
      salesChange: stats?.sales_change || "0%",
      salesChangeType: stats?.sales_change_type || "neutral"
    };
  }, [dashboardStats, salesStats]);

  // Fonction pour actualiser les données
  const handleRefresh = () => {
    refetchStats();
    refetchSales();
    toast({
      title: "Actualisation",
      description: "Données actualisées avec succès"
    });
  };

  // Actions rapides pour le caissier
  const quickActions = [
    {
      title: "Nouvelle Vente",
      description: "Créer une nouvelle vente",
      icon: ShoppingCart,
      action: () => navigate("/sales"),
      color: "bg-green-500 hover:bg-green-600"
    },
    {
      title: "Historique",
      description: "Voir l'historique des ventes",
      icon: Receipt,
      action: () => navigate("/sales-history"),
      color: "bg-blue-500 hover:bg-blue-600"
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-surface flex">
      <Sidebar />
      
      <div className="flex-1 flex flex-col">
        <Header />
        
        <main className="flex-1 p-6 space-y-6">
          {/* Welcome Section */}
          <div className="bg-gradient-to-r from-green-600 to-green-700 rounded-xl p-6 text-white">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold mb-2">
                  Tableau de Bord Caissier
                </h1>
                <p className="text-green-100 text-lg">
                  Bonjour {user?.first_name || user?.username} ! Gérez vos ventes efficacement
                </p>
              </div>
              <Button 
                variant="secondary" 
                onClick={handleRefresh}
                className="gap-2"
                disabled={statsLoading || salesLoading}
              >
                <RefreshCw className={`h-4 w-4 ${(statsLoading || salesLoading) ? 'animate-spin' : ''}`} />
                Actualiser
              </Button>
            </div>
          </div>

          {/* Stats Grid - Spécifiques au caissier */}
          <ErrorBoundary>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {statsLoading ? (
                <>
                  <div className="h-32 bg-muted animate-pulse rounded-lg" />
                  <div className="h-32 bg-muted animate-pulse rounded-lg" />
                  <div className="h-32 bg-muted animate-pulse rounded-lg" />
                  <div className="h-32 bg-muted animate-pulse rounded-lg" />
                </>
              ) : (
                <>
                  <StatsCard
                    title="Ventes du jour"
                    value={`${cashierStats.todaySales.toLocaleString()} FBu`}
                    change={cashierStats.salesChange}
                    changeType={cashierStats.salesChangeType}
                    icon={DollarSign}
                    description="total aujourd'hui"
                  />
                  <StatsCard
                    title="Commandes"
                    value={cashierStats.todayOrders.toString()}
                    change={`${cashierStats.completedSales} terminées`}
                    changeType="positive"
                    icon={ShoppingCart}
                    description={`${cashierStats.pendingSales} en cours`}
                  />
                  <StatsCard
                    title="Panier moyen"
                    value={`${cashierStats.avgOrderValue.toLocaleString()} FBu`}
                    change="Aujourd'hui"
                    changeType="neutral"
                    icon={TrendingUp}
                    description="par commande"
                  />
                  <StatsCard
                    title="Performance"
                    value={`${cashierStats.completedSales}`}
                    change={`${Math.round((cashierStats.completedSales / (cashierStats.completedSales + cashierStats.pendingSales || 1)) * 100)}%`}
                    changeType="positive"
                    icon={Users}
                    description="taux de réussite"
                  />
                </>
              )}
            </div>
          </ErrorBoundary>

          {/* Actions rapides et graphiques */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Actions rapides */}
            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Clock className="h-5 w-5" />
                    Actions Rapides
                  </CardTitle>
                  <CardDescription>
                    Accès direct aux fonctions principales
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  {quickActions.map((action, index) => (
                    <Button
                      key={index}
                      onClick={action.action}
                      className={`w-full justify-start gap-3 h-auto p-4 ${action.color} text-white`}
                    >
                      <action.icon className="h-5 w-5" />
                      <div className="text-left">
                        <div className="font-semibold">{action.title}</div>
                        <div className="text-sm opacity-90">{action.description}</div>
                      </div>
                    </Button>
                  ))}
                </CardContent>
              </Card>

              {/* Résumé rapide */}
              <Card>
                <CardHeader>
                  <CardTitle>Résumé du jour</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-muted-foreground">Ventes terminées</span>
                      <span className="font-semibold text-green-600">{cashierStats.completedSales}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-muted-foreground">En cours</span>
                      <span className="font-semibold text-orange-600">{cashierStats.pendingSales}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-muted-foreground">Chiffre d'affaires</span>
                      <span className="font-semibold text-blue-600">{cashierStats.todaySales.toLocaleString()} FBu</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Graphiques */}
            <div className="lg:col-span-2 space-y-6">
              {/* Évolution des ventes */}
              <ErrorBoundary>
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <BarChart3 className="h-5 w-5" />
                      Évolution des ventes
                    </CardTitle>
                    <CardDescription>
                      Ventes par heure aujourd'hui
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    {salesLoading ? (
                      <div className="h-[300px] w-full animate-pulse bg-muted rounded" />
                    ) : formattedSalesData.length > 0 ? (
                      <ResponsiveContainer width="100%" height={300}>
                        <LineChart data={formattedSalesData}>
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="time" />
                          <YAxis />
                          <Tooltip formatter={(value) => [`${value} FBu`, "Ventes"]} />
                          <Line type="monotone" dataKey="sales" stroke="#16a34a" strokeWidth={2} />
                        </LineChart>
                      </ResponsiveContainer>
                    ) : (
                      <div className="flex items-center justify-center h-[300px] text-muted-foreground">
                        <div className="text-center">
                          <BarChart3 className="h-12 w-12 mx-auto mb-4 opacity-50" />
                          <p>Aucune vente enregistrée</p>
                          <p className="text-sm">Commencez à vendre pour voir les statistiques</p>
                        </div>
                      </div>
                    )}
                  </CardContent>
                </Card>
              </ErrorBoundary>

              {/* Top produits */}
              <ErrorBoundary>
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <TrendingUp className="h-5 w-5" />
                      Produits populaires
                    </CardTitle>
                    <CardDescription>
                      Top 5 des ventes aujourd'hui
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    {salesLoading ? (
                      <div className="h-[250px] w-full animate-pulse bg-muted rounded" />
                    ) : formattedTopProducts.length > 0 ? (
                      <ResponsiveContainer width="100%" height={250}>
                        <BarChart data={formattedTopProducts}>
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="name" />
                          <YAxis />
                          <Tooltip formatter={(value) => [`${value}`, "Vendus"]} />
                          <Bar dataKey="sales" fill="#16a34a" />
                        </BarChart>
                      </ResponsiveContainer>
                    ) : (
                      <div className="flex items-center justify-center h-[250px] text-muted-foreground">
                        <div className="text-center">
                          <TrendingUp className="h-12 w-12 mx-auto mb-4 opacity-50" />
                          <p>Aucun produit vendu</p>
                          <p className="text-sm">Les produits populaires apparaîtront ici</p>
                        </div>
                      </div>
                    )}
                  </CardContent>
                </Card>
              </ErrorBoundary>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default CashierDashboard;
