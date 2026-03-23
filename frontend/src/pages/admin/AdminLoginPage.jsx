import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import publicApi from '../../api/publicApi';
import { useAdminStore } from '../../store/adminStore';

export default function AdminLoginPage() {
    const [loading, setLoading] = useState(false);
    const [showPassword, setShowPassword] = useState(false);
    const login = useAdminStore(state => state.login);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        const username = e.target.username.value;
        const password = e.target.password.value;
        
        setLoading(true);
        try {
            const res = await publicApi.post('/admin/auth/login', { username, password });
            login(res.data.admin, res.data.access_token);
            navigate('/admin');
        } catch (error) {
            if (error.response?.status === 401) {
                toast.error("Invalid username or password");
            } else {
                toast.error("Something went wrong");
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-darkBg flex items-center justify-center p-4">
            <div className="bg-cardBg p-8 rounded-xl w-full max-w-[400px] shadow-2xl border border-gray-800">
                <div className="text-center mb-8">
                    <div className="text-accent font-mono text-3xl font-bold mb-2">&lt; /&gt; CodeArena</div>
                    <h2 className="text-gray-400 text-lg">Admin Portal</h2>
                </div>
                
                <form onSubmit={handleSubmit} className="space-y-5">
                    <div>
                        <label className="block text-sm font-medium text-gray-300 mb-1">Username</label>
                        <input 
                            name="username"
                            type="text" 
                            required
                            className="w-full bg-darkBg border border-gray-700 rounded p-2.5 text-white focus:border-accent focus:ring-1 focus:ring-accent outline-none transition"
                        />
                    </div>
                    
                    <div>
                        <label className="block text-sm font-medium text-gray-300 mb-1">Password</label>
                        <div className="relative">
                            <input 
                                name="password"
                                type={showPassword ? "text" : "password"} 
                                required
                                className="w-full bg-darkBg border border-gray-700 rounded p-2.5 text-white focus:border-accent focus:ring-1 focus:ring-accent outline-none transition pr-10"
                            />
                            <button 
                                type="button"
                                className="absolute right-3 top-3 text-gray-400 hover:text-white"
                                onClick={() => setShowPassword(!showPassword)}
                            >
                                {showPassword ? 'Hide' : 'Show'}
                            </button>
                        </div>
                    </div>
                    
                    <button 
                        type="submit" 
                        disabled={loading}
                        className="w-full bg-accent hover:bg-blue-700 text-white font-medium py-2.5 rounded transition disabled:opacity-50"
                    >
                        {loading ? 'Signing in...' : 'Sign In'}
                    </button>
                </form>
            </div>
        </div>
    );
}
