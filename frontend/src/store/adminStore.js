import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export const useAdminStore = create(
    persist(
        (set) => ({
            admin: { username: 'admin', full_name: 'Administrator' },
            token: 'dummy-token',
            isAuthenticated: true,
            login: () => {}, // No-op
            logout: () => {}, // No-op
            setAdmin: (admin) => set({ admin }),
        }),
        {
            name: 'codearena-admin',
        }
    )
);
