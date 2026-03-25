import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import { Copy, Plus, Users, Clock, Trash2, CheckCircle2, PlayCircle } from 'lucide-react';
import api from '../../api/axios';
import publicApi from '../../api/publicApi';
import { useAdminStore } from '../../store/adminStore';

export default function AdminDashboard() {
    const admin = useAdminStore(state => state.admin);
    const logout = useAdminStore(state => state.logout);
    const navigate = useNavigate();
    
    const [health, setHealth] = useState(null);
    const [sessions, setSessions] = useState([]);
    const [waitingCandidates, setWaitingCandidates] = useState([]);
    const [allCandidates, setAllCandidates] = useState([]);
    const [problems, setProblems] = useState([]);
    
    const [loading, setLoading] = useState(true);
    const [activeTab, setActiveTab] = useState('waiting');
    
    const [showAssignModal, setShowAssignModal] = useState(false);
    const [selectedCandidate, setSelectedCandidate] = useState(null);
    const [selectedProblemIds, setSelectedProblemIds] = useState([]);
    const [timeLimit, setTimeLimit] = useState(45);

    useEffect(() => {
        fetchData();
        fetchHealth();
        fetchProblems();
    }, []);

    useEffect(() => {
        if (activeTab === 'waiting') fetchWaiting();
        if (activeTab === 'candidates') fetchAllCandidates();
        if (activeTab === 'sessions') fetchSessions();
    }, [activeTab]);

    const fetchHealth = async () => {
        try {
            const res = await api.get('/health');
            setHealth(res.data.docker);
        } catch (e) {
            setHealth({ status: 'offline' });
        }
    };

    const fetchData = async () => {
        setLoading(true);
        await Promise.all([fetchSessions(), fetchWaiting(), fetchAllCandidates()]);
        setLoading(false);
    };

    const fetchSessions = async () => {
        try {
            const res = await api.get('/admin/sessions/');
            setSessions(res.data);
        } catch (error) {
            toast.error("Failed to load sessions");
        }
    };

    const fetchWaiting = async () => {
        try {
            const res = await api.get('/admin/candidates/waiting');
            setWaitingCandidates(res.data);
        } catch (error) {
            console.error("Waiting fetch failed", error);
        }
    };

    const fetchAllCandidates = async () => {
        try {
            const res = await api.get('/admin/candidates/');
            setAllCandidates(res.data);
        } catch (error) {
            console.error("Candidates fetch failed", error);
        }
    };

    const fetchProblems = async () => {
        try {
            const res = await publicApi.get('/problems/');
            setProblems(res.data);
        } catch (error) {
            console.error("Problems fetch failed", error);
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

    const copyApplyLink = () => {
        const url = `${window.location.origin}/apply`;
        navigator.clipboard.writeText(url);
        toast.success("Registration link copied!");
    };

    const handleDeleteCandidate = async (id) => {
        if (!window.confirm("Delete this candidate and all results? This cannot be undone.")) return;
        try {
            await api.delete(`/admin/candidates/${id}`);
            toast.success("Deleted");
            fetchAllCandidates();
            fetchWaiting();
        } catch (e) {
            toast.error("Delete failed");
        }
    };

    const handleAssign = async () => {
        if (selectedProblemIds.length === 0) {
            toast.error("Select at least one problem");
            return;
        }
        try {
            await api.post(`/admin/candidates/${selectedCandidate.id}/assign`, {
                problem_ids: selectedProblemIds,
                time_limit_minutes: timeLimit
            });
            toast.success("Test assigned!");
            setShowAssignModal(false);
            fetchWaiting();
            fetchAllCandidates();
        } catch (e) {
            toast.error(e.response?.data?.detail || "Assignment failed");
        }
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
        <div className="min-h-screen bg-darkBg flex flex-col text-white">
            {/* Navbar */}
            <nav className="sticky top-0 z-10 bg-cardBg border-b border-gray-800 px-6 py-4 flex justify-between items-center shadow-md">
                <div className="flex items-center space-x-2">
                    <span className="text-accent font-mono text-xl font-bold">&lt; /&gt;</span>
                    <span className="font-bold text-lg">CodeArena Admin</span>
                </div>
                <div className="flex items-center space-x-6">
                    <button onClick={copyApplyLink} className="text-xs bg-gray-800 hover:bg-gray-700 px-3 py-1.5 rounded-lg border border-gray-700 transition flex items-center space-x-2">
                        <Copy size={14} />
                        <span>Registration Link</span>
                    </button>
                    {getDockerPill()}
                    <div className="h-6 w-[1px] bg-gray-800"></div>
                    <span className="text-gray-300">{admin?.full_name}</span>
                    <button onClick={handleLogout} className="text-sm text-gray-400 hover:text-white transition">Logout</button>
                </div>
            </nav>

            <div className="p-8 flex-1 max-w-7xl mx-auto w-full">
                {/* Tabs */}
                <div className="flex space-x-1 bg-darkBg p-1 rounded-xl border border-gray-800 mb-8 w-fit">
                    {[
                        { id: 'waiting', label: 'Waiting Room', icon: Clock, count: waitingCandidates.length },
                        { id: 'candidates', label: 'All Candidates', icon: Users, count: allCandidates.length },
                        { id: 'sessions', label: 'Legacy Sessions', icon: PlayCircle, count: sessions.length }
                    ].map(tab => (
                        <button
                            key={tab.id}
                            onClick={() => setActiveTab(tab.id)}
                            className={`flex items-center space-x-2 px-6 py-2.5 rounded-lg font-bold text-sm transition-all
                                ${activeTab === tab.id 
                                    ? 'bg-accent text-white shadow-lg shadow-blue-500/20' 
                                    : 'text-gray-500 hover:text-gray-300 hover:bg-gray-800/50'}`}
                        >
                            <tab.icon size={16} />
                            <span>{tab.label}</span>
                            {tab.count > 0 && (
                                <span className={`ml-2 text-[10px] px-1.5 py-0.5 rounded-full ${activeTab === tab.id ? 'bg-white/20' : 'bg-gray-800'}`}>
                                    {tab.count}
                                </span>
                            )}
                        </button>
                    ))}
                </div>

                {loading ? (
                    <div className="flex flex-col items-center justify-center h-64 space-y-4">
                        <div className="w-10 h-10 border-4 border-accent border-t-transparent rounded-full animate-spin"></div>
                        <div className="text-gray-500 font-medium tracking-widest uppercase text-xs">Fetching Data...</div>
                    </div>
                ) : (
                    <>
                        {/* WAITING ROOM TAB */}
                        {activeTab === 'waiting' && (
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
                                {waitingCandidates.length === 0 ? (
                                    <div className="col-span-full bg-cardBg border border-dashed border-gray-700 p-16 rounded-2xl text-center">
                                        <div className="bg-gray-800 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                                            <Clock className="text-gray-500" size={32} />
                                        </div>
                                        <h3 className="text-xl font-bold mb-2">Waiting Room is Empty</h3>
                                        <p className="text-gray-500 max-w-sm mx-auto">New candidates will appear here once they register using the shared registration link.</p>
                                        <button onClick={copyApplyLink} className="mt-6 text-accent hover:underline text-sm font-medium">Copy Registration Link</button>
                                    </div>
                                ) : (
                                    waitingCandidates.map(cand => (
                                        <div key={cand.id} className="bg-cardBg border border-gray-800 rounded-2xl p-6 hover:border-accent/50 transition-all group relative overflow-hidden shadow-xl">
                                            <div className="absolute top-0 right-0 p-4 opacity-0 group-hover:opacity-100 transition-opacity">
                                                <button onClick={() => handleDeleteCandidate(cand.id)} className="text-gray-600 hover:text-red-500 p-2">
                                                    <Trash2 size={18} />
                                                </button>
                                            </div>
                                            <div className="flex items-center space-x-4 mb-6">
                                                <div className="w-12 h-12 bg-accent/10 rounded-full flex items-center justify-center text-accent font-bold text-xl uppercase">
                                                    {cand.candidate_name[0]}
                                                </div>
                                                <div>
                                                    <h3 className="font-bold text-lg">{cand.candidate_name}</h3>
                                                    <p className="text-sm text-gray-500">{cand.candidate_email}</p>
                                                </div>
                                            </div>
                                            <div className="flex items-center justify-between pt-4 border-t border-gray-800">
                                                <div className="text-xs text-gray-500 flex items-center space-x-1">
                                                    <Clock size={12} />
                                                    <span>Joined {new Date(cand.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                                                </div>
                                                <button 
                                                    onClick={() => {
                                                        setSelectedCandidate(cand);
                                                        setShowAssignModal(true);
                                                    }}
                                                    className="bg-accent hover:bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-bold transition shadow-lg shadow-blue-500/10"
                                                >
                                                    Assign Test
                                                </button>
                                            </div>
                                        </div>
                                    ))
                                )}
                            </div>
                        )}

                        {/* ALL CANDIDATES TAB */}
                        {activeTab === 'candidates' && (
                            <div className="bg-cardBg rounded-2xl border border-gray-800 overflow-hidden shadow-2xl animate-in fade-in duration-500">
                                <div className="overflow-x-auto">
                                    <table className="w-full text-left">
                                        <thead>
                                            <tr className="bg-[#111827] text-gray-500 text-[11px] uppercase tracking-widest font-bold">
                                                <th className="p-5">Candidate</th>
                                                <th className="p-5">Status</th>
                                                <th className="p-5 text-center">Problems</th>
                                                <th className="p-5 text-center">Score</th>
                                                <th className="p-5 text-right">Actions</th>
                                            </tr>
                                        </thead>
                                        <tbody className="divide-y divide-gray-800/50">
                                            {allCandidates.map(cand => (
                                                <tr key={cand.id} className="hover:bg-gray-800/30 transition-colors">
                                                    <td className="p-5">
                                                        <div className="font-bold">{cand.candidate_name}</div>
                                                        <div className="text-xs text-gray-500 italic">{cand.candidate_email}</div>
                                                    </td>
                                                    <td className="p-5">
                                                        <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold uppercase border
                                                            ${cand.status === 'submitted' ? 'bg-green-900/30 text-green-400 border-green-800' :
                                                              cand.status === 'started' ? 'bg-blue-900/30 text-blue-400 border-blue-800' :
                                                              cand.status === 'timed_out' ? 'bg-red-900/30 text-red-400 border-red-800' :
                                                              'bg-gray-800 text-gray-400 border-gray-700'}`}>
                                                            {cand.status}
                                                        </span>
                                                    </td>
                                                    <td className="p-5 text-center font-mono text-sm">{cand.problems_count}</td>
                                                    <td className="p-5 text-center">
                                                        {cand.score !== null ? (
                                                            <div className={`font-mono font-bold text-lg ${cand.score >= 70 ? 'text-green-400' : cand.score >= 40 ? 'text-amber-400' : 'text-red-400'}`}>
                                                                {cand.score.toFixed(0)}%
                                                            </div>
                                                        ) : <span className="text-gray-600">--</span>}
                                                    </td>
                                                    <td className="p-5 text-right space-x-4">
                                                        <Link to={`/admin/candidates/${cand.id}`} className="text-accent hover:underline text-sm font-bold">Report</Link>
                                                        <button onClick={() => handleDeleteCandidate(cand.id)} className="text-gray-600 hover:text-red-500 transition">
                                                            <Trash2 size={16} />
                                                        </button>
                                                    </td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        )}

                        {/* LEGACY SESSIONS TAB */}
                        {activeTab === 'sessions' && (
                             <div className="bg-cardBg rounded-2xl border border-gray-800 overflow-hidden shadow-2xl">
                                <div className="p-6 border-b border-gray-800 flex justify-between items-center bg-[#172036]">
                                    <h2 className="font-bold flex items-center space-x-2">
                                        <PlayCircle size={18} className="text-accent" />
                                        <span>Automated Test Sessions</span>
                                    </h2>
                                    <Link to="/admin/sessions/new" className="bg-accent hover:bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-bold transition flex items-center space-x-2">
                                        <Plus size={16} />
                                        <span>New Session</span>
                                    </Link>
                                </div>
                                <div className="overflow-x-auto">
                                    <table className="w-full text-left">
                                        <thead className="bg-[#111827] text-gray-500 text-[11px] uppercase tracking-widest font-bold">
                                            <tr>
                                                <th className="p-5">Title</th>
                                                <th className="p-5 text-center">Difficulty</th>
                                                <th className="p-5 text-center">Stats</th>
                                                <th className="p-5 text-center">Status</th>
                                                <th className="p-5 text-right">Actions</th>
                                            </tr>
                                        </thead>
                                        <tbody className="divide-y divide-gray-800/50">
                                            {sessions.map(s => (
                                                <tr key={s.id} className="hover:bg-gray-800/30 transition-colors">
                                                    <td className="p-5 font-bold">{s.title}</td>
                                                    <td className="p-5 text-center">
                                                        <span className="text-[10px] bg-gray-800 px-2 py-0.5 rounded uppercase font-bold text-gray-400">{s.difficulty_filter}</span>
                                                    </td>
                                                    <td className="p-5 text-center text-xs text-gray-400">
                                                        {s.submitted_count}/{s.candidate_count} Subs
                                                    </td>
                                                    <td className="p-5 text-center">
                                                        <button 
                                                            onClick={() => toggleActive(s.id, s.is_active)}
                                                            className={`text-[10px] px-2 py-0.5 rounded-full font-bold uppercase transition outline-none
                                                                ${s.is_active ? 'bg-green-900/30 text-green-400 border border-green-800' : 'bg-red-900/30 text-red-400 border border-red-800'}`}
                                                        >
                                                            {s.is_active ? 'Active' : 'Paused'}
                                                        </button>
                                                    </td>
                                                    <td className="p-5 text-right space-x-4">
                                                        <button onClick={() => copyLink(s.session_token)} title="Copy Session Link" className="text-gray-500 hover:text-white transition"><Copy size={16} /></button>
                                                        <Link to={`/admin/sessions/${s.id}`} className="text-accent hover:underline text-sm font-bold">Results</Link>
                                                    </td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                             </div>
                        )}
                    </>
                )}
            </div>

            {/* ASSIGN TEST MODAL */}
            {showAssignModal && (
                <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md">
                    <div className="bg-cardBg border border-gray-800 w-full max-w-2xl rounded-3xl overflow-hidden shadow-[0_0_50px_rgba(0,0,0,0.5)] animate-in zoom-in-95 duration-200">
                        <div className="p-8 border-b border-gray-800 flex justify-between items-center bg-[#172036]">
                            <div>
                                <h2 className="text-2xl font-bold">Assign Problems</h2>
                                <p className="text-sm text-gray-400">For {selectedCandidate?.candidate_name}</p>
                            </div>
                            <button onClick={() => setShowAssignModal(false)} className="text-gray-500 hover:text-white">
                                <Plus size={24} className="rotate-45" />
                            </button>
                        </div>
                        
                        <div className="p-8 space-y-8 max-h-[60vh] overflow-y-auto custom-scrollbar">
                            {/* Problem Selection */}
                            <div>
                                <h3 className="text-xs font-bold uppercase tracking-widest text-gray-500 mb-4">Select 1 or more problems</h3>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                                    {problems.map(p => {
                                        const isSelected = selectedProblemIds.includes(p.id);
                                        return (
                                            <div 
                                                key={p.id}
                                                onClick={() => {
                                                    if (isSelected) setSelectedProblemIds(selectedProblemIds.filter(id => id !== p.id));
                                                    else setSelectedProblemIds([...selectedProblemIds, p.id]);
                                                }}
                                                className={`p-4 rounded-xl border-2 cursor-pointer transition-all flex items-center justify-between
                                                    ${isSelected ? 'border-accent bg-accent/5' : 'border-gray-800 bg-[#0F172A] hover:border-gray-700'}`}
                                            >
                                                <div className="flex-1 min-w-0">
                                                    <div className="font-bold truncate">{p.title}</div>
                                                    <div className="text-[10px] text-gray-500 uppercase">{p.difficulty} • {p.tags?.[0] || 'Logic'}</div>
                                                </div>
                                                {isSelected && <CheckCircle2 className="text-accent shrink-0" size={20} />}
                                            </div>
                                        );
                                    })}
                                </div>
                            </div>

                            {/* Time Limit */}
                            <div>
                                <h3 className="text-xs font-bold uppercase tracking-widest text-gray-500 mb-4 flex items-center justify-between">
                                    <span>Time Limit (Minutes)</span>
                                    <span className="text-accent font-mono text-lg">{timeLimit}m</span>
                                </h3>
                                <input 
                                    type="range" 
                                    min="5" 
                                    max="180" 
                                    step="5"
                                    value={timeLimit}
                                    onChange={(e) => setTimeLimit(parseInt(e.target.value))}
                                    className="w-full h-2 bg-gray-800 rounded-lg appearance-none cursor-pointer accent-accent"
                                />
                                <div className="flex justify-between text-[10px] text-gray-600 mt-2 font-bold uppercase">
                                    <span>Short Sweep (5m)</span>
                                    <span>Deep Dive (3h)</span>
                                </div>
                            </div>
                        </div>

                        <div className="p-8 bg-[#0F172A] border-t border-gray-800 flex justify-end space-x-4">
                            <button 
                                onClick={() => setShowAssignModal(false)}
                                className="px-6 py-3 rounded-xl font-bold text-gray-400 hover:text-white transition"
                            >
                                Cancel
                            </button>
                            <button 
                                onClick={handleAssign}
                                disabled={selectedProblemIds.length === 0}
                                className="bg-accent hover:bg-blue-600 text-white px-10 py-3 rounded-xl font-bold transition shadow-lg shadow-blue-500/20 disabled:opacity-50"
                            >
                                Send Assignment →
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
