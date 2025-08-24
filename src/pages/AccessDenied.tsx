import { AlertTriangle, ArrowLeft } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/hooks/use-auth-dynamic';

export default function AccessDenied() {
  const navigate = useNavigate();
  const { user } = useAuth();

  const handleGoBack = () => {
    // Rediriger selon le rôle
    if (user?.role === 'cashier') {
      navigate('/sales');
    } else {
      navigate('/');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background to-muted flex items-center justify-center p-4">
      <div className="max-w-md w-full text-center space-y-6">
        {/* Icône d'alerte */}
        <div className="flex justify-center">
          <div className="rounded-full bg-destructive/10 p-6">
            <AlertTriangle className="h-16 w-16 text-destructive" />
          </div>
        </div>

        {/* Titre */}
        <div className="space-y-2">
          <h1 className="text-3xl font-bold text-foreground">
            Pas d'accès
          </h1>
          <p className="text-muted-foreground">
            Vous n'avez pas les permissions nécessaires pour accéder à cette page.
          </p>
        </div>

        {/* Informations utilisateur */}
        {user && (
          <div className="bg-muted/50 rounded-lg p-4 space-y-2">
            <p className="text-sm text-muted-foreground">
              <span className="font-medium">Utilisateur:</span> {user.first_name || user.username}
            </p>
            <p className="text-sm text-muted-foreground">
              <span className="font-medium">Rôle:</span> {user.role}
            </p>
            <p className="text-sm text-muted-foreground">
              <span className="font-medium">Permissions requises:</span> dashboard.view
            </p>
          </div>
        )}

        {/* Bouton de retour */}
        <Button 
          onClick={handleGoBack}
          className="w-full"
          size="lg"
        >
          <ArrowLeft className="h-4 w-4 mr-2" />
          Retourner à votre espace de travail
        </Button>

        {/* Message d'aide */}
        <p className="text-xs text-muted-foreground">
          Si vous pensez qu'il s'agit d'une erreur, contactez votre administrateur.
        </p>
      </div>
    </div>
  );
}
