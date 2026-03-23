import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import { Copy, Plus } from 'lucide-react';
import api from '../../api/axios';
import { useAdminStore } from '../../store/adminStore';

export default function AdminDashboard() {
    const admin = useAdminStore(state => state.admin);
    const logout = useAdminStore(state => state.logout);
    const navigate = useNavigate();
    
    const [health, setHealth] = useState(null);
    const [sessions, setSessions] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchData();
        fetchHealth();
    }, []);

    const fetchHealth = async () => {
        try {
            const res = await api.get('/health');
            setHealth(res.data.docker);
        } catch (e) {
            setHealth({ status: 'offline' });
        }
    };

    const fetchData = async () => {
        try {
            const res = await api.get('/admin/sessions/');
            setSessions(res.data);
        } catch (error) {
            toast.error("Failed to load sessions");
        } finally {
            setLoading(false);
        }
    };

    const handleLogout = () => {
        logout();
        navigate('/admin/login');
    };

    const toggleActive = async (id, currentStatus) => {
        try {
            await api.patch(`/admin/sessions/${id}`, { is_active: !currentStatus });
            setSessions(sessions.map(s => s.id === id ? { ...s, is_active: !currentStatus } : s));
            toast.success("Session updated");
        } catch (e) {
            toast.error("Status update failed");
        }
    };

    const copyLink = (token) => {
        const url = `${window.location.origin}/test/${token}`;
        navigator.clipboard.writeText(url);
        toast.success("Link copied!");
    };

    const totalCands = sessions.reduce((acc, s) => acc + s.candidate_count, 0);
    const totalSubs = sessions.reduce((acc, s) => acc + s.submitted_count, 0);
    const scoreSessions = sessions.filter(s => s.avg_score !== null);
    const avgScoreTotal = scoreSessions.length ? (scoreSessions.reduce((acc, s) => acc + s.avg_score, 0) / scoreSessions.length).toFixed(1) : '--';

    const getDockerPill = () => {
        if (!health) return <span className="bg-gray-800 text-xs px-2 py-1 rounded">Checking Docker...</span>;
        if (health.status === 'running') {
            if (health.ready) {
                return <span className="bg-green-900/40 text-green-400 border border-green-800 text-xs px-3 py-1 rounded-full">Docker executor ready</span>;
            }
            const missingCount = (health.missing_images || []).length;
            return <span className="bg-amber-900/40 text-amber-400 border border-amber-800 text-xs px-3 py-1 rounded-full">Missing images: {missingCount}</span>;
        }
        return <span className="bg-red-900/40 text-red-400 border border-red-800 text-xs px-3 py-1 rounded-full">Docker offline</span>;
    };

    return (
        <div className="min-h-screen bg-darkBg flex flex-col">
            {/* Navbar */}
            <nav className="sticky top-0 z-10 bg-cardBg border-b border-gray-800 px-6 py-4 flex justify-between items-center shadow-md">
                <div className="flex items-center space-x-2">
                    <span className="text-accent font-mono text-xl font-bold">&lt; /&gt;</span>
                    <span className="font-bold text-lg">CodeArena Admin</span>
                </div>
                <div className="flex items-center space-x-4">
                    {getDockerPill()}
                    <span className="text-gray-300 ml-4 border-l border-gray-700 pl-4">{admin?.full_name}</span>
                    <button onClick={handleLogout} className="text-sm text-gray-400 hover:text-white transition">Logout</button>
                </div>
            </nav>

            <div className="p-8 flex-1 max-w-7xl mx-auto w-full">
                {/* Stats row */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
                    <div className="bg-cardBg p-5 rounded-lg border border-gray-800">
                        <div className="text-gray-400 text-sm mb-1">Total Sessions</div>
                        <div className="text-2xl font-bold">{sessions.length}</div>
                    </div>
                    <div className="bg-cardBg p-5 rounded-lg border border-gray-800">
                        <div className="text-gray-400 text-sm mb-1">Total Candidates</div>
                        <div className="text-2xl font-bold">{totalCands}</div>
                    </div>
                    <div className="bg-cardBg p-5 rounded-lg border border-gray-800">
                        <div className="text-gray-400 text-sm mb-1">Total Submitted</div>
                        <div className="text-2xl font-bold">{totalSubs}</div>
                    </div>
                    <div className="bg-cardBg p-5 rounded-lg border border-gray-800">
                        <div className="text-gray-400 text-sm mb-1">Avg Score</div>
                        <div className="text-2xl font-bold text-accent">{avgScoreTotal}</div>
                    </div>
                </div>

                {/* Sessions Table */}
                <div className="bg-cardBg rounded-lg border border-gray-800 overflow-hidden shadow-lg">
                    <div className="p-5 border-b border-gray-800 flex justify-between items-center bg-[#172036]">
                        <h2 className="text-lg font-bold">Your Test Sessions</h2>
                        <Link to="/admin/sessions/new" className="bg-accent hover:bg-blue-600 text-white px-4 py-2 rounded text-sm font-medium flex items-center space-x-1 transition">
                            <Plus size={16} />
                            <span>Create New Session</span>
                        </Link>
                    </div>

                    {loading ? (
                        <div className="p-10 text-center text-gray-400">Loading sessions...</div>
                    ) : sessions.length === 0 ? (
                        <div className="p-10 text-center text-gray-400">
                            No sessions yet. Create your first test session.
                        </div>
                    ) : (
                        <div className="overflow-x-auto">
                            <table className="w-full text-left border-collapse">
                                <thead>
                                    <tr className="bg-[#111827] text-gray-400 text-sm">
                                        <th className="p-4 font-medium border-b border-gray-800">Title</th>
                                        <th className="p-4 font-medium border-b border-gray-800 text-center">Difficulty</th>
                                        <th className="p-4 font-medium border-b border-gray-800 text-center">Time</th>
                                        <th className="p-4 font-medium border-b border-gray-800 text-center">Candidates</th>
                                        <th className="p-4 font-medium border-b border-gray-800 text-center">Submitted</th>
                                        <th className="p-4 font-medium border-b border-gray-800 text-center">Avg Score</th>
                                        <th className="p-4 font-medium border-b border-gray-800 text-center">Status</th>
                                        <th className="p-4 font-medium border-b border-gray-800 text-center">Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {sessions.map((s) => (
                                        <tr key={s.id} className="border-b border-gray-800/50 hover:bg-[#233150] transition">
                                            <td className="p-4 font-medium">{s.title}</td>
                                            <td className="p-4 text-center">
                                                <span className={`text-xs px-2 py-1 rounded uppercase tracking-wide font-bold
                                                    ${s.difficulty_filter === 'easy' ? 'bg-green-900/30 text-green-400' :
                                                      s.difficulty_filter === 'medium' ? 'bg-amber-900/30 text-amber-400' :
                                                      s.difficulty_filter === 'hard' ? 'bg-red-900/30 text-red-400' :
                                                      'bg-blue-900/30 text-blue-400'}`
                                                }>
                                                    {s.difficulty_filter}
                                                </span>
                                            </td>
                                            <td className="p-4 text-center text-gray-300">{s.time_limit_minutes}m</td>
                                            <td className="p-4 text-center">{s.candidate_count}</td>
                                            <td className="p-4 text-center">{s.submitted_count}</td>
                                            <td className="p-4 text-center font-mono">
                                                {s.avg_score !== null ? s.avg_score.toFixed(1) : '--'}
                                            </td>
                                            <td className="p-4 text-center">
                                                <button 
                                                    onClick={() => toggleActive(s.id, s.is_active)}
                                                    className={`text-xs px-2 py-1 rounded inline-block min-w-[60px] transition
                                                        ${s.is_active ? 'bg-green-900/30 text-green-400 hover:bg-green-900/50' : 'bg-red-900/30 text-red-400 hover:bg-red-900/50'}`}
                                                >
                                                    {s.is_active ? 'Active' : 'Inactive'}
                                                </button>
                                            </td>
                                            <td className="p-4 text-center space-x-3">
                                                <button onClick={() => copyLink(s.session_token)} className="text-gray-400 hover:text-white transition" title="Copy Link">
                                                    <Copy size={18} className="inline" />
                                                </button>
                                                <Link to={`/admin/sessions/${s.id}`} className="text-accent hover:text-blue-400 transition text-sm font-medium">
                                                    View Results
                                                </Link>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
