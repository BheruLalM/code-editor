import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import publicApi from '../../api/publicApi';

export default function CandidateRegisterPage() {
    const { token } = useParams();
    const navigate = useNavigate();
    
    const [sessionData, setSessionData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [errorMsg, setErrorMsg] = useState('');
    const [submitting, setSubmitting] = useState(false);

    useEffect(() => {
        publicApi.get(`/test/${token}`)
            .then(res => {
                const payload = res?.data;
                if (!payload || typeof payload !== 'object' || !payload.title) {
                    setErrorMsg("Invalid test session data. Please contact your recruiter.");
                    return;
                }
                setSessionData(payload);
            })
            .catch(err => {
                const reason = err.response?.data?.reason;
                if (reason === 'expired') setErrorMsg("This test link has expired");
                else if (reason === 'inactive') setErrorMsg("This test is no longer active");
                else if (reason === 'full') setErrorMsg("This test session is full");
                else if (err.code === 'ECONNABORTED') setErrorMsg("Server took too long to respond. Please try again.");
                else if (!err.response) setErrorMsg("Unable to reach server. Please check network or API URL.");
                else setErrorMsg("This link is invalid");
            })
            .finally(() => setLoading(false));
    }, [token]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const candidate_name = e.target.name.value;
        const candidate_email = e.target.email.value;

        setSubmitting(true);
        const loadingToast = toast.loading("Setting up your test...");
        
        try {
            const res = await publicApi.post(`/test/${token}/register`, {
                candidate_name, candidate_email
            });
            
            toast.dismiss(loadingToast);
            
            const candToken = res.data.candidate_token;
            // Store token in session storage for the redirect
            sessionStorage.setItem('codearena_cand_token', candToken);
            
            navigate(`/solve/${candToken}`);
            
        } catch (err) {
            toast.dismiss(loadingToast);
            toast.error(err.response?.data?.detail || "Registration failed");
            setSubmitting(false);
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-darkBg text-white flex items-center justify-center flex-col space-y-4">
                <div className="w-8 h-8 border-4 border-accent border-t-transparent rounded-full animate-spin"></div>
                <div className="text-gray-400 font-medium tracking-wide">Loading session...</div>
            </div>
        );
    }

    if (errorMsg) {
        return (
            <div className="min-h-screen bg-darkBg text-white flex items-center justify-center p-4">
                <div className="bg-cardBg border border-red-900/50 p-8 rounded-xl max-w-md w-full text-center shadow-lg">
                    <div className="w-16 h-16 bg-red-900/30 text-red-500 rounded-full flex items-center justify-center mx-auto mb-4 text-2xl border border-red-800">
                        !
                    </div>
                    <h2 className="text-2xl font-bold mb-2">Access Denied</h2>
                    <p className="text-gray-400">{errorMsg}</p>
                </div>
            </div>
        );
    }

    if (!sessionData) {
        return (
            <div className="min-h-screen bg-darkBg text-white flex items-center justify-center p-4">
                <div className="bg-cardBg border border-red-900/50 p-8 rounded-xl max-w-md w-full text-center shadow-lg">
                    <h2 className="text-2xl font-bold mb-2">Unable to Load Test</h2>
                    <p className="text-gray-400">The test session data is unavailable right now. Please try again or contact your recruiter.</p>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-darkBg text-white flex flex-col items-center justify-center p-4">
            <div className="mb-8 text-center">
                <div className="text-accent font-mono text-3xl font-bold mb-2">&lt; /&gt; CodeArena</div>
            </div>

            <div className="bg-cardBg border border-gray-800 p-8 rounded-xl max-w-lg w-full shadow-2xl">
                <h1 className="text-2xl font-bold mb-2">{sessionData.title}</h1>
                {sessionData.description && (
                    <p className="text-gray-400 mb-6 text-sm whitespace-pre-wrap">{sessionData.description}</p>
                )}
                
                <div className="flex flex-wrap gap-4 mb-6 bg-[#111827] p-4 rounded-lg border border-gray-800 text-sm">
                    <div className="flex items-center space-x-2 w-full md:w-auto">
                        <span>⏱</span>
                        <span className="text-gray-300">{sessionData.time_limit_minutes} minutes</span>
                    </div>
                    <div className="flex items-center space-x-2 w-full md:w-auto">
                        <span>📝</span>
                        <span className="text-gray-300">1 coding problem</span>
                    </div>
                    <div className="flex items-center space-x-2 w-full md:w-auto">
                        <span className="text-green-500">✓</span>
                        <span className="text-gray-300">One submission allowed</span>
                    </div>
                </div>

                <hr className="border-gray-800 my-6" />

                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-400 mb-1">Full Name*</label>
                        <input 
                            name="name"
                            type="text" 
                            required
                            autoFocus
                            placeholder="John Doe"
                            className="w-full bg-darkBg border border-gray-700 rounded p-3 text-white focus:border-accent focus:ring-1 focus:ring-accent outline-none transition"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-400 mb-1">Email Address*</label>
                        <input 
                            name="email"
                            type="email" 
                            required
                            placeholder="john@example.com"
                            className="w-full bg-darkBg border border-gray-700 rounded p-3 text-white focus:border-accent focus:ring-1 focus:ring-accent outline-none transition"
                        />
                    </div>

                    <div className="pt-4">
                        <button 
                            type="submit" 
                            disabled={submitting}
                            className="w-full bg-accent hover:bg-blue-600 font-medium text-white py-3 rounded-lg transition shadow-lg disabled:opacity-50"
                        >
                            Start Test →
                        </button>
                    </div>
                    
                    <div className="text-xs text-center text-gray-500 mt-4 leading-relaxed">
                        Once you start, the timer begins immediately.<br/>
                        Do not close or refresh the browser.
                    </div>
                </form>
            </div>
        </div>
    );
}
