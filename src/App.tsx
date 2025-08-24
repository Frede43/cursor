import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryProvider } from "@/providers/QueryProvider";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { NotificationProvider } from "./hooks/use-notifications";
import { AuthProvider } from "./hooks/use-auth-dynamic";
import { ProtectedRoute } from "./components/auth/ProtectedRoute-dynamic";
import Index from "./pages/Index.tsx";
import Login from "./pages/Login.tsx";
import Profile from "./pages/Profile.tsx";
import Products from "./pages/Products.tsx";
import Sales from "./pages/Sales.tsx";
import SalesHistory from "./pages/SalesHistory.tsx";
import Users from "./pages/Users.tsx";
import Stocks from "./pages/Stocks.tsx";
import Kitchen from "./pages/Kitchen.tsx";
import Reports from "./pages/Reports.tsx";
import Settings from "./pages/Settings.tsx";
import AccessDenied from "./pages/AccessDenied.tsx";
import Tables from "./pages/Tables";
import Orders from "./pages/Orders";
import Suppliers from "./pages/Suppliers";
import Supplies from "./pages/Supplies";
import Expenses from "./pages/Expenses";
import DailyReport from "./pages/DailyReport";
import Analytics from "./pages/Analytics";
import Alerts from "./pages/Alerts";
import Monitoring from "./pages/Monitoring";
import Help from "./pages/Help";
import Dashboard from "./pages/Dashboard";
import NotFound from "./pages/NotFound";
import { BottomNotificationProvider } from "./components/notifications/BottomNotificationProvider";

const App = () => (
  <QueryProvider>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <AuthProvider>
          <NotificationProvider>
            <BottomNotificationProvider>
              <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/" element={
              <ProtectedRoute requiredPermissions={['dashboard.view']} accessDeniedComponent={<AccessDenied />}>
                <Index />
              </ProtectedRoute>
            } />
            <Route path="/dashboard" element={
              <ProtectedRoute requiredPermissions={['dashboard.view']} accessDeniedComponent={<AccessDenied />}>
                <Index />
              </ProtectedRoute>
            } />
            <Route path="/profile" element={
              <ProtectedRoute>
                <Profile />
              </ProtectedRoute>
            } />
            <Route path="/products" element={
              <ProtectedRoute requiredPermissions={['products.view']}>
                <Products />
              </ProtectedRoute>
            } />
            <Route path="/sales" element={
              <ProtectedRoute requiredPermissions={['sales.view']}>
                <Sales />
              </ProtectedRoute>
            } />
            <Route path="/stocks" element={
              <ProtectedRoute requiredPermissions={['stocks.view']}>
                <Stocks />
              </ProtectedRoute>
            } />
            <Route path="/stock-sync" element={
              <ProtectedRoute requiredPermissions={['stocks.view']}>
                <Stocks />
              </ProtectedRoute>
            } />
            <Route path="/supplies" element={
              <ProtectedRoute requiredPermissions={['supplies.view']}>
                <Supplies />
              </ProtectedRoute>
            } />
            <Route path="/kitchen" element={
              <ProtectedRoute requiredPermissions={['kitchen.view']}>
                <Kitchen />
              </ProtectedRoute>
            } />
            <Route path="/sales-history" element={
              <ProtectedRoute requiredPermissions={['finances.history']}>
                <SalesHistory />
              </ProtectedRoute>
            } />
            <Route path="/daily-report" element={
              <ProtectedRoute requiredPermissions={['reports.view']}>
                <DailyReport />
              </ProtectedRoute>
            } />
            <Route path="/reports" element={
              <ProtectedRoute requiredPermissions={['reports.view']}>
                <Reports />
              </ProtectedRoute>
            } />
            <Route path="/analytics" element={
              <ProtectedRoute requiredPermissions={['analytics.view']}>
                <Analytics />
              </ProtectedRoute>
            } />
            <Route path="/tables" element={
              <ProtectedRoute requiredPermissions={['tables.view']}>
                <Tables />
              </ProtectedRoute>
            } />
            <Route path="/orders" element={
              <ProtectedRoute requiredPermissions={['orders.view']}>
                <Orders />
              </ProtectedRoute>
            } />
            <Route path="/users" element={
              <ProtectedRoute requiredPermissions={['users.view']}>
                <Users />
              </ProtectedRoute>
            } />
            <Route path="/suppliers" element={
              <ProtectedRoute requiredPermissions={['suppliers.view']}>
                <Suppliers />
              </ProtectedRoute>
            } />
            <Route path="/expenses" element={
              <ProtectedRoute requiredPermissions={['expenses.view']}>
                <Expenses />
              </ProtectedRoute>
            } />
            <Route path="/settings" element={
              <ProtectedRoute requiredPermissions={['settings.view']}>
                <Settings />
              </ProtectedRoute>
            } />
            <Route path="/alerts" element={
              <ProtectedRoute requiredPermissions={['alerts.view']}>
                <Alerts />
              </ProtectedRoute>
            } />
            <Route path="/monitoring" element={
              <ProtectedRoute requiredPermissions={['monitoring.view']}>
                <Monitoring />
              </ProtectedRoute>
            } />
            <Route path="/help" element={
              <ProtectedRoute>
                <Help />
              </ProtectedRoute>
            } />
            <Route path="*" element={<NotFound />} />
              </Routes>
            </BottomNotificationProvider>
          </NotificationProvider>
        </AuthProvider>
      </BrowserRouter>
    </TooltipProvider>
  </QueryProvider>
);

export default App;
