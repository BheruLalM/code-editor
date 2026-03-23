import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import toast from 'react-hot-toast';
import api from '../../api/axios';
import BackButton from '../../components/BackButton';
import MonacoEditor from '../../components/MonacoEditor';
import TestResults from '../../components/TestResults';

export default function CandidateResultPage() {
    const { id } = useParams();
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(true);
    const [assigning, setAssigning] = useState(false);
    const [newLinks, setNewLinks] = useState([]);

    useEffect(() => {
        api.get(`/admin/candidates/${id}`)
            .then(res => setResult(res.data))
            .catch(() => toast.error("Failed to load result"))
            .finally(() => setLoading(false));
    }, [id]);

    const copyCode = () => {
        if (result?.submitted_code) {
            navigator.clipboard.writeText(result.submitted_code);
            toast.success("Code copied!");
        }
    };

    const assignExtraProblems = async () => {
        setAssigning(true);
        try {
            const res = await api.post(`/admin/candidates/${id}/assign-extra`);
            setNewLinks(res.data.new_links);
            toast.success("Successfully assigned 2 extra problems!");
        } catch (error) {
            toast.error(error.response?.data?.detail || "Failed to assign extra problems");
        } finally {
            setAssigning(false);
        }
    };

    if (loading) return <div className="min-h-screen bg-darkBg text-white p-10 flex justify-center">Loading...</div>;
    if (!result) return <div className="min-h-screen bg-darkBg text-red-400 p-10">Result not found</div>;

    const timeStr = result.time_taken_seconds 
        ? `${Math.floor(result.time_taken_seconds/60)}m ${result.time_taken_seconds%60}s` 
        : '--';

    const renderScoreCircle = () => {
        const score = result.score ?? 0;
        let color = 'text-green-500 border-green-500 shadow-green-500/20';
        if (score < 50) color = 'text-red-500 border-red-500 shadow-red-500/20';
        else if (score < 75) color = 'text-amber-500 border-amber-500 shadow-amber-500/20';

        if (result.status !== 'submitted') {
            return (
                <div className="w-24 h-24 rounded-full border-4 border-gray-700 flex items-center justify-center flex-col shrink-0">
                    <span className="text-gray-500 text-sm text-center px-2">Not<br/>Submitted</span>
                </div>
            );
        }

        return (
            <div className={`w-24 h-24 rounded-full border-4 flex flex-col items-center justify-center shadow-lg bg-darkBg shrink-0 ${color}`}>
                <span className="text-3xl font-bold tracking-tighter">{score.toFixed(0)}</span>
                <span className="text-[10px] text-gray-400 uppercase tracking-widest mt-1">Score</span>
            </div>
        );
    };

    return (
        <div className="min-h-screen bg-darkBg text-white p-6 md:p-10">
            <div className="max-w-6xl mx-auto space-y-6">
                <BackButton />
                
                <div className="bg-cardBg border border-gray-800 rounded-xl p-6 shadow flex flex-col md:flex-row gap-6 justify-between items-start md:items-center">
                    <div>
                        <h1 className="text-3xl font-bold mb-1">{result.candidate_name}</h1>
                        <div className="text-gray-400 mb-4">{result.candidate_email}</div>
                        <button 
                            onClick={assignExtraProblems}
                            disabled={assigning}
                            className="bg-accent hover:bg-blue-600 disabled:opacity-50 text-white px-4 py-2 rounded text-sm font-medium transition"
                        >
                            {assigning ? 'Assigning...' : 'Assign 2 More Problems'}
                        </button>
                    </div>
                    {renderScoreCircle()}
                </div>

                {newLinks.length > 0 && (
                    <div className="bg-green-900/20 border border-green-800 p-4 rounded-lg space-y-2">
                        <h3 className="text-green-400 font-bold">New Test Links Generated:</h3>
                        {newLinks.map((token) => (
                            <div key={token} className="flex items-center justify-between bg-darkBg p-3 rounded border border-gray-800">
                                <span className="font-mono text-sm text-gray-300">{window.location.origin}/test/{token}</span>
                                <button 
                                    onClick={() => {
                                        navigator.clipboard.writeText(`${window.location.origin}/test/${token}`);
                                        toast.success("Link copied!");
                                    }}
                                    className="text-xs text-accent hover:text-white px-4 py-2 bg-gray-800 rounded transition font-medium"
                                >
                                    Copy Link
                                </button>
                            </div>
                        ))}
                    </div>
                )}

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="bg-[#111827] border border-gray-800 p-4 rounded-lg">
                        <div className="text-xs text-gray-500 mb-1 uppercase tracking-wider">Problem</div>
                        <div className="font-semibold truncate" title={result.problem?.title}>{result.problem?.title || 'Unknown'}</div>
                        {result.problem && (
                            <div className="text-xs mt-1 text-gray-400 capitalize">{result.problem.difficulty}</div>
                        )}
                    </div>
                    <div className="bg-[#111827] border border-gray-800 p-4 rounded-lg">
                        <div className="text-xs text-gray-500 mb-1 uppercase tracking-wider">Language</div>
                        <div className="font-semibold capitalize">{result.language || 'Not started'}</div>
                    </div>
                    <div className="bg-[#111827] border border-gray-800 p-4 rounded-lg">
                        <div className="text-xs text-gray-500 mb-1 uppercase tracking-wider">Time Taken</div>
                        <div className="font-semibold font-mono">{timeStr}</div>
                    </div>
                    <div className="bg-[#111827] border border-gray-800 p-4 rounded-lg">
                        <div className="text-xs text-gray-500 mb-1 uppercase tracking-wider">Submitted</div>
                        <div className="font-semibold text-sm">
                            {result.submitted_at ? new Date(result.submitted_at).toLocaleString() : '--'}
                        </div>
                    </div>
                </div>

                {result.status === 'submitted' ? (
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">
                        {/* Left Col: Test Results */}
                        <div className="bg-cardBg border border-gray-800 rounded-lg p-6">
                            <h2 className="text-xl font-bold mb-4 flex items-center justify-between">
                                <span>Test Results</span>
                                <span className="text-sm font-normal text-gray-400 bg-darkBg px-3 py-1 rounded">
                                    {result.passed_cases}/{result.total_cases} passed
                                </span>
                            </h2>
                            <div className="mb-4 h-2 w-full bg-gray-800 rounded overflow-hidden">
                                <div 
                                    className="h-full bg-accent transition-all duration-1000" 
                                    style={{ width: `${(result.passed_cases/result.total_cases)*100}%` }}
                                ></div>
                            </div>
                            
                            {result.test_results && (
                                <TestResults 
                                    results={result.test_results.visible} 
                                    hiddenPassed={result.test_results.hidden_passed}
                                    hiddenTotal={result.test_results.hidden_total}
                                />
                            )}
                        </div>

                        {/* Right Col: Code */}
                        <div className="bg-cardBg border border-gray-800 rounded-lg flex flex-col h-[700px] overflow-hidden">
                            <div className="p-4 border-b border-gray-800 bg-[#172036] flex justify-between items-center">
                                <div className="flex items-center space-x-2">
                                    <h2 className="font-bold">Submitted Code</h2>
                                    <span className="bg-darkBg border border-gray-700 text-gray-300 px-2 py-0.5 rounded text-xs capitalize">
                                        {result.language}
                                    </span>
                                </div>
                                <button onClick={copyCode} className="text-sm text-accent hover:text-blue-400 transition flex items-center space-x-1">
                                    <span>Copy Code</span>
                                </button>
                            </div>
                            <div className="flex-1 bg-darkBg relative">
                                {result.submitted_code ? (
                                    <MonacoEditor 
                                        value={result.submitted_code} 
                                        language={result.language} 
                                        readOnly={true} 
                                    />
                                ) : (
                                    <div className="absolute inset-0 flex items-center justify-center text-gray-500 italic">
                                        Candidate has not submitted code yet.
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>
                ) : (
                    <div className="bg-cardBg border border-gray-800 p-10 rounded-lg text-center">
                        <div className="text-gray-400 text-lg">Candidate has not submitted a solution yet.</div>
                        <div className="text-sm text-gray-500 mt-2">Current Status: <span className="capitalize">{result.status}</span></div>
                    </div>
                )}
            </div>
        </div>
    );
}
