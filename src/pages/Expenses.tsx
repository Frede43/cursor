import { useState, useMemo } from "react";
import { Sidebar } from "@/components/layout/Sidebar";
import { Header } from "@/components/layout/Header";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Progress } from "@/components/ui/progress";
import { 
  Receipt, 
  Plus, 
  Edit, 
  Trash2, 
  Upload,
  Download,
  Calendar,
  DollarSign,
  TrendingUp,
  AlertTriangle,
  CheckCircle,
  Clock,
  FileText,
  Camera
} from "lucide-react";
import { useExpenses, useExpenseCategories, useCreateExpense } from "@/hooks/use-api";
import { useToast } from "@/hooks/use-toast";

interface Expense {
  id: string;
  date: string;
  category: string;
  description: string;
  amount: number;
  supplier?: string;
  paymentMethod: "cash" | "bank" | "card" | "mobile" | "bank_transfer" | "check";
  status: "pending" | "approved" | "rejected" | "paid";
  receipt?: string;
  approvedBy?: string;
  notes?: string;
}


const expenseCategories = [
  "Achats marchandises",
  "Salaires",
  "Électricité",
  "Eau",
  "Maintenance",
  "Marketing",
  "Transport",
  "Assurance",
  "Taxes",
  "Autres"
];


export default function Expenses() {
  const [showNewExpenseDialog, setShowNewExpenseDialog] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [newExpense, setNewExpense] = useState({
    category: "",
    description: "",
    amount: "",
    supplier: "",
    paymentMethod: "cash" as const,
    receipt: null as File | null
  });
  const { toast } = useToast();

  // Récupérer les données des dépenses depuis l'API
  const {
    data: expensesData,
    isLoading: expensesLoading,
    error: expensesError,
    refetch: refetchExpenses
  } = useExpenses({
    category: selectedCategory === "all" ? undefined : parseInt(selectedCategory)
  });

  // Récupérer les catégories de dépenses
  const {
    data: categoriesData,
    isLoading: categoriesLoading
  } = useExpenseCategories({ is_active: true });

  // Hook pour créer une dépense
  const createExpenseMutation = useCreateExpense();

  // Mapper les données de l'API vers le format d'affichage
  const expenses = useMemo(() => {
    if (!expensesData?.results) return [];
    
    return expensesData.results.map(expense => ({
      id: expense.id.toString(),
      date: expense.expense_date,
      category: expense.category_name || "Non catégorisé",
      description: expense.description,
      amount: expense.amount,
      supplier: (expense as any).supplier_name,
      paymentMethod: expense.payment_method as "cash" | "bank" | "card" | "mobile" | "bank_transfer" | "check",
      status: expense.is_approved ? "approved" as const : "pending" as const,
      receipt: expense.receipt_number,
      approvedBy: expense.approved_by_name,
      notes: expense.notes
    }));
  }, [expensesData]);

  // Mapper les catégories
  const categories = useMemo(() => {
    if (!categoriesData?.results) return expenseCategories;
    return categoriesData.results.map(cat => cat.name);
  }, [categoriesData]);

  // Calculer les budgets dynamiquement à partir des dépenses
  const monthlyBudgets = useMemo(() => {
    if (!expenses.length) return {};
    
    const budgetsByCategory: Record<string, { budget: number; spent: number }> = {};
    
    // Grouper les dépenses par catégorie
    expenses.forEach(expense => {
      if (!budgetsByCategory[expense.category]) {
        budgetsByCategory[expense.category] = {
          budget: 0,
          spent: 0
        };
      }
      budgetsByCategory[expense.category].spent += expense.amount;
    });
    
    // Définir des budgets par défaut basés sur les dépenses actuelles
    Object.keys(budgetsByCategory).forEach(category => {
      const spent = budgetsByCategory[category].spent;
      // Budget = 150% des dépenses actuelles (marge de sécurité)
      budgetsByCategory[category].budget = Math.round(spent * 1.5);
    });
    
    return budgetsByCategory;
  }, [expenses]);

  const getStatusInfo = (status: Expense["status"]) => {
    switch (status) {
      case "pending":
        return { variant: "warning" as const, label: "En attente", icon: Clock };
      case "approved":
        return { variant: "success" as const, label: "Approuvée", icon: CheckCircle };
      case "rejected":
        return { variant: "destructive" as const, label: "Rejetée", icon: AlertTriangle };
      case "paid":
        return { variant: "default" as const, label: "Payée", icon: DollarSign };
    }
  };

  const getPaymentMethodLabel = (method: string) => {
    switch (method) {
      case "cash": return "Espèces";
      case "bank":
      case "bank_transfer": return "Virement";
      case "card": return "Carte";
      case "mobile": return "Mobile Money";
      case "check": return "Chèque";
      default: return method;
    }
  };

  const filteredExpenses = expenses.filter(expense => 
    selectedCategory === "all" || expense.category === selectedCategory
  );

  const totalExpenses = filteredExpenses.reduce((sum, expense) => sum + expense.amount, 0);

  const approveExpense = async (expenseId: string) => {
    try {
      // TODO: Implement API call to approve expense
      // await updateExpense(expenseId, { is_approved: true });
      toast({
        title: "Dépense approuvée",
        description: "La dépense a été approuvée avec succès."
      });
      refetchExpenses();
    } catch (error) {
      toast({
        title: "Erreur",
        description: "Impossible d'approuver la dépense.",
        variant: "destructive"
      });
    }
  };

  const rejectExpense = async (expenseId: string) => {
    try {
      // TODO: Implement API call to reject expense
      // await updateExpense(expenseId, { is_approved: false, status: 'rejected' });
      toast({
        title: "Dépense rejetée",
        description: "La dépense a été rejetée."
      });
      refetchExpenses();
    } catch (error) {
      toast({
        title: "Erreur",
        description: "Impossible de rejeter la dépense.",
        variant: "destructive"
      });
    }
  };

  const createExpense = async () => {
    try {
      const expenseData = {
        description: newExpense.description,
        amount: parseFloat(newExpense.amount),
        category: typeof newExpense.category === 'string' ? 1 : newExpense.category,
        supplier_name: newExpense.supplier,
        payment_method: newExpense.paymentMethod,
        expense_date: new Date().toISOString().split('T')[0],
        is_approved: false
      };

      await createExpenseMutation.mutateAsync(expenseData);
      
      toast({
        title: "Dépense créée",
        description: "La nouvelle dépense a été enregistrée avec succès."
      });
      
      setShowNewExpenseDialog(false);
      setNewExpense({
        category: "",
        description: "",
        amount: "",
        supplier: "",
        paymentMethod: "cash",
        receipt: null
      });
      
      refetchExpenses();
    } catch (error) {
      toast({
        title: "Erreur",
        description: "Impossible de créer la dépense.",
        variant: "destructive"
      });
    }
  };

  const handleReceiptUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setNewExpense(prev => ({ ...prev, receipt: file }));
    }
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
                Gestion des dépenses
              </h1>
              <p className="text-muted-foreground">
                Suivez et contrôlez toutes vos dépenses d'exploitation
              </p>
            </div>
            <Dialog open={showNewExpenseDialog} onOpenChange={setShowNewExpenseDialog}>
              <DialogTrigger asChild>
                <Button className="gap-2">
                  <Plus className="h-4 w-4" />
                  Nouvelle dépense
                </Button>
              </DialogTrigger>
              <DialogContent className="max-w-2xl">
                <DialogHeader>
                  <DialogTitle>Nouvelle dépense</DialogTitle>
                  <DialogDescription>
                    Enregistrez une nouvelle dépense avec justificatif
                  </DialogDescription>
                </DialogHeader>
                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label>Catégorie</Label>
                      <Select value={newExpense.category} onValueChange={(value) => setNewExpense(prev => ({...prev, category: value}))}>
                        <SelectTrigger>
                          <SelectValue placeholder="Sélectionner une catégorie" />
                        </SelectTrigger>
                        <SelectContent>
                          {categories.map(category => (
                            <SelectItem key={category} value={category}>{category}</SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                    <div className="space-y-2">
                      <Label>Montant (FBu)</Label>
                      <Input
                        type="number"
                        value={newExpense.amount}
                        onChange={(e) => setNewExpense(prev => ({...prev, amount: e.target.value}))}
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label>Description</Label>
                    <Textarea
                      placeholder="Décrivez la dépense..."
                      value={newExpense.description}
                      onChange={(e) => setNewExpense(prev => ({...prev, description: e.target.value}))}
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label>Fournisseur (optionnel)</Label>
                      <Input
                        placeholder="Nom du fournisseur"
                        value={newExpense.supplier}
                        onChange={(e) => setNewExpense(prev => ({...prev, supplier: e.target.value}))}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label>Mode de paiement</Label>
                      <Select value={newExpense.paymentMethod} onValueChange={(value: any) => setNewExpense(prev => ({...prev, paymentMethod: value}))}>
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="cash">Espèces</SelectItem>
                          <SelectItem value="bank_transfer">Virement bancaire</SelectItem>
                          <SelectItem value="card">Carte</SelectItem>
                          <SelectItem value="mobile">Mobile Money</SelectItem>
                          <SelectItem value="check">Chèque</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label>Justificatif</Label>
                    <div className="flex items-center gap-2">
                      <Input
                        type="file"
                        accept="image/*,.pdf"
                        onChange={handleReceiptUpload}
                        className="flex-1"
                      />
                      <Button variant="outline" size="icon">
                        <Camera className="h-4 w-4" />
                      </Button>
                    </div>
                    {newExpense.receipt && (
                      <p className="text-sm text-muted-foreground">
                        Fichier sélectionné: {newExpense.receipt.name}
                      </p>
                    )}
                  </div>

                  <Button onClick={createExpense} className="w-full">
                    Enregistrer la dépense
                  </Button>
                </div>
              </DialogContent>
            </Dialog>
          </div>

          {/* Budget Overview */}
          {Object.keys(monthlyBudgets).length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle>Suivi budgétaire mensuel</CardTitle>
                <CardDescription>
                  Progression par rapport aux budgets calculés dynamiquement
                </CardDescription>
              </CardHeader>
              <CardContent>
                {expensesLoading ? (
                  <div className="space-y-4">
                    {[1, 2, 3].map(i => (
                      <div key={i} className="space-y-2">
                        <div className="h-4 bg-muted rounded animate-pulse" />
                        <div className="h-2 bg-muted rounded animate-pulse" />
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="space-y-4">
                    {Object.entries(monthlyBudgets).map(([category, data]) => {
                      const percentage = (data.spent / data.budget) * 100;
                      const isOverBudget = percentage > 100;
                      
                      return (
                        <div key={category} className="space-y-2">
                          <div className="flex justify-between items-center">
                            <span className="font-medium">{category}</span>
                            <div className="text-right">
                              <span className="font-bold">
                                {data.spent.toLocaleString()} / {data.budget.toLocaleString()} FBu
                              </span>
                              <Badge variant={isOverBudget ? "destructive" : percentage > 80 ? "warning" : "success"} className="ml-2">
                                {percentage.toFixed(1)}%
                              </Badge>
                            </div>
                          </div>
                          <Progress 
                            value={Math.min(percentage, 100)} 
                            className={`h-2 ${isOverBudget ? 'bg-destructive/20' : ''}`}
                          />
                          {isOverBudget && (
                            <p className="text-sm text-destructive">
                              ⚠️ Dépassement de budget: +{(data.spent - data.budget).toLocaleString()} FBu
                            </p>
                          )}
                        </div>
                      );
                    })}
                  </div>
                )}
              </CardContent>
            </Card>
          )}

          {/* Filters */}
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center gap-4">
                <Label>Filtrer par catégorie:</Label>
                <Select value={selectedCategory} onValueChange={setSelectedCategory}>
                  <SelectTrigger className="w-64">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">Toutes les catégories</SelectItem>
                    {categories.map(category => (
                      <SelectItem key={category} value={category}>{category}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <div className="ml-auto">
                  <span className="text-sm text-muted-foreground">Total affiché: </span>
                  <span className="font-bold text-lg">{totalExpenses.toLocaleString()} FBu</span>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Expenses List */}
          <Card>
            <CardHeader>
              <CardTitle>Liste des dépenses</CardTitle>
              <CardDescription>
                {filteredExpenses.length} dépense(s) • Total: {totalExpenses.toLocaleString()} FBu
              </CardDescription>
            </CardHeader>
            <CardContent>
              {expensesLoading ? (
                <div className="space-y-4">
                  {[1, 2, 3, 4, 5].map(i => (
                    <div key={i} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="flex items-center gap-4">
                        <div className="h-12 w-12 bg-muted rounded-lg animate-pulse" />
                        <div className="space-y-2">
                          <div className="h-4 w-48 bg-muted rounded animate-pulse" />
                          <div className="h-3 w-32 bg-muted rounded animate-pulse" />
                        </div>
                      </div>
                      <div className="text-right space-y-2">
                        <div className="h-6 w-24 bg-muted rounded animate-pulse" />
                        <div className="h-8 w-20 bg-muted rounded animate-pulse" />
                      </div>
                    </div>
                  ))}
                </div>
              ) : filteredExpenses.length === 0 ? (
                <div className="text-center py-8">
                  <Receipt className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                  <h3 className="text-lg font-semibold mb-2">Aucune dépense trouvée</h3>
                  <p className="text-muted-foreground mb-4">
                    {selectedCategory === "all" 
                      ? "Aucune dépense enregistrée pour le moment."
                      : `Aucune dépense dans la catégorie "${selectedCategory}".`
                    }
                  </p>
                  <Button onClick={() => setShowNewExpenseDialog(true)} className="gap-2">
                    <Plus className="h-4 w-4" />
                    Ajouter une dépense
                  </Button>
                </div>
              ) : (
                <div className="space-y-4">
                  {filteredExpenses.map((expense) => {
                  const statusInfo = getStatusInfo(expense.status);
                  const StatusIcon = statusInfo.icon;
                  
                  return (
                    <div
                      key={expense.id}
                      className="flex items-center justify-between p-4 border rounded-lg hover:bg-muted/50 transition-colors"
                    >
                      <div className="flex items-center gap-4">
                        <div className="h-12 w-12 bg-gradient-to-br from-primary to-primary-glow rounded-lg flex items-center justify-center">
                          <Receipt className="h-6 w-6 text-primary-foreground" />
                        </div>
                        <div>
                          <div className="flex items-center gap-2 mb-1">
                            <h3 className="font-semibold">{expense.description}</h3>
                            <Badge variant={statusInfo.variant} className="gap-1">
                              <StatusIcon className="h-3 w-3" />
                              {statusInfo.label}
                            </Badge>
                          </div>
                          <div className="text-sm text-muted-foreground space-y-1">
                            <div className="flex items-center gap-4">
                              <span className="flex items-center gap-1">
                                <Calendar className="h-3 w-3" />
                                {expense.date}
                              </span>
                              <Badge variant="outline">{expense.category}</Badge>
                              <span>{getPaymentMethodLabel(expense.paymentMethod)}</span>
                            </div>
                            {expense.supplier && (
                              <div>Fournisseur: {expense.supplier}</div>
                            )}
                            {expense.approvedBy && (
                              <div>Approuvé par: {expense.approvedBy}</div>
                            )}
                          </div>
                        </div>
                      </div>

                      <div className="text-right">
                        <div className="text-xl font-bold mb-2">
                          {expense.amount.toLocaleString()} FBu
                        </div>
                        <div className="flex gap-2">
                          {expense.receipt && (
                            <Button variant="outline" size="sm" className="gap-1">
                              <FileText className="h-4 w-4" />
                              Voir
                            </Button>
                          )}
                          
                          {expense.status === "pending" && (
                            <>
                              <Button 
                                size="sm"
                                onClick={() => approveExpense(expense.id)}
                                className="gap-1"
                              >
                                <CheckCircle className="h-4 w-4" />
                                Approuver
                              </Button>
                              <Button 
                                variant="destructive"
                                size="sm"
                                onClick={() => rejectExpense(expense.id)}
                                className="gap-1"
                              >
                                <AlertTriangle className="h-4 w-4" />
                                Rejeter
                              </Button>
                            </>
                          )}

                          <Button variant="outline" size="sm">
                            <Edit className="h-4 w-4" />
                          </Button>
                        </div>
                      </div>
                    </div>
                  );
                  })}
                </div>
              )}
            </CardContent>
          </Card>
        </main>
      </div>
    </div>
  );
}
