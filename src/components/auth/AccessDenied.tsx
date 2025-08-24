/**
 * Composant d'affichage pour les accès refusés
 */

import { UserRole } from '@/types/auth';
import { Button } from '@/components/ui/button';
import { useNavigate } from 'react-router-dom';
import { 
  ShieldX, 
  Lock, 
  ArrowLeft, 
  Home,
  AlertTriangle 
} from 'lucide-react';

interface AccessDeniedProps {
  type: 'role' | 'permission';
  required: string[] | UserRole[];
  current?: string;
  message?: string;
}

export const AccessDenied = ({ 
  type, 
  required, 
  current, 
  message 
}: AccessDeniedProps) => {
  const navigate = useNavigate();

  const getIcon = () => {
    switch (type) {
      case 'role':
        return <ShieldX className="w-20 h-20 text-red-500" />;
      case 'permission':
        return <Lock className="w-20 h-20 text-red-500" />;
      default:
        return <AlertTriangle className="w-20 h-20 text-red-500" />;
    }
  };

  const getTitle = () => {
    switch (type) {
      case 'role':
        return 'Rôle insuffisant';
      case 'permission':
        return 'Permission refusée';
      default:
        return 'Accès refusé';
    }
  };

  const getDescription = () => {
    if (message) return message;
    
    switch (type) {
      case 'role':
        return 'Votre rôle ne vous permet pas d\'accéder à cette ressource.';
      case 'permission':
        return 'Vous n\'avez pas les permissions nécessaires pour cette action.';
      default:
        return 'L\'accès à cette ressource vous est refusé.';
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-8 text-center">
        {/* Icône */}
        <div className="flex justify-center mb-6">
          {getIcon()}
        </div>

        {/* Titre */}
        <h1 className="text-2xl font-bold text-gray-900 mb-4">
          {getTitle()}
        </h1>

        {/* Description */}
        <p className="text-gray-600 mb-6">
          {getDescription()}
        </p>

        {/* Détails techniques */}
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
          <div className="text-sm text-red-800">
            <div className="font-semibold mb-2">Détails :</div>
            
            {type === 'role' && current && (
              <div className="mb-2">
                <span className="font-medium">Votre rôle :</span> 
                <span className="ml-2 px-2 py-1 bg-red-100 rounded text-xs">
                  {current}
                </span>
              </div>
            )}
            
            <div>
              <span className="font-medium">
                {type === 'role' ? 'Rôle(s) requis :' : 'Permission(s) requise(s) :'}
              </span>
              <div className="mt-1 flex flex-wrap gap-1">
                {required.map((item, index) => (
                  <span 
                    key={index}
                    className="px-2 py-1 bg-red-100 rounded text-xs"
                  >
                    {item}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="space-y-3">
          <Button
            onClick={() => navigate(-1)}
            variant="outline"
            className="w-full"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Retour
          </Button>
          
          <Button
            onClick={() => navigate('/')}
            className="w-full"
          >
            <Home className="w-4 h-4 mr-2" />
            Accueil
          </Button>
        </div>

        {/* Message d'aide */}
        <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <p className="text-sm text-blue-800">
            <span className="font-semibold">Besoin d'accès ?</span>
            <br />
            Contactez votre administrateur pour obtenir les permissions nécessaires.
          </p>
        </div>
      </div>
    </div>
  );
};

export default AccessDenied;
