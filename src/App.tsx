import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryProvider } from "@/providers/QueryProvider";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useAuth, AuthProvider } from '@/hooks/use-auth';
import { NotificationProvider } from "./hooks/use-notifications";
import ProtectedRoute from "./components/auth/ProtectedRoute";
import Index from "./pages/Index";
import Login from "./pages/Login";
import Products from "./pages/Products";
import Profile from "./pages/Profile";
import Sales from "./pages/Sales";
import Stocks from "./pages/Stocks";
import StockSync from "./pages/StockSync";
import Supplies from "./pages/Supplies";
import SalesHistory from "./pages/SalesHistory";
import DailyReport from "./pages/DailyReport";
import Reports from "./pages/Reports";
import Analytics from "./pages/Analytics";
import Tables from "./pages/Tables";
import Orders from "./pages/Orders";
import Users from "./pages/Users";
import Suppliers from "./pages/Suppliers";
import Expenses from "./pages/Expenses";
import Settings from "./pages/Settings";
import Alerts from "./pages/Alerts";
import Monitoring from "./pages/Monitoring";
import Help from "./pages/Help";
import Kitchen from "./pages/Kitchen";
import Dashboard from "./pages/Dashboard";
import NotFound from "./pages/NotFound";

const App = () => (
  <QueryProvider>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <AuthProvider>
          <NotificationProvider>
          <Routes>
          <Route path="/login" element={<Login />} />
          
          {/* Protected Routes */}
          <Route path="/" element={<ProtectedRoute requiredPermissions={['dashboard.view']}><Index /></ProtectedRoute>} />
          <Route path="/dashboard" element={<ProtectedRoute requiredPermissions={['dashboard.view']}><Index /></ProtectedRoute>} />

          {/* Authentication & Profile */}
          <Route path="/profile" element={<ProtectedRoute requiredPermissions={['profile.view']}><Profile /></ProtectedRoute>} />
          <Route path="/products" element={<ProtectedRoute requiredPermissions={['products.view']}><Products /></ProtectedRoute>} />
          <Route path="/sales" element={<ProtectedRoute requiredPermissions={['sales.view']}><Sales /></ProtectedRoute>} />

          {/* Stock Management */}
          <Route path="/stocks" element={<ProtectedRoute requiredPermissions={['stocks.view']}><Stocks /></ProtectedRoute>} />
          <Route path="/stock-sync" element={<ProtectedRoute requiredPermissions={['stocks.manage']}><StockSync /></ProtectedRoute>} />
          <Route path="/supplies" element={<ProtectedRoute requiredPermissions={['stocks.manage']}><Supplies /></ProtectedRoute>} />
          <Route path="/kitchen" element={<ProtectedRoute><Kitchen /></ProtectedRoute>} />

          {/* Financial & Reports */}
          <Route path="/sales-history" element={<ProtectedRoute requiredPermissions={['finances.history']}><SalesHistory /></ProtectedRoute>} />
          <Route path="/daily-report" element={<ProtectedRoute requiredPermissions={['finances.reports']}><DailyReport /></ProtectedRoute>} />
          <Route path="/reports" element={<ProtectedRoute requiredPermissions={['finances.reports']}><Reports /></ProtectedRoute>} />
          <Route path="/analytics" element={<ProtectedRoute requiredPermissions={['finances.view']}><Analytics /></ProtectedRoute>} />

          {/* Operational Pages */}
          <Route path="/tables" element={<ProtectedRoute requiredPermissions={['tables.view']}><Tables /></ProtectedRoute>} />
          <Route path="/orders" element={<ProtectedRoute requiredPermissions={['orders.view']}><Orders /></ProtectedRoute>} />

          {/* Administration */}
          <Route path="/users" element={<ProtectedRoute requiredPermissions={['users.view']}><Users /></ProtectedRoute>} />
          <Route path="/suppliers" element={<ProtectedRoute requiredPermissions={['stocks.manage']}><Suppliers /></ProtectedRoute>} />
          <Route path="/expenses" element={<ProtectedRoute requiredPermissions={['finances.view']}><Expenses /></ProtectedRoute>} />

          {/* System & Support */}
          <Route path="/settings" element={<ProtectedRoute requiredPermissions={['settings.view']}><Settings /></ProtectedRoute>} />
          <Route path="/alerts" element={<ProtectedRoute><Alerts /></ProtectedRoute>} />
          <Route path="/monitoring" element={<ProtectedRoute requiredPermissions={['settings.view']}><Monitoring /></ProtectedRoute>} />
          <Route path="/help" element={<ProtectedRoute><Help /></ProtectedRoute>} />

          {/* Catch-all route */}
          <Route path="*" element={<NotFound />} />
        </Routes>
          </NotificationProvider>
        </AuthProvider>
      </BrowserRouter>
    </TooltipProvider>
  </QueryProvider>
);

export default App;
