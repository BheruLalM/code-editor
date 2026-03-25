import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import publicApi from '../../api/publicApi';

export default function WaitingRoomPage() {
    const { token } = useParams();
    const navigate = useNavigate();
    const [candidateName, setCandidateName] = useState('');
    const [error, setError] = useState('');

    useEffect(() => {
        const checkStatus = async () => {
            try {
                const res = await publicApi.get(`/test/attempt/${token}`);
                setCandidateName(res.data.candidate_name);
                
                if (res.data.status !== 'waiting') {
                    navigate(`/solve/${token}`);
                }
            } catch (err) {
                setError("Invalid session or session expired.");
            }
        };

        checkStatus();
        const interval = setInterval(checkStatus, 5000); // Poll every 5 seconds
        return () => clearInterval(interval);
    }, [token, navigate]);

    if (error) {
        return (
            <div className="min-h-screen bg-darkBg text-white flex items-center justify-center p-4">
                <div className="bg-cardBg border border-red-900/50 p-8 rounded-xl max-w-md w-full text-center shadow-lg">
                    <h2 className="text-2xl font-bold mb-2 text-red-500">Error</h2>
                    <p className="text-gray-400">{error}</p>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-darkBg text-white flex flex-col items-center justify-center p-4">
            <div className="max-w-md w-full text-center space-y-8">
                <div className="animate-pulse">
                    <div className="text-accent font-mono text-3xl font-bold mb-2">&lt; /&gt; CodeArena</div>
                </div>
                
                <div className="bg-cardBg border border-gray-800 p-10 rounded-2xl shadow-2xl relative overflow-hidden">
                    <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-accent to-transparent"></div>
                    
                    <h1 className="text-2xl font-bold mb-4">Hello, {candidateName}!</h1>
                    <p className="text-gray-400 mb-8 leading-relaxed">
                        You have successfully registered. Please wait while an admin reviews your application and assigns your assessment problems.
                    </p>
                    
                    <div className="flex flex-col items-center space-y-6">
                        <div className="relative">
                            <div className="w-16 h-16 border-4 border-accent border-t-transparent rounded-full animate-spin"></div>
                            <div className="absolute inset-0 flex items-center justify-center">
                                <div className="w-2 h-2 bg-accent rounded-full animate-ping"></div>
                            </div>
                        </div>
                        
                        <div className="space-y-2">
                            <div className="text-accent font-medium">Waiting for assignment...</div>
                            <p className="text-xs text-gray-500 italic">This page will automatically refresh once your test is ready.</p>
                        </div>
                    </div>
                </div>

                <div className="text-xs text-gray-600">
                    ID: {token.substring(0, 8)}...
                </div>
            </div>
        </div>
    );
}
