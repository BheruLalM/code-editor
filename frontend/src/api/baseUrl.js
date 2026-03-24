const LOCAL_API = 'http://localhost:8000';

function normalizeUrl(url) {
    if (!url || typeof url !== 'string') return '';
    return url.trim().replace(/\/+$/, '');
}

export function getApiBaseUrl() {
    const envUrl = normalizeUrl(import.meta.env.VITE_API_URL);
    if (envUrl) return envUrl;

    if (typeof window !== 'undefined') {
        const runtimeUrl = normalizeUrl(window.__CODEARENA_API_URL);
        if (runtimeUrl) return runtimeUrl;
    }

    return LOCAL_API;
}
