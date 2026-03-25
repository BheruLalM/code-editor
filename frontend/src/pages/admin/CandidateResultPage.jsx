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
    const [selectedProblemIndex, setSelectedProblemIndex] = useState(0);

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

        return (
            <div className={`w-24 h-24 rounded-full border-4 flex flex-col items-center justify-center shadow-lg bg-darkBg shrink-0 ${color}`}>
                <span className="text-3xl font-bold tracking-tighter">{score.toFixed(0)}</span>
                <span className="text-[10px] text-gray-400 uppercase tracking-widest mt-1">Overall</span>
            </div>
        );
    };

    return (
        <div className="min-h-screen bg-darkBg text-white p-6 md:p-10">
            <div className="max-w-6xl mx-auto space-y-6">
                <BackButton />
                
                <div className="bg-cardBg border border-gray-800 rounded-xl p-6 shadow flex flex-col md:flex-row gap-6 justify-between items-start md:items-center">
                    <div>
                        <div className="flex items-center space-x-3 mb-1">
                             <h1 className="text-3xl font-bold">{result.candidate_name}</h1>
                             <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold uppercase border
                                ${result.status === 'submitted' ? 'bg-green-900/30 text-green-400 border-green-800' :
                                  result.status === 'started' ? 'bg-blue-900/30 text-blue-400 border-blue-800' :
                                  'bg-gray-800 text-gray-400 border-gray-700'}`}>
                                {result.status}
                            </span>
                        </div>
                        <div className="text-gray-400">{result.candidate_email}</div>
                    </div>
                    {renderScoreCircle()}
                </div>

                {/* Problem Selection Tabs */}
                {result.problems && result.problems.length > 0 && (
                    <div className="flex space-x-2 border-b border-gray-800 overflow-x-auto pb-1 custom-scrollbar">
                        {result.problems.map((p, idx) => (
                            <button
                                key={idx}
                                onClick={() => setSelectedProblemIndex(idx)}
                                className={`px-6 py-3 text-sm font-bold transition-all border-b-2 whitespace-nowrap
                                    ${selectedProblemIndex === idx 
                                        ? 'border-accent text-accent bg-accent/5' 
                                        : 'border-transparent text-gray-500 hover:text-gray-300'}`}
                            >
                                {p.title}
                            </button>
                        ))}
                    </div>
                )}

                {result.problems?.[selectedProblemIndex] && (() => {
                    const p = result.problems[selectedProblemIndex];
                    return (
                        <>
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                                <div className="bg-[#111827] border border-gray-800 p-4 rounded-lg">
                                    <div className="text-xs text-gray-500 mb-1 uppercase tracking-wider">Problem Status</div>
                                    <div className={`font-semibold capitalize ${p.status === 'submitted' ? 'text-green-400' : 'text-amber-400'}`}>{p.status}</div>
                                </div>
                                <div className="bg-[#111827] border border-gray-800 p-4 rounded-lg">
                                    <div className="text-xs text-gray-500 mb-1 uppercase tracking-wider">Language</div>
                                    <div className="font-semibold capitalize">{p.language || 'N/A'}</div>
                                </div>
                                <div className="bg-[#111827] border border-gray-800 p-4 rounded-lg">
                                    <div className="text-xs text-gray-500 mb-1 uppercase tracking-wider">Passed Cases</div>
                                    <div className="font-semibold font-mono">{p.passed_cases}/{p.total_cases}</div>
                                </div>
                                <div className="bg-[#111827] border border-gray-800 p-4 rounded-lg">
                                    <div className="text-xs text-gray-500 mb-1 uppercase tracking-wider">Problem Score</div>
                                    <div className="font-semibold text-accent">{p.score?.toFixed(1)}%</div>
                                </div>
                            </div>

                            {p.status === 'submitted' ? (
                                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">
                                    {/* Left Col: Test Results */}
                                    <div className="bg-cardBg border border-gray-800 rounded-lg p-6">
                                        <h2 className="text-xl font-bold mb-4 flex items-center justify-between">
                                            <span>Test Results</span>
                                            <span className="text-sm font-normal text-gray-400 bg-darkBg px-3 py-1 rounded">
                                                {p.passed_cases}/{p.total_cases} passed
                                            </span>
                                        </h2>
                                        <div className="mb-4 h-2 w-full bg-gray-800 rounded overflow-hidden">
                                            <div 
                                                className="h-full bg-accent transition-all duration-1000" 
                                                style={{ width: `${(p.passed_cases/p.total_cases)*100}%` }}
                                            ></div>
                                        </div>
                                        
                                        {p.test_results && (
                                            <TestResults 
                                                results={p.test_results.visible} 
                                                hiddenPassed={p.test_results.hidden_passed}
                                                hiddenTotal={p.test_results.hidden_total}
                                            />
                                        )}
                                    </div>

                                    {/* Right Col: Code */}
                                    <div className="bg-cardBg border border-gray-800 rounded-lg flex flex-col h-[700px] overflow-hidden">
                                        <div className="p-4 border-b border-gray-800 bg-[#172036] flex justify-between items-center">
                                            <div className="flex items-center space-x-2">
                                                <h2 className="font-bold">Submitted Code</h2>
                                                <span className="bg-darkBg border border-gray-700 text-gray-300 px-2 py-0.5 rounded text-xs capitalize">
                                                    {p.language}
                                                </span>
                                            </div>
                                            <button 
                                                onClick={() => {
                                                    navigator.clipboard.writeText(p.submitted_code);
                                                    toast.success("Code copied!");
                                                }} 
                                                className="text-sm text-accent hover:text-blue-400 transition flex items-center space-x-1"
                                            >
                                                <span>Copy Code</span>
                                            </button>
                                        </div>
                                        <div className="flex-1 bg-darkBg relative">
                                            {p.submitted_code ? (
                                                <MonacoEditor 
                                                    value={p.submitted_code} 
                                                    language={p.language} 
                                                    readOnly={true} 
                                                />
                                            ) : (
                                                <div className="absolute inset-0 flex items-center justify-center text-gray-500 italic">
                                                    No code submitted for this problem.
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            ) : (
                                <div className="bg-cardBg border border-gray-800 p-10 rounded-lg text-center">
                                    <div className="text-gray-400 text-lg">Candidate has not submitted a solution for this problem yet.</div>
                                    <div className="text-sm text-gray-500 mt-2">Problem Status: <span className="capitalize">{p.status}</span></div>
                                </div>
                            )}
                        </>
                    );
                })()}
            </div>
        </div>
    );
}
