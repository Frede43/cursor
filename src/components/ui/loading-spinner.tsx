/**
 * Composant de chargement réutilisable
 */

import { cn } from '@/lib/utils';

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  className?: string;
  text?: string;
}

export const LoadingSpinner = ({ 
  size = 'md', 
  className,
  text = 'Chargement...' 
}: LoadingSpinnerProps) => {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12'
  };

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <div 
          className={cn(
            'animate-spin rounded-full border-t-2 border-b-2 border-primary mx-auto mb-4',
            sizeClasses[size],
            className
          )}
        />
        {text && (
          <p className="text-sm text-muted-foreground">{text}</p>
        )}
      </div>
    </div>
  );
};

export default LoadingSpinner;
