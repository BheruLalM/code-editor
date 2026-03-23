import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import { Copy, RefreshCw, Download } from 'lucide-react';
import api from '../../api/axios';
import BackButton from '../../components/BackButton';

export default function SessionDetailPage() {
    const { id } = useParams();
    const [session, setSession] = useState(null);
    const [candidates, setCandidates] = useState([]);
    const [loading, setLoading] = useState(true);
    const [lastUpdated, setLastUpdated] = useState(0);

    const loadData = async (silent = false) => {
        try {
            const [sessRes, candsRes] = await Promise.all([
                api.get(`/admin/sessions/${id}`),
                api.get(`/admin/candidates/?session_id=${id}`)
            ]);
            setSession(sessRes.data);
            setCandidates(candsRes.data);
            setLastUpdated(0);
        } catch (error) {
            if (!silent) toast.error("Failed to load session data");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadData();
        const pollInt = setInterval(() => loadData(true), 30000);
        const secInt = setInterval(() => setLastUpdated(p => p + 1), 1000);
        return () => {
            clearInterval(pollInt);
            clearInterval(secInt);
        };
    }, [id]);

    const copyLink = () => {
        navigator.clipboard.writeText(session.shareable_link);
        toast.success("Link copied!");
    };

    const downloadCSV = () => {
        const headers = ["#,Name,Email,Problem,Score,Status,Time Taken,Language"];
        const rows = candidates.map((c, i) => {
            const time = c.time_taken_seconds ? `${Math.floor(c.time_taken_seconds/60)}m ${c.time_taken_seconds%60}s` : '--';
            return `"${i+1}","${c.candidate_name}","${c.candidate_email}","${c.problem_title}","${c.score ?? '--'}","${c.status}","${time}","${c.language ?? '--'}"`;
        });
        const csv = headers.concat(rows).join("\n");
        const blob = new Blob([csv], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `session-${id}-results.csv`;
        a.click();
    };

    if (loading) return <div className="min-h-screen bg-darkBg text-white p-10 flex justify-center">Loading...</div>;
    if (!session) return <div className="min-h-screen bg-darkBg text-red-400 p-10">Session not found</div>;

    const getScoreBadge = (score) => {
        if (score === null) return <span className="text-gray-500 font-mono">--</span>;
        if (score < 50) return <span className="bg-red-900/40 text-red-400 px-2 py-0.5 rounded font-mono border border-red-800">{score.toFixed(1)}</span>;
        if (score < 75) return <span className="bg-amber-900/40 text-amber-400 px-2 py-0.5 rounded font-mono border border-amber-800">{score.toFixed(1)}</span>;
        return <span className="bg-green-900/40 text-green-400 px-2 py-0.5 rounded font-mono border border-green-800">{score.toFixed(1)}</span>;
    };

    const getStatusPill = (status) => {
        switch(status) {
            case 'registered': return <span className="bg-gray-800 text-gray-300 px-2 py-0.5 rounded text-xs">Registered</span>;
            case 'started': return <span className="bg-blue-900/40 text-blue-400 border border-blue-800 px-2 py-0.5 rounded text-xs flex items-center w-fit"><span className="w-1.5 h-1.5 bg-blue-500 rounded-full animate-pulse mr-1"></span>Started</span>;
            case 'submitted': return <span className="bg-green-900/40 text-green-400 border border-green-800 px-2 py-0.5 rounded text-xs">Submitted</span>;
            case 'timed_out': return <span className="bg-red-900/40 text-red-400 border border-red-800 px-2 py-0.5 rounded text-xs">Timed Out</span>;
            default: return status;
        }
    };

    return (
        <div className="min-h-screen bg-darkBg text-white p-6 md:p-10">
            <div className="max-w-7xl mx-auto space-y-6">
                <BackButton to="/admin" />
                
                <div className="bg-cardBg border border-gray-800 rounded-xl p-6 shadow-md flex flex-wrap justify-between items-start gap-4">
                    <div>
                        <h1 className="text-3xl font-bold mb-3">{session.title}</h1>
                        <div className="flex space-x-3 mb-4">
                            <span className="bg-[#111827] border border-gray-700 px-3 py-1 text-sm rounded capitalize">{session.difficulty_filter}</span>
                            <span className="bg-[#111827] border border-gray-700 px-3 py-1 text-sm rounded">{session.time_limit_minutes}m limit</span>
                            {!session.is_active && <span className="bg-red-900/40 text-red-400 border border-red-800 px-3 py-1 text-sm rounded">Inactive</span>}
                        </div>
                        
                        <div className="flex items-center space-x-2">
                            <div className="bg-[#111827] border border-gray-700 px-4 py-2 rounded text-sm font-mono text-accent">
                                {session.shareable_link}
                            </div>
                            <button onClick={copyLink} className="p-2 border border-gray-700 rounded hover:bg-gray-800 transition">
                                <Copy size={18} />
                            </button>
                        </div>
                    </div>
                    
                    <div className="flex bg-[#111827] border border-gray-800 rounded-lg overflow-hidden shrink-0">
                        <div className="p-4 border-r border-gray-800 text-center min-w-[100px]">
                            <div className="text-xs text-gray-400">Registered</div>
                            <div className="text-2xl font-bold font-mono">{session.candidate_count}</div>
                        </div>
                        <div className="p-4 border-r border-gray-800 text-center min-w-[100px]">
                            <div className="text-xs text-gray-400">Submitted</div>
                            <div className="text-2xl font-bold font-mono">{session.submitted_count}</div>
                        </div>
                        <div className="p-4 border-r border-gray-800 text-center min-w-[100px]">
                            <div className="text-xs text-gray-400">Avg Score</div>
                            <div className="text-2xl font-bold font-mono text-accent">{session.avg_score !== null ? session.avg_score.toFixed(1) : '--'}</div>
                        </div>
                        <div className="p-4 text-center min-w-[100px]">
                            <div className="text-xs text-gray-400">Best Score</div>
                            <div className="text-2xl font-bold font-mono text-green-400">{session.best_score ?? '--'}</div>
                        </div>
                    </div>
                </div>

                <div className="bg-cardBg border border-gray-800 rounded-xl shadow-md overflow-hidden">
                    <div className="p-5 border-b border-gray-800 bg-[#172036] flex justify-between items-center">
                        <div className="flex items-center space-x-4">
                            <h2 className="text-xl font-bold">Candidates</h2>
                            <span className="text-xs text-gray-400">Last updated: {lastUpdated}s ago</span>
                        </div>
                        <div className="flex space-x-3">
                            <button onClick={() => loadData()} className="p-2 border border-gray-700 rounded hover:bg-gray-800 transition" title="Refresh">
                                <RefreshCw size={18} className="text-gray-300" />
                            </button>
                            <button onClick={downloadCSV} className="flex items-center space-x-2 bg-gray-800 hover:bg-gray-700 px-3 py-1.5 rounded transition border border-gray-700 font-medium text-sm">
                                <Download size={16} />
                                <span>Export CSV</span>
                            </button>
                        </div>
                    </div>

                    {candidates.length === 0 ? (
                        <div className="p-10 text-center text-gray-400">No candidates have joined this session yet.</div>
                    ) : (
                        <div className="overflow-x-auto">
                            <table className="w-full text-left">
                                <thead className="bg-[#111827] text-gray-400 text-xs uppercase tracking-wider">
                                    <tr>
                                        <th className="p-4 border-b border-gray-800">#</th>
                                        <th className="p-4 border-b border-gray-800">Candidate</th>
                                        <th className="p-4 border-b border-gray-800">Problem</th>
                                        <th className="p-4 border-b border-gray-800">Score</th>
                                        <th className="p-4 border-b border-gray-800">Status</th>
                                        <th className="p-4 border-b border-gray-800 text-center">Time Taken</th>
                                        <th className="p-4 border-b border-gray-800">Lang</th>
                                        <th className="p-4 border-b border-gray-800 text-right">Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {candidates.map((c, i) => (
                                        <tr key={c.id} className="border-b border-gray-800/50 hover:bg-[#233150] transition">
                                            <td className="p-4 text-gray-400 text-sm">{i + 1}</td>
                                            <td className="p-4">
                                                <div className="font-semibold">{c.candidate_name}</div>
                                                <div className="text-xs text-gray-500">{c.candidate_email}</div>
                                            </td>
                                            <td className="p-4 text-sm truncate max-w-[150px]" title={c.problem_title}>
                                                {c.problem_title}
                                            </td>
                                            <td className="p-4">
                                                {getScoreBadge(c.score)}
                                            </td>
                                            <td className="p-4">
                                                {getStatusPill(c.status)}
                                            </td>
                                            <td className="p-4 text-center font-mono text-sm text-gray-300">
                                                {c.time_taken_seconds ? `${Math.floor(c.time_taken_seconds/60)}m ${c.time_taken_seconds%60}s` : '--'}
                                            </td>
                                            <td className="p-4 text-sm text-gray-400 capitalize">{c.language || '--'}</td>
                                            <td className="p-4 text-right">
                                                <Link 
                                                    to={`/admin/candidates/${c.id}`}
                                                    className={`px-3 py-1.5 rounded text-sm font-medium border transition inline-block
                                                        ${c.status === 'submitted' 
                                                            ? 'border-accent text-accent hover:bg-accent/10' 
                                                            : 'border-gray-700 text-gray-500 cursor-not-allowed pointer-events-none'}`}
                                                >
                                                    View Code
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
