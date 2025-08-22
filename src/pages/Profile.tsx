import { useState, useEffect } from "react";
import { Sidebar } from "@/components/layout/Sidebar";
import { Header } from "@/components/layout/Header";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";

interface UserProfileData {
  id?: string | number;
  first_name?: string;
  last_name?: string;
  email?: string;
  phone?: string;
  address?: string;
  language?: string;
  timezone?: string;
  avatar?: string;
}

interface UserProfileForm extends Omit<UserProfileData, 'first_name' | 'last_name'> {
  firstName: string;
  lastName: string;
  language: string;
  timezone: string;
  avatar: string;
}
import { 
  User, 
  Mail, 
  Phone, 
  MapPin, 
  Lock, 
  Camera, 
  Globe, 
  Clock,
  Activity,
  Save,
  Eye,
  EyeOff
} from "lucide-react";
import { useAuth } from "@/hooks/use-auth";
import { useUserActivities, useUpdateProfile, useChangePassword, useUpdatePreferences } from "@/hooks/use-api";
import { toast } from "sonner";
import { useQuery } from "@tanstack/react-query";
import { apiService } from "@/services/api";

export default function Profile() {
  const { user } = useAuth();
  const [showCurrentPassword, setShowCurrentPassword] = useState(false);
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  // User profile state initialized with auth user data
  const [userProfile, setUserProfile] = useState<UserProfileForm>({
    firstName: "",
    lastName: "",
    email: "",
    phone: "",
    address: "",
    language: "fr",
    timezone: "Africa/Bujumbura",
    avatar: ""
  });

  // Fetch user activities
  const {
    data: activitiesData,
    isLoading: activitiesLoading,
    error: activitiesError
  } = useUserActivities({ user: user?.id });

  // Fetch current user profile from API
  const {
    data: profileData,
    isLoading: profileLoading,
    refetch: refetchProfile
  } = useQuery<UserProfileData>({
    queryKey: ['auth', 'profile'],
    queryFn: () => apiService.get('/auth/profile/') as Promise<UserProfileData>,
    enabled: !!user?.id,
    staleTime: 0 // Toujours récupérer les données fraîches
  });

  // Update profile when user data or profile data is available
  useEffect(() => {
    const userData = (profileData || user) as UserProfileData | null;
    if (userData) {
      setUserProfile(prev => ({
        ...prev,
        firstName: userData.first_name || "",
        lastName: userData.last_name || "",
        email: userData.email || "",
        phone: userData.phone || "",
        address: userData.address || "",
        language: userData.language || "fr",
        timezone: userData.timezone || "Africa/Bujumbura",
        avatar: userData.avatar || ""
      }));
    }
  }, [user, profileData]);

  const [passwordData, setPasswordData] = useState({
    currentPassword: "",
    newPassword: "",
    confirmPassword: ""
  });

  // Process activity history from API
  const activityHistory = activitiesData?.results?.map((activity: any) => ({
    date: new Date(activity.timestamp).toLocaleString('fr-FR'),
    action: activity.description || activity.action,
    type: activity.action.toLowerCase().includes('login') ? 'login' : 
          activity.action.toLowerCase().includes('product') ? 'product' :
          activity.action.toLowerCase().includes('sale') ? 'sale' :
          activity.action.toLowerCase().includes('report') ? 'report' :
          activity.action.toLowerCase().includes('stock') ? 'stock' : 'other'
  })) || [];

  // Hooks pour les mutations API
  const updateProfileMutation = useUpdateProfile();
  const changePasswordMutation = useChangePassword();
  const updatePreferencesMutation = useUpdatePreferences();

  const handleProfileUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    updateProfileMutation.mutate({
      first_name: userProfile.firstName,
      last_name: userProfile.lastName,
      email: userProfile.email,
      phone: userProfile.phone || undefined
    }, {
      onSuccess: (updatedData: UserProfileData) => {
        // Mettre à jour l'état local avec les nouvelles données
        setUserProfile(prev => ({
          ...prev,
          firstName: updatedData.first_name || prev.firstName,
          lastName: updatedData.last_name || prev.lastName,
          email: updatedData.email || prev.email,
          phone: updatedData.phone || prev.phone,
          language: updatedData.language || prev.language,
          timezone: updatedData.timezone || prev.timezone,
          avatar: updatedData.avatar || prev.avatar
        }));
        
        // Forcer la mise à jour du contexte auth
        window.location.reload();
      }
    });
  };

  const handlePasswordChange = async (e: React.FormEvent) => {
    e.preventDefault();
    if (passwordData.newPassword !== passwordData.confirmPassword) {
      toast.error("Les mots de passe ne correspondent pas");
      return;
    }
    changePasswordMutation.mutate({
      current_password: passwordData.currentPassword,
      new_password: passwordData.newPassword
    }, {
      onSuccess: () => {
        setPasswordData({ currentPassword: "", newPassword: "", confirmPassword: "" });
      }
    });
  };

  const handleAvatarUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      // TODO: Implement avatar upload logic
      const reader = new FileReader();
      reader.onload = (event) => {
        setUserProfile(prev => ({
          ...prev,
          avatar: event.target?.result as string
        }));
      };
      reader.readAsDataURL(file);
    }
  };

  const getActivityIcon = (type: string) => {
    switch (type) {
      case "login": return "🔐";
      case "product": return "📦";
      case "sale": return "💰";
      case "report": return "📊";
      case "stock": return "📋";
      default: return "📝";
    }
  };

  return (
    <div className="min-h-screen bg-gradient-surface flex">
      <Sidebar />
      
      <div className="flex-1 flex flex-col">
        <Header />
        
        <main className="flex-1 p-6 space-y-6">
          {/* Header Section */}
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-foreground mb-2">
                Profil utilisateur
              </h1>
              <p className="text-muted-foreground">
                Gérez vos informations personnelles et préférences
              </p>
            </div>
          </div>

          <Tabs defaultValue="profile" className="space-y-6">
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="profile">Profil</TabsTrigger>
              <TabsTrigger value="security">Sécurité</TabsTrigger>
              <TabsTrigger value="preferences">Préférences</TabsTrigger>
              <TabsTrigger value="activity">Activité</TabsTrigger>
            </TabsList>

            {/* Profile Tab */}
            <TabsContent value="profile">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <User className="h-5 w-5" />
                    Informations personnelles
                  </CardTitle>
                  <CardDescription>
                    Modifiez vos informations de profil
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <form onSubmit={handleProfileUpdate} className="space-y-6">
                    {/* Avatar Section */}
                    <div className="flex items-center gap-6">
                      <div className="relative">
                        <Avatar className="h-24 w-24">
                          <AvatarImage src={userProfile.avatar} />
                          <AvatarFallback className="text-lg">
                            {userProfile.firstName[0]}{userProfile.lastName[0]}
                          </AvatarFallback>
                        </Avatar>
                        <label htmlFor="avatar-upload" className="absolute -bottom-2 -right-2 bg-primary text-primary-foreground rounded-full p-2 cursor-pointer hover:bg-primary/90 transition-colors">
                          <Camera className="h-4 w-4" />
                        </label>
                        <input
                          id="avatar-upload"
                          type="file"
                          accept="image/*"
                          onChange={handleAvatarUpload}
                          className="hidden"
                        />
                      </div>
                      <div>
                        <h3 className="text-lg font-semibold">{userProfile.firstName} {userProfile.lastName}</h3>
                        <p className="text-muted-foreground">{userProfile.email}</p>
                        <Badge variant="success" className="mt-2">
                          {user?.is_superuser ? 'Administrateur' : user?.is_staff ? 'Gérant' : 'Serveur'}
                        </Badge>
                      </div>
                    </div>

                    {/* Form Fields */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="firstName">Prénom</Label>
                        <Input
                          id="firstName"
                          value={userProfile.firstName}
                          onChange={(e) => setUserProfile(prev => ({...prev, firstName: e.target.value}))}
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="lastName">Nom</Label>
                        <Input
                          id="lastName"
                          value={userProfile.lastName}
                          onChange={(e) => setUserProfile(prev => ({...prev, lastName: e.target.value}))}
                        />
                      </div>
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="email">Email</Label>
                      <div className="relative">
                        <Mail className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                        <Input
                          id="email"
                          type="email"
                          value={userProfile.email}
                          onChange={(e) => setUserProfile(prev => ({...prev, email: e.target.value}))}
                          className="pl-10"
                        />
                      </div>
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="phone">Téléphone</Label>
                      <div className="relative">
                        <Phone className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                        <Input
                          id="phone"
                          value={userProfile.phone}
                          onChange={(e) => setUserProfile(prev => ({...prev, phone: e.target.value}))}
                          className="pl-10"
                        />
                      </div>
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="address">Adresse</Label>
                      <div className="relative">
                        <MapPin className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                        <Input
                          id="address"
                          value={userProfile.address}
                          onChange={(e) => setUserProfile(prev => ({...prev, address: e.target.value}))}
                          className="pl-10"
                        />
                      </div>
                    </div>

                    <Button 
                      type="submit" 
                      disabled={updateProfileMutation.isPending}
                      className="w-full gap-2"
                    >
                      <Save className="h-4 w-4" />
                      {updateProfileMutation.isPending ? 'Sauvegarde...' : 'Sauvegarder les modifications'}
                    </Button>
                  </form>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Security Tab */}
            <TabsContent value="security">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Lock className="h-5 w-5" />
                    Sécurité
                  </CardTitle>
                  <CardDescription>
                    Modifiez votre mot de passe et gérez la sécurité de votre compte
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <form onSubmit={handlePasswordChange} className="space-y-4">
                    <div className="space-y-2">
                      <Label htmlFor="currentPassword">Mot de passe actuel</Label>
                      <div className="relative">
                        <Lock className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                        <Input
                          id="currentPassword"
                          type={showCurrentPassword ? "text" : "password"}
                          value={passwordData.currentPassword}
                          onChange={(e) => setPasswordData(prev => ({...prev, currentPassword: e.target.value}))}
                          className="pl-10 pr-10"
                        />
                        <Button
                          type="button"
                          variant="ghost"
                          size="icon"
                          className="absolute right-0 top-0 h-full px-3"
                          onClick={() => setShowCurrentPassword(!showCurrentPassword)}
                        >
                          {showCurrentPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                        </Button>
                      </div>
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="newPassword">Nouveau mot de passe</Label>
                      <div className="relative">
                        <Lock className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                        <Input
                          id="newPassword"
                          type={showNewPassword ? "text" : "password"}
                          value={passwordData.newPassword}
                          onChange={(e) => setPasswordData(prev => ({...prev, newPassword: e.target.value}))}
                          className="pl-10 pr-10"
                        />
                        <Button
                          type="button"
                          variant="ghost"
                          size="icon"
                          className="absolute right-0 top-0 h-full px-3"
                          onClick={() => setShowNewPassword(!showNewPassword)}
                        >
                          {showNewPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                        </Button>
                      </div>
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="confirmPassword">Confirmer le mot de passe</Label>
                      <div className="relative">
                        <Lock className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                        <Input
                          id="confirmPassword"
                          type={showConfirmPassword ? "text" : "password"}
                          value={passwordData.confirmPassword}
                          onChange={(e) => setPasswordData(prev => ({...prev, confirmPassword: e.target.value}))}
                          className="pl-10 pr-10"
                        />
                        <Button
                          type="button"
                          variant="ghost"
                          size="icon"
                          className="absolute right-0 top-0 h-full px-3"
                          onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                        >
                          {showConfirmPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                        </Button>
                      </div>
                    </div>

                    <Button 
                      type="submit" 
                      disabled={changePasswordMutation.isPending}
                      className="w-full"
                    >
                      {changePasswordMutation.isPending ? 'Changement...' : 'Changer le mot de passe'}
                    </Button>
                  </form>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Preferences Tab */}
            <TabsContent value="preferences">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Globe className="h-5 w-5" />
                    Préférences
                  </CardTitle>
                  <CardDescription>
                    Configurez vos préférences d'utilisation
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="language">Langue</Label>
                    <Select value={userProfile.language} onValueChange={(value) => setUserProfile(prev => ({...prev, language: value}))}>
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
                    <Label htmlFor="timezone">Fuseau horaire</Label>
                    <Select value={userProfile.timezone} onValueChange={(value) => setUserProfile(prev => ({...prev, timezone: value}))}>
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

                  <Button 
                    onClick={() => updatePreferencesMutation.mutate({
                      language: userProfile.language,
                      timezone: userProfile.timezone
                    })}
                    disabled={updatePreferencesMutation.isPending}
                    className="w-full gap-2"
                  >
                    <Save className="h-4 w-4" />
                    {updatePreferencesMutation.isPending ? 'Sauvegarde...' : 'Sauvegarder les préférences'}
                  </Button>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Activity Tab */}
            <TabsContent value="activity">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Activity className="h-5 w-5" />
                    Historique d'activité
                  </CardTitle>
                  <CardDescription>
                    Consultez vos dernières actions dans le système
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  {activitiesLoading ? (
                    <div className="text-center py-8">
                      <p className="text-muted-foreground">Chargement des activités...</p>
                    </div>
                  ) : activitiesError ? (
                    <div className="text-center py-8">
                      <p className="text-red-500">Erreur lors du chargement des activités</p>
                    </div>
                  ) : activityHistory.length === 0 ? (
                    <div className="text-center py-8">
                      <p className="text-muted-foreground">Aucune activité récente</p>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      {activityHistory.map((activity, index) => (
                        <div key={index} className="flex items-center gap-4 p-3 border rounded-lg">
                          <div className="text-2xl">{getActivityIcon(activity.type)}</div>
                          <div className="flex-1">
                            <p className="font-medium">{activity.action}</p>
                            <p className="text-sm text-muted-foreground flex items-center gap-1">
                              <Clock className="h-3 w-3" />
                              {activity.date}
                            </p>
                          </div>
                          <Badge variant="outline">{activity.type}</Badge>
                        </div>
                      ))}
                    </div>
                  )}
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </main>
      </div>
    </div>
  );
}
