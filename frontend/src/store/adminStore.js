import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export const useAdminStore = create(
    persist(
        (set) => ({
            admin: null,
            token: null,
            isAuthenticated: false,
            login: (admin, token) => set({ admin, token, isAuthenticated: true }),
            logout: () => set({ admin: null, token: null, isAuthenticated: false }),
            setAdmin: (admin) => set({ admin }),
        }),
        {
            name: 'codearena-admin',
        }
    )
);
