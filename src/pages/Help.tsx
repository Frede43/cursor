import { useState } from "react";
import { Sidebar } from "@/components/layout/Sidebar";
import { Header } from "@/components/layout/Header";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { 
  HelpCircle, 
  Search, 
  Book, 
  Video,
  MessageCircle,
  Phone,
  Mail,
  FileText,
  Play,
  Download,
  Star,
  ThumbsUp,
  Send
} from "lucide-react";

interface FAQItem {
  id: string;
  question: string;
  answer: string;
  category: string;
  helpful: number;
  views: number;
}

interface Tutorial {
  id: string;
  title: string;
  description: string;
  duration: string;
  category: string;
  difficulty: "beginner" | "intermediate" | "advanced";
  videoUrl?: string;
}

const faqItems: FAQItem[] = [
  {
    id: "1",
    question: "Comment ajouter un nouveau produit ?",
    answer: "Allez dans la section 'Produits', cliquez sur 'Nouveau produit', remplissez les informations requises (nom, prix, catégorie, stock initial) et sauvegardez.",
    category: "Produits",
    helpful: 15,
    views: 45
  },
  {
    id: "2",
    question: "Comment effectuer une vente ?",
    answer: "Utilisez l'interface POS dans 'Ventes'. Sélectionnez la table, ajoutez les produits au panier, choisissez le mode de paiement et finalisez la transaction.",
    category: "Ventes",
    helpful: 23,
    views: 67
  },
  {
    id: "3",
    question: "Comment gérer les alertes de stock ?",
    answer: "Les alertes apparaissent automatiquement quand le stock atteint le seuil minimum. Vous pouvez configurer ces seuils dans les paramètres de chaque produit.",
    category: "Stocks",
    helpful: 18,
    views: 52
  },
  {
    id: "4",
    question: "Comment générer un rapport ?",
    answer: "Allez dans 'Rapports', sélectionnez le type de rapport, la période et le format d'export souhaité, puis cliquez sur 'Générer'.",
    category: "Rapports",
    helpful: 12,
    views: 34
  }
];

const tutorials: Tutorial[] = [
  {
    id: "1",
    title: "Premiers pas avec Bar Stock Wise",
    description: "Introduction complète au système de gestion",
    duration: "15 min",
    category: "Démarrage",
    difficulty: "beginner"
  },
  {
    id: "2",
    title: "Configuration du point de vente",
    description: "Paramétrer l'interface POS pour votre établissement",
    duration: "12 min",
    category: "Ventes",
    difficulty: "intermediate"
  },
  {
    id: "3",
    title: "Gestion avancée des stocks",
    description: "Optimiser la gestion des inventaires et approvisionnements",
    duration: "20 min",
    category: "Stocks",
    difficulty: "advanced"
  },
  {
    id: "4",
    title: "Création de rapports personnalisés",
    description: "Générer des analyses adaptées à vos besoins",
    duration: "18 min",
    category: "Rapports",
    difficulty: "intermediate"
  }
];

export default function Help() {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [showSupportDialog, setShowSupportDialog] = useState(false);
  const [supportRequest, setSupportRequest] = useState({
    subject: "",
    category: "",
    priority: "medium",
    message: ""
  });

  const categories = ["all", "Démarrage", "Produits", "Ventes", "Stocks", "Rapports", "Paramètres"];
  const supportCategories = ["Technique", "Fonctionnel", "Formation", "Facturation"];

  const filteredFAQ = faqItems.filter(item => {
    const matchesSearch = item.question.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         item.answer.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === "all" || item.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const filteredTutorials = tutorials.filter(tutorial => {
    const matchesSearch = tutorial.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         tutorial.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === "all" || tutorial.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const getDifficultyInfo = (difficulty: Tutorial["difficulty"]) => {
    switch (difficulty) {
      case "beginner":
        return { variant: "success" as const, label: "Débutant" };
      case "intermediate":
        return { variant: "warning" as const, label: "Intermédiaire" };
      case "advanced":
        return { variant: "destructive" as const, label: "Avancé" };
    }
  };

  const submitSupportRequest = () => {
    // TODO: Implement support request submission
    console.log("Support request:", supportRequest);
    setShowSupportDialog(false);
    setSupportRequest({
      subject: "",
      category: "",
      priority: "medium",
      message: ""
    });
  };

  const markHelpful = (faqId: string) => {
    // TODO: Implement helpful marking
    console.log(`Marked FAQ ${faqId} as helpful`);
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
                Centre d'aide
              </h1>
              <p className="text-muted-foreground">
                Documentation, tutoriels et support technique
              </p>
            </div>
            <Dialog open={showSupportDialog} onOpenChange={setShowSupportDialog}>
              <DialogTrigger asChild>
                <Button className="gap-2">
                  <MessageCircle className="h-4 w-4" />
                  Contacter le support
                </Button>
              </DialogTrigger>
              <DialogContent className="max-w-2xl">
                <DialogHeader>
                  <DialogTitle>Demande de support</DialogTitle>
                  <DialogDescription>
                    Décrivez votre problème, notre équipe vous aidera rapidement
                  </DialogDescription>
                </DialogHeader>
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label>Sujet</Label>
                    <Input
                      placeholder="Résumé de votre problème"
                      value={supportRequest.subject}
                      onChange={(e) => setSupportRequest(prev => ({...prev, subject: e.target.value}))}
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label>Catégorie</Label>
                      <select 
                        value={supportRequest.category} 
                        onChange={(e) => setSupportRequest(prev => ({...prev, category: e.target.value}))}
                        className="w-full p-2 border rounded"
                      >
                        <option value="">Sélectionner une catégorie</option>
                        {supportCategories.map(cat => (
                          <option key={cat} value={cat}>{cat}</option>
                        ))}
                      </select>
                    </div>
                    <div className="space-y-2">
                      <Label>Priorité</Label>
                      <select 
                        value={supportRequest.priority} 
                        onChange={(e) => setSupportRequest(prev => ({...prev, priority: e.target.value}))}
                        className="w-full p-2 border rounded"
                      >
                        <option value="low">Faible</option>
                        <option value="medium">Moyenne</option>
                        <option value="high">Élevée</option>
                        <option value="urgent">Urgente</option>
                      </select>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label>Description détaillée</Label>
                    <Textarea
                      placeholder="Décrivez votre problème en détail..."
                      value={supportRequest.message}
                      onChange={(e) => setSupportRequest(prev => ({...prev, message: e.target.value}))}
                      rows={5}
                    />
                  </div>

                  <Button onClick={submitSupportRequest} className="w-full gap-2">
                    <Send className="h-4 w-4" />
                    Envoyer la demande
                  </Button>
                </div>
              </DialogContent>
            </Dialog>
          </div>

          {/* Quick Contact */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card>
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="h-12 w-12 bg-gradient-to-br from-primary to-primary-glow rounded-lg flex items-center justify-center mx-auto mb-3">
                    <Phone className="h-6 w-6 text-primary-foreground" />
                  </div>
                  <h3 className="font-semibold mb-1">Support téléphonique</h3>
                  <p className="text-sm text-muted-foreground mb-3">Lun-Ven 8h-18h</p>
                  <p className="font-medium">+257 22 123 456</p>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="h-12 w-12 bg-gradient-to-br from-success to-success/80 rounded-lg flex items-center justify-center mx-auto mb-3">
                    <Mail className="h-6 w-6 text-success-foreground" />
                  </div>
                  <h3 className="font-semibold mb-1">Support email</h3>
                  <p className="text-sm text-muted-foreground mb-3">Réponse sous 24h</p>
                  <p className="font-medium">support@barstock.demo</p>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="h-12 w-12 bg-gradient-to-br from-warning to-warning/80 rounded-lg flex items-center justify-center mx-auto mb-3">
                    <MessageCircle className="h-6 w-6 text-warning-foreground" />
                  </div>
                  <h3 className="font-semibold mb-1">Chat en direct</h3>
                  <p className="text-sm text-muted-foreground mb-3">Disponible 24/7</p>
                  <Button size="sm">Démarrer le chat</Button>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Search */}
          <Card>
            <CardContent className="pt-6">
              <div className="flex gap-4">
                <div className="flex-1 relative">
                  <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                  <Input
                    placeholder="Rechercher dans la documentation..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-10"
                  />
                </div>
                <select 
                  value={selectedCategory} 
                  onChange={(e) => setSelectedCategory(e.target.value)}
                  className="px-3 py-2 border rounded-md"
                >
                  {categories.map(cat => (
                    <option key={cat} value={cat}>
                      {cat === "all" ? "Toutes catégories" : cat}
                    </option>
                  ))}
                </select>
              </div>
            </CardContent>
          </Card>

          <Tabs defaultValue="faq" className="space-y-6">
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="faq">FAQ</TabsTrigger>
              <TabsTrigger value="tutorials">Tutoriels</TabsTrigger>
              <TabsTrigger value="documentation">Documentation</TabsTrigger>
              <TabsTrigger value="contact">Contact</TabsTrigger>
            </TabsList>

            {/* FAQ Tab */}
            <TabsContent value="faq">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <HelpCircle className="h-5 w-5" />
                    Questions fréquentes
                  </CardTitle>
                  <CardDescription>
                    {filteredFAQ.length} question(s) trouvée(s)
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <Accordion type="single" collapsible className="space-y-2">
                    {filteredFAQ.map((item) => (
                      <AccordionItem key={item.id} value={item.id} className="border rounded-lg px-4">
                        <AccordionTrigger className="hover:no-underline">
                          <div className="flex items-center gap-2 text-left">
                            <span>{item.question}</span>
                            <Badge variant="outline">{item.category}</Badge>
                          </div>
                        </AccordionTrigger>
                        <AccordionContent className="pt-4">
                          <p className="text-muted-foreground mb-4">{item.answer}</p>
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-4 text-sm text-muted-foreground">
                              <span>{item.views} vues</span>
                              <span>{item.helpful} personnes ont trouvé cela utile</span>
                            </div>
                            <Button 
                              variant="outline" 
                              size="sm"
                              onClick={() => markHelpful(item.id)}
                              className="gap-1"
                            >
                              <ThumbsUp className="h-3 w-3" />
                              Utile
                            </Button>
                          </div>
                        </AccordionContent>
                      </AccordionItem>
                    ))}
                  </Accordion>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Tutorials Tab */}
            <TabsContent value="tutorials">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Video className="h-5 w-5" />
                    Tutoriels vidéo
                  </CardTitle>
                  <CardDescription>
                    Guides pratiques pour maîtriser toutes les fonctionnalités
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {filteredTutorials.map((tutorial) => {
                      const difficultyInfo = getDifficultyInfo(tutorial.difficulty);
                      
                      return (
                        <Card key={tutorial.id} className="cursor-pointer hover:shadow-md transition-shadow">
                          <CardContent className="p-4">
                            <div className="flex items-start gap-4">
                              <div className="h-16 w-16 bg-gradient-to-br from-primary to-primary-glow rounded-lg flex items-center justify-center">
                                <Play className="h-8 w-8 text-primary-foreground" />
                              </div>
                              <div className="flex-1">
                                <h3 className="font-semibold mb-1">{tutorial.title}</h3>
                                <p className="text-sm text-muted-foreground mb-2">{tutorial.description}</p>
                                <div className="flex items-center gap-2">
                                  <Badge variant="outline">{tutorial.category}</Badge>
                                  <Badge variant={difficultyInfo.variant}>{difficultyInfo.label}</Badge>
                                  <span className="text-sm text-muted-foreground">{tutorial.duration}</span>
                                </div>
                              </div>
                            </div>
                          </CardContent>
                        </Card>
                      );
                    })}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Documentation Tab */}
            <TabsContent value="documentation">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Book className="h-5 w-5" />
                    Documentation technique
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    <Card className="cursor-pointer hover:shadow-md transition-shadow">
                      <CardContent className="p-4 text-center">
                        <FileText className="h-12 w-12 text-primary mx-auto mb-3" />
                        <h3 className="font-semibold mb-2">Guide d'installation</h3>
                        <p className="text-sm text-muted-foreground mb-3">
                          Instructions complètes pour l'installation
                        </p>
                        <Button variant="outline" size="sm" className="gap-1">
                          <Download className="h-3 w-3" />
                          Télécharger PDF
                        </Button>
                      </CardContent>
                    </Card>

                    <Card className="cursor-pointer hover:shadow-md transition-shadow">
                      <CardContent className="p-4 text-center">
                        <FileText className="h-12 w-12 text-success mx-auto mb-3" />
                        <h3 className="font-semibold mb-2">Manuel utilisateur</h3>
                        <p className="text-sm text-muted-foreground mb-3">
                          Guide complet d'utilisation du système
                        </p>
                        <Button variant="outline" size="sm" className="gap-1">
                          <Download className="h-3 w-3" />
                          Télécharger PDF
                        </Button>
                      </CardContent>
                    </Card>

                    <Card className="cursor-pointer hover:shadow-md transition-shadow">
                      <CardContent className="p-4 text-center">
                        <FileText className="h-12 w-12 text-warning mx-auto mb-3" />
                        <h3 className="font-semibold mb-2">API Documentation</h3>
                        <p className="text-sm text-muted-foreground mb-3">
                          Documentation technique pour développeurs
                        </p>
                        <Button variant="outline" size="sm" className="gap-1">
                          <Download className="h-3 w-3" />
                          Télécharger PDF
                        </Button>
                      </CardContent>
                    </Card>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Contact Tab */}
            <TabsContent value="contact">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Informations de contact</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="flex items-center gap-3 p-3 border rounded-lg">
                      <Phone className="h-5 w-5 text-primary" />
                      <div>
                        <p className="font-medium">Support téléphonique</p>
                        <p className="text-sm text-muted-foreground">+257 22 123 456</p>
                        <p className="text-xs text-muted-foreground">Lundi-Vendredi 8h-18h</p>
                      </div>
                    </div>

                    <div className="flex items-center gap-3 p-3 border rounded-lg">
                      <Mail className="h-5 w-5 text-success" />
                      <div>
                        <p className="font-medium">Email support</p>
                        <p className="text-sm text-muted-foreground">support@barstock.demo</p>
                        <p className="text-xs text-muted-foreground">Réponse sous 24h</p>
                      </div>
                    </div>

                    <div className="flex items-center gap-3 p-3 border rounded-lg">
                      <MessageCircle className="h-5 w-5 text-warning" />
                      <div>
                        <p className="font-medium">Chat en direct</p>
                        <p className="text-sm text-muted-foreground">Assistance immédiate</p>
                        <p className="text-xs text-muted-foreground">Disponible 24/7</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle>Ressources utiles</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <Button variant="outline" className="w-full justify-start gap-2">
                      <Book className="h-4 w-4" />
                      Base de connaissances
                    </Button>
                    <Button variant="outline" className="w-full justify-start gap-2">
                      <Video className="h-4 w-4" />
                      Chaîne YouTube
                    </Button>
                    <Button variant="outline" className="w-full justify-start gap-2">
                      <MessageCircle className="h-4 w-4" />
                      Forum communautaire
                    </Button>
                    <Button variant="outline" className="w-full justify-start gap-2">
                      <FileText className="h-4 w-4" />
                      Notes de version
                    </Button>
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
