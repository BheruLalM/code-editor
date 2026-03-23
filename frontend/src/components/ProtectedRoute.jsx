import { useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';
import { useAdminStore } from '../store/adminStore';

export default function ProtectedRoute({ children }) {
    const isAuthenticated = useAdminStore(state => state.isAuthenticated);
    const [isRehydrated, setIsRehydrated] = useState(false);

    useEffect(() => {
        const timer = setTimeout(() => {
            setIsRehydrated(true);
        }, 150);
        return () => clearTimeout(timer);
    }, []);

    if (!isRehydrated) {
        return (
            <div className="flex items-center justify-center min-h-screen bg-darkBg text-white">
                Loading...
            </div>
        );
    }

    if (!isAuthenticated) {
        return <Navigate to="/admin/login" replace />;
    }

    return children;
}
