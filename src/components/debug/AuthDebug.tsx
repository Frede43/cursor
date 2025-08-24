import { useAuth } from '@/hooks/use-auth';
import { useLocation } from 'react-router-dom';
import { useEffect } from 'react';

export const AuthDebug = () => {
  const { user, isLoading, isAuthenticated } = useAuth();
  const location = useLocation();

  useEffect(() => {
    console.log('AuthDebug - State change:', {
      user,
      isLoading,
      isAuthenticated,
      pathname: location.pathname,
      localStorage: localStorage.getItem('user')
    });
  }, [user, isLoading, isAuthenticated, location.pathname]);

  const clearStorage = () => {
    localStorage.removeItem('user');
    window.location.reload();
  };

  return (
    <div className="fixed top-0 right-0 bg-red-100 p-4 text-xs z-50 max-w-xs">
      <h3 className="font-bold">Auth Debug</h3>
      <div>Path: {location.pathname}</div>
      <div>Loading: {isLoading ? 'true' : 'false'}</div>
      <div>Authenticated: {isAuthenticated ? 'true' : 'false'}</div>
      <div>User: {user ? user.username : 'null'}</div>
      <div>LocalStorage: {localStorage.getItem('user') ? 'exists' : 'null'}</div>
      <button 
        onClick={clearStorage}
        className="mt-2 px-2 py-1 bg-red-500 text-white text-xs rounded"
      >
        Clear & Reload
      </button>
    </div>
  );
};
