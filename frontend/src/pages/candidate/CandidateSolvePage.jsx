import { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { Play, Send } from 'lucide-react';
import publicApi from '../../api/publicApi';
import Timer from '../../components/Timer';
import MonacoEditor from '../../components/MonacoEditor';
import TestResults from '../../components/TestResults';

export default function CandidateSolvePage() {
    const { token } = useParams();
    const navigate = useNavigate();
    
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [errorMsg, setErrorMsg] = useState('');
    
    const [language, setLanguage] = useState('python');
    const [code, setCode] = useState('');
    
    const [executing, setExecuting] = useState(false);
    const [submitting, setSubmitting] = useState(false);
    
    // Console state
    const [runOutput, setRunOutput] = useState(null);
    const [activeTab, setActiveTab] = useState('results');
    
    const saveTimeout = useRef(null);

    useEffect(() => {
        loadAttempt();
    }, [token]);

    const loadAttempt = async () => {
        try {
            const res = await publicApi.get(`/test/attempt/${token}`);
            const d = res.data;
            setData(d);
            
            if (d.already_submitted) {
                setLoading(false);
                return;
            }
            
            // Check for saved code
            const savedCode = sessionStorage.getItem(`codearena_saved_${token}`);
            const savedLang = sessionStorage.getItem(`codearena_lang_${token}`);
            const starter = d.problem?.starter_code || {};
            const allowedLangs = Object.keys(starter);
            const langToUse = savedLang && starter[savedLang] ? savedLang : (starter.python ? 'python' : allowedLangs[0]);

            if (allowedLangs.length > 0) {
                setLanguage(langToUse);
            }
            
            if (savedCode) {
                setCode(savedCode);
            } else if (d.problem?.starter_code) {
                setCode(starter[langToUse]);
                sessionStorage.setItem(`codearena_saved_${token}`, starter[langToUse]);
            }
            
            setLoading(false);
        } catch (err) {
            setErrorMsg("Invalid test link. Please contact your recruiter.");
            setLoading(false);
        }
    };

    const handleCodeChange = (newCode) => {
        setCode(newCode);
        if (saveTimeout.current) clearTimeout(saveTimeout.current);
        saveTimeout.current = setTimeout(() => {
            sessionStorage.setItem(`codearena_saved_${token}`, newCode);
        }, 10000); 
    };

    const handleLanguageChange = (e) => {
        const newLang = e.target.value;
        const starter = data.problem?.starter_code || {};
        const currentStarter = starter[language];
        const newStarter = starter[newLang];

        if (!newStarter) {
            toast.error("Selected language is not available for this problem.");
            return;
        }
        
        if (code !== '' && code !== currentStarter) {
            if (!window.confirm("Switch language? Your current code will be replaced.")) {
                return;
            }
        }
        
        setLanguage(newLang);
        sessionStorage.setItem(`codearena_lang_${token}`, newLang);

        setCode(newStarter);
        sessionStorage.setItem(`codearena_saved_${token}`, newStarter);
    };

    const handleRun = async () => {
        setExecuting(true);
        setActiveTab('results');
        try {
            const res = await publicApi.post('/execute/run', {
                problem_id: data.problem.id,
                language: language,
                code: code
            });
            setRunOutput(res.data);
        } catch (err) {
            setRunOutput({ error: err.response?.data?.detail || "Execution failed" });
            setActiveTab('output');
        } finally {
            setExecuting(false);
        }
    };

    const handleSubmitClick = async () => {
        if (!window.confirm("Submit your solution?\nYou will not be able to make changes after submission.")) {
            return;
        }
        doSubmit();
    };

    const doSubmit = async () => {
        if (data.already_submitted) return;
        setSubmitting(true);
        try {
            await publicApi.post(`/test/attempt/${token}/submit`, {
                language: language,
                code: code
            });
            await loadAttempt();
        } catch (err) {
            const msg = err.response?.data?.detail || "Submission failed";
            toast.error(msg);
            setSubmitting(false);
            if (err.response?.status === 400 && msg.includes('already submitted')) {
                await loadAttempt();
            }
        }
    };

    if (loading) {
        return <div className="min-h-screen bg-darkBg text-white flex flex-col items-center justify-center space-y-4">
            <div className="w-8 h-8 border-4 border-accent border-t-transparent rounded-full animate-spin"></div>
            <div className="text-gray-400 font-medium tracking-wide">Loading workspace...</div>
        </div>;
    }

    if (errorMsg) {
        return <div className="min-h-screen bg-darkBg text-white flex items-center justify-center p-10">{errorMsg}</div>;
    }

    if (data.already_submitted) {
        return (
            <div className="fixed inset-0 bg-darkBg z-50 overflow-y-auto pt-10 pb-20 px-4">
                <div className="max-w-[520px] mx-auto bg-cardBg border border-gray-800 rounded-xl p-8 shadow-2xl relative">
                    <div className="text-center mb-6">
                        <div className="text-gray-400 mb-2 font-medium">Test Completed</div>
                        
                        <div className={`w-36 h-36 mx-auto rounded-full border-8 flex flex-col items-center justify-center mb-4 transition-colors relative
                            ${data.score >= 75 ? 'border-green-500 text-green-500 shadow-[0_0_30px_rgba(34,197,94,0.2)]' : 
                              data.score >= 50 ? 'border-amber-500 text-amber-500 shadow-[0_0_30px_rgba(245,158,11,0.2)]' : 
                              'border-red-500 text-red-500 shadow-[0_0_30px_rgba(239,68,68,0.2)]'}`}
                        >
                            <span className="text-5xl font-black">{data.score?.toFixed(0) || 0}</span>
                            <span className="text-sm font-semibold opacity-60">/ 100</span>
                        </div>
                        
                        <div className="text-lg font-bold">
                            {(data.test_results?.visible?.filter(r=>r.passed).length || 0) + (data.test_results?.hidden_passed || 0)}/
                            {(data.test_results?.visible?.length || 0) + (data.test_results?.hidden_total || 0)} test cases passed
                        </div>
                    </div>

                    <div className="grid grid-cols-2 gap-3 mb-8">
                        <div className="bg-[#111827] border border-gray-800 p-3 rounded text-center shrink-0 w-full flex flex-col">
                            <div className="text-xs text-gray-500">Visible Passed</div>
                            <div className="font-mono text-lg">{data.test_results?.visible?.filter(r=>r.passed).length || 0}/{data.test_results?.visible?.length || 0}</div>
                        </div>
                        <div className="bg-[#111827] border border-gray-800 p-3 rounded text-center shrink-0 w-full flex flex-col">
                            <div className="text-xs text-gray-500">Hidden Passed</div>
                            <div className="font-mono text-lg">{data.test_results?.hidden_passed || 0}/{data.test_results?.hidden_total || 0}</div>
                        </div>
                        
                        <div className="bg-[#111827] border border-gray-800 p-3 rounded text-center shrink-0 w-full flex flex-col">
                            <div className="text-xs text-gray-500">Language</div>
                            <div className="font-mono text-lg capitalize">{data.submitted_code ? data.language : 'None'}</div>
                        </div>
                        
                        <div className="bg-[#111827] border border-gray-800 p-3 rounded text-center shrink-0 w-full flex flex-col">
                             <div className="text-xs text-gray-500">Status</div>
                             <div className="font-mono text-lg capitalize text-green-400">Submitted</div>
                        </div>
                    </div>

                    <div className="text-sm text-center text-gray-400 border-t border-gray-800 pt-6">
                        Your solution has been submitted successfully.<br/>
                        The recruiter will review your results.
                    </div>
                </div>
            </div>
        );
    }

    const p = data.problem;

    return (
        <div className="h-screen bg-darkBg text-white flex flex-col overflow-hidden">
            {/* TOP BAR */}
            <header className="h-14 border-b border-gray-800 bg-[#172036] flex items-center justify-between px-6 shrink-0 z-10 w-full shadow-md">
                <div className="flex items-center space-x-3 w-[30%]">
                    <span className="font-bold text-lg truncate" title={p.title}>{p.title}</span>
                    <span className={`text-xs px-2 py-0.5 rounded capitalize font-semibold tracking-wide border min-w-fit
                        ${p.difficulty === 'easy' ? 'bg-green-900/40 text-green-400 border-green-800' :
                          p.difficulty === 'medium' ? 'bg-amber-900/40 text-amber-400 border-amber-800' :
                          'bg-red-900/40 text-red-400 border-red-800'}`
                    }>
                        {p.difficulty}
                    </span>
                </div>
                <div className="text-sm text-gray-500 text-center truncate flex-1 justify-center max-w-[40%]">{data.candidate_name}</div>
                <div className="w-[30%] flex justify-end">
                    <Timer 
                        totalSeconds={data.time_limit_minutes * 60} 
                        onExpire={doSubmit} 
                    />
                </div>
            </header>

            {/* 3 PANEL LAYOUT */}
            <main className="flex-1 flex overflow-hidden">
                
                {/* LEFT PANEL */}
                <section className="w-[32%] border-r border-gray-800 overflow-y-auto p-6 bg-[#0A0E17] custom-scrollbar pb-24 relative">
                    <h2 className="text-2xl font-bold mb-4">{p.title}</h2>
                    
                    <div className="flex flex-wrap gap-2 mb-6">
                        {p.tags?.map(t => (
                            <span key={t} className="bg-cardBg border border-gray-700 text-gray-300 text-xs px-2 py-1 rounded">
                                {t}
                            </span>
                        ))}
                    </div>

                    <div className="prose prose-invert prose-p:leading-relaxed max-w-none text-gray-300 mb-8 whitespace-pre-wrap text-sm">
                        {p.description}
                    </div>

                    {p.constraints && (
                        <div className="mb-8">
                            <h3 className="text-gray-400 font-bold uppercase tracking-wider text-xs mb-3 border-b border-gray-800 pb-2">Constraints</h3>
                            <div className="bg-cardBg p-3 rounded border border-gray-800 font-mono text-xs text-gray-300 whitespace-pre-wrap">
                                {p.constraints}
                            </div>
                        </div>
                    )}

                    <div className="space-y-6 mb-8">
                        <h3 className="text-gray-400 font-bold uppercase tracking-wider text-xs border-b border-gray-800 pb-2">Examples</h3>
                        {p.examples.map((ex, i) => (
                            <div key={i} className="bg-cardBg border border-gray-800 rounded p-4">
                                <div className="mb-2">
                                    <strong className="text-gray-500 text-xs uppercase mr-2">Input:</strong>
                                    <div className="bg-darkBg p-2 mt-1 rounded font-mono text-sm border border-gray-800 whitespace-pre-wrap">{ex.input}</div>
                                </div>
                                <div className="mb-2">
                                    <strong className="text-gray-500 text-xs uppercase mr-2">Output:</strong>
                                    <div className="bg-darkBg p-2 mt-1 rounded font-mono text-sm border border-gray-800 text-green-400">{ex.output}</div>
                                </div>
                                {ex.explanation && (
                                    <div className="mt-3 text-sm text-gray-400 border-t border-gray-800 pt-2 pb-1">
                                        <span className="font-semibold block mb-1">Explanation:</span>
                                        {ex.explanation}
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>

                    <div className="space-y-4">
                        <h3 className="text-gray-400 font-bold uppercase tracking-wider text-xs border-b border-gray-800 pb-2">Visible Test Cases</h3>
                        {p.visible_test_cases.map((tc, i) => {
                            const resultTC = runOutput?.results?.find(r => r.case_number === i + 1);
                            
                            return (
                                <div key={i} className={`bg-cardBg border rounded p-4 transition-colors text-sm ${
                                    resultTC 
                                        ? resultTC.passed 
                                            ? 'border-green-800 bg-green-900/10' 
                                            : 'border-red-800 bg-red-900/10'
                                        : 'border-gray-800'
                                }`}>
                                    <div className="flex font-semibold justify-between items-center mb-1">
                                        <span className="text-gray-300">Test Case {i+1}: {tc.description || 'Basic case'}</span>
                                        {resultTC && (
                                            resultTC.passed ? <span className="text-green-500">✓</span> : <span className="text-red-500">✗</span>
                                        )}
                                    </div>
                                    
                                    {resultTC && !resultTC.passed && (
                                        <div className="mt-3 text-xs font-mono space-y-2 bg-darkBg p-3 rounded border border-red-900/50">
                                            <div><span className="text-gray-500 pr-2">Input:</span> <span className="text-gray-300">{resultTC.input}</span></div>
                                            <div><span className="text-gray-500 pr-2">Expected:</span> <span className="text-green-400">{resultTC.expected}</span></div>
                                            <div><span className="text-gray-500 pr-2">Actual:</span> <span className="text-red-400">{resultTC.actual || resultTC.error}</span></div>
                                        </div>
                                    )}
                                </div>
                            );
                        })}
                    </div>
                </section>

                {/* MIDDLE PANEL */}
                <section className="w-[48%] flex flex-col relative border-r border-gray-800 bg-[#0A0E17]">
                    <div className="h-14 border-b border-gray-800 flex items-center justify-between px-4 bg-[#111827] shrink-0">
                        <select 
                            value={language}
                            onChange={handleLanguageChange}
                            className="bg-[#1e293b] border border-gray-700 text-sm rounded-md px-3 py-1.5 cursor-pointer outline-none focus:border-accent text-white min-w-[160px]"
                        >
                            <option value="python">Python 3</option>
                            <option value="javascript">JavaScript (Node)</option>
                            <option value="java">Java</option>
                        </select>
                        <div className="text-xs text-gray-500 flex items-center space-x-1 border border-gray-800 px-2 py-1 rounded bg-darkBg">
                            <div className="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse"></div>
                            <span>Autosaved locally</span>
                        </div>
                    </div>

                    <div className="flex-1 relative">
                        <MonacoEditor 
                            value={code} 
                            onChange={handleCodeChange} 
                            language={language}
                        />
                        {executing && (
                            <div className="absolute inset-0 bg-darkBg/60 backdrop-blur-sm z-10 flex items-center justify-center">
                                <div className="bg-cardBg px-6 py-4 rounded-lg shadow-xl border border-gray-700 flex items-center space-x-3">
                                    <div className="w-4 h-4 border-2 border-accent border-t-transparent rounded-full animate-spin"></div>
                                    <span className="font-medium text-sm text-gray-300">Executing code...</span>
                                </div>
                            </div>
                        )}
                        {submitting && (
                            <div className="absolute inset-0 bg-darkBg/80 backdrop-blur-md z-20 flex items-center justify-center">
                                <div className="bg-cardBg px-8 py-6 rounded-xl shadow-2xl border border-gray-700 flex flex-col items-center">
                                    <div className="w-10 h-10 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mb-4"></div>
                                    <span className="font-bold text-xl mb-1 text-white">Evaluating Solution</span>
                                    <span className="text-sm text-gray-400 font-medium">Running hidden test cases...</span>
                                </div>
                            </div>
                        )}
                    </div>

                    <div className="h-16 border-t border-gray-800 bg-[#111827] flex items-center justify-between px-6 shrink-0 relative z-10">
                        <div className="text-sm text-gray-400 font-mono">
                            {runOutput?.execution_time_ms !== undefined ? (
                                <span className="flex items-center space-x-2">
                                    <span className="w-2 h-2 rounded-full bg-green-500"></span>
                                    <span>Ran in {runOutput.execution_time_ms}ms</span>
                                </span>
                            ) : (
                                <span className="opacity-0">Ready</span>
                            )}
                        </div>
                        <div className="flex space-x-3">
                            <button 
                                onClick={handleRun}
                                disabled={executing || submitting}
                                className="flex items-center space-x-1.5 border border-gray-600 hover:bg-gray-800 hover:border-gray-500 text-gray-300 hover:text-white px-5 py-2.5 rounded font-medium transition-all disabled:opacity-50 text-sm bg-darkBg shadow-sm"
                            >
                                <Play size={16} fill="currentColor" />
                                <span>Run Code</span>
                            </button>
                            <button 
                                onClick={handleSubmitClick}
                                disabled={executing || submitting}
                                className="flex items-center space-x-1.5 bg-accent hover:bg-blue-600 text-white px-6 py-2.5 rounded font-bold transition-all disabled:opacity-50 text-sm shadow-blue-500/20 shadow-lg border border-blue-500/50"
                            >
                                <Send size={16} />
                                <span>Submit Solution</span>
                            </button>
                        </div>
                    </div>
                </section>

                {/* RIGHT PANEL */}
                <section className="w-[20%] flex flex-col bg-cardBg z-10 shadow-[-5px_0_20px_rgba(0,0,0,0.15)] relative">
                    <div className="h-14 border-b border-gray-800 bg-[#111827] flex shrink-0 w-full">
                        <button 
                            onClick={() => setActiveTab('results')}
                            className={`flex-1 text-sm font-bold transition-all border-b-2 tracking-wide uppercase px-2
                                ${activeTab === 'results' ? 'border-accent text-accent bg-[#1a2333]' : 'border-transparent text-gray-400 hover:text-gray-200 hover:bg-gray-800/50'}`}
                        >
                            Test Results
                        </button>
                        <button 
                            onClick={() => setActiveTab('output')}
                            className={`flex-1 text-sm font-bold transition-all border-b-2 tracking-wide uppercase px-2
                                ${activeTab === 'output' ? 'border-accent text-accent bg-[#1a2333]' : 'border-transparent text-gray-400 hover:text-gray-200 hover:bg-gray-800/50'}`}
                        >
                            Output Logs
                        </button>
                    </div>

                    <div className="flex-1 overflow-y-auto p-4 custom-scrollbar bg-[#0A0E17]">
                        {activeTab === 'output' && (
                            <div className="font-mono text-[13px] h-full leading-relaxed w-full overflow-x-hidden p-1">
                                {!runOutput ? (
                                    <div className="text-gray-600 italic mt-6 flex flex-col items-center justify-center p-4 bg-darkBg rounded border border-gray-800/50 h-32">
                                        <Play size={20} className="mb-2 opacity-50 text-gray-500" />
                                        <div className="text-gray-500 text-xs">Run code to see stdout</div>
                                    </div>
                                ) : runOutput.error ? (
                                    <div className="text-red-400 whitespace-pre-wrap break-all p-3 bg-red-900/10 border border-red-900/30 rounded">{runOutput.error}</div>
                                ) : (
                                    <>
                                        {runOutput.results?.some(r => r.actual) ? (
                                            <div className="text-gray-300 w-full pr-1">
                                                {runOutput.results.map((r, i) => r.actual ? (
                                                    <div key={i} className="mb-4 border-l-2 pl-3 pb-1 border-gray-700 w-full overflow-hidden">
                                                        <div className="text-[10px] uppercase tracking-wider text-gray-500 mb-1.5 font-sans font-bold">Case {i+1} Output</div>
                                                        <div className={`whitespace-pre-wrap break-words w-full p-2 bg-[#111827] rounded text-xs ${r.error ? 'text-red-400' : 'text-gray-300'} border border-gray-800`}>{r.actual || r.error}</div>
                                                    </div>
                                                ) : null)}
                                            </div>
                                        ) : (
                                            <div className="text-gray-500 italic text-center p-8 text-xs bg-darkBg rounded border border-gray-800">
                                                No stdout returned by your code.<br/>(Successfully ran tests)
                                            </div>
                                        )}
                                    </>
                                )}
                            </div>
                        )}

                        {activeTab === 'results' && (
                            <div className="h-full">
                                {!runOutput ? (
                                    <div className="text-gray-600 italic mt-6 flex flex-col items-center justify-center p-4 bg-darkBg rounded border border-gray-800/50 h-32">
                                        <Play size={20} className="mb-2 opacity-50 text-gray-500" />
                                        <div className="text-gray-500 text-xs text-center leading-relaxed">No test results yet.<br/>Run your code to start testing.</div>
                                    </div>
                                ) : runOutput.error ? (
                                    <div className="p-4 bg-red-900/20 border border-red-900/50 rounded text-red-400 text-sm">Execution failed before tests could run. Check output.</div>
                                ) : (
                                    <div className="space-y-3 p-1 w-full">
                                        <div className="flex justify-between items-center mb-5 border-b border-gray-800 pb-3 h-6">
                                            <span className="font-bold text-[11px] uppercase tracking-wider text-gray-400">Total</span>
                                            <span className={`text-[11px] px-2 py-0.5 rounded font-bold uppercase tracking-wider border
                                                ${runOutput.passed === runOutput.total 
                                                    ? 'bg-green-900/30 text-green-400 border-green-800' 
                                                    : 'bg-red-900/30 text-red-400 border-red-800'}`}>
                                                {runOutput.passed}/{runOutput.total} passed
                                            </span>
                                        </div>
                                        
                                        <div className="space-y-2">
                                            {runOutput.results.map((r, i) => (
                                                <div key={i} className={`p-3 rounded border text-sm w-full transition-colors flex items-center justify-between
                                                    ${r.passed ? 'bg-green-900/10 border-green-900 shadow-[0_2px_10px_rgba(34,197,94,0.05)]' : 'bg-red-900/10 border-red-900 shadow-[0_2px_10px_rgba(239,68,68,0.05)]'}`}>
                                                    <div className="flex items-center space-x-2 flex-1 min-w-0 pr-2">
                                                        <div className={`w-2 h-2 rounded-full shrink-0 ${r.passed ? 'bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.8)]' : 'bg-red-500 shadow-[0_0_8px_rgba(239,68,68,0.8)]'}`}></div>
                                                        <div className="font-semibold text-gray-300 text-xs truncate">Case {i+1}</div>
                                                    </div>
                                                    <div className="text-[10px] font-mono text-gray-500 bg-darkBg px-1.5 py-0.5 rounded border border-gray-800 shrink-0">
                                                        {r.execution_time_ms}ms
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                </section>
            </main>
        </div>
    );
}
