import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { QueryProvider } from "@/providers/QueryProvider";
import { TooltipProvider } from "@/components/ui/tooltip";
import { Toaster } from "@/components/ui/toaster";
import { NotificationProvider } from "@/hooks/use-notifications";
import { AuthProvider } from "@/hooks/use-auth-dynamic";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute-dynamic";

// Pages
import Index from "@/pages/Index";
import Login from "@/pages/Login";
import Profile from "@/pages/Profile";
import Products from "@/pages/Products";
import Sales from "@/pages/Sales";
import Kitchen from "@/pages/Kitchen";
import Stocks from "@/pages/Stocks";
import StockSync from "@/pages/StockSync";
import Supplies from "@/pages/Supplies";
import SalesHistory from "@/pages/SalesHistory";
import DailyReport from "@/pages/DailyReport";
import Settings from "@/pages/Settings";
import Users from "@/pages/Users";
import Tables from "@/pages/Tables";
import Orders from "@/pages/Orders";
import CashierDashboard from "@/pages/CashierDashboard";
import Suppliers from "@/pages/Suppliers";
import Expenses from "@/pages/Expenses";
import Alerts from "@/pages/Alerts";

function App() {
  return (
    <QueryProvider>
      <TooltipProvider>
        <Router>
          <AuthProvider>
            <NotificationProvider>
              <Routes>
                {/* Route publique */}
                <Route path="/login" element={<Login />} />
                
                {/* Routes protégées */}
                <Route path="/" element={
                  <ProtectedRoute>
                    <Index />
                  </ProtectedRoute>
                } />
                
                <Route path="/profile" element={
                  <ProtectedRoute>
                    <Profile />
                  </ProtectedRoute>
                } />
                
                <Route path="/products" element={
                  <ProtectedRoute>
                    <Products />
                  </ProtectedRoute>
                } />
                
                <Route path="/sales" element={
                  <ProtectedRoute>
                    <Sales />
                  </ProtectedRoute>
                } />
                
                <Route path="/kitchen" element={
                  <ProtectedRoute>
                    <Kitchen />
                  </ProtectedRoute>
                } />
                
                <Route path="/stocks" element={
                  <ProtectedRoute>
                    <Stocks />
                  </ProtectedRoute>
                } />
                
                <Route path="/stock-sync" element={
                  <ProtectedRoute>
                    <StockSync />
                  </ProtectedRoute>
                } />
                
                <Route path="/supplies" element={
                  <ProtectedRoute>
                    <Supplies />
                  </ProtectedRoute>
                } />
                
                <Route path="/sales-history" element={
                  <ProtectedRoute>
                    <SalesHistory />
                  </ProtectedRoute>
                } />
                
                <Route path="/daily-report" element={
                  <ProtectedRoute>
                    <DailyReport />
                  </ProtectedRoute>
                } />
                
                <Route path="/settings" element={
                  <ProtectedRoute requiredRole="admin">
                    <Settings />
                  </ProtectedRoute>
                } />
                
                <Route path="/users" element={
                  <ProtectedRoute requiredRole="admin">
                    <Users />
                  </ProtectedRoute>
                } />
                
                <Route path="/tables" element={
                  <ProtectedRoute>
                    <Tables />
                  </ProtectedRoute>
                } />
                
                <Route path="/orders" element={
                  <ProtectedRoute>
                    <Orders />
                  </ProtectedRoute>
                } />
                
                <Route path="/cashier-dashboard" element={
                  <ProtectedRoute requiredRole="cashier">
                    <CashierDashboard />
                  </ProtectedRoute>
                } />
                
                <Route path="/suppliers" element={
                  <ProtectedRoute>
                    <Suppliers />
                  </ProtectedRoute>
                } />
                
                <Route path="/expenses" element={
                  <ProtectedRoute>
                    <Expenses />
                  </ProtectedRoute>
                } />
                
                <Route path="/alerts" element={
                  <ProtectedRoute>
                    <Alerts />
                  </ProtectedRoute>
                } />
              </Routes>
            </NotificationProvider>
          </AuthProvider>
        </Router>
        <Toaster />
      </TooltipProvider>
    </QueryProvider>
  );
}

export default App;
