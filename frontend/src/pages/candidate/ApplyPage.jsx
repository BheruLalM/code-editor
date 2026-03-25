import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import publicApi from '../../api/publicApi';

export default function ApplyPage() {
    const navigate = useNavigate();
    const [submitting, setSubmitting] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const candidate_name = e.target.name.value;
        const candidate_email = e.target.email.value;

        setSubmitting(true);
        const loadingToast = toast.loading("Registering...");
        
        try {
            const res = await publicApi.post('/test/apply', {
                candidate_name, candidate_email
            });
            
            toast.dismiss(loadingToast);
            const candToken = res.data.candidate_token;
            
            // If already submitted, navigate to solve results
            if (res.data.status === 'submitted') {
                navigate(`/solve/${candToken}`);
                return;
            }

            // If already assigned/started, navigate to solve
            if (res.data.status === 'started' || res.data.status === 'registered') {
                navigate(`/solve/${candToken}`);
                return;
            }

            // Otherwise, go to waiting room
            navigate(`/waiting/${candToken}`);
            
        } catch (err) {
            toast.dismiss(loadingToast);
            toast.error(err.response?.data?.detail || "Registration failed");
            setSubmitting(false);
        }
    };

    return (
        <div className="min-h-screen bg-darkBg text-white flex flex-col items-center justify-center p-4">
            <div className="mb-8 text-center animate-fade-in">
                <div className="text-accent font-mono text-4xl font-bold mb-2">&lt; /&gt; CodeArena</div>
                <p className="text-gray-400">Join the assessment queue</p>
            </div>

            <div className="bg-cardBg border border-gray-800 p-10 rounded-2xl max-w-lg w-full shadow-2xl backdrop-blur-sm bg-opacity-80">
                <h1 className="text-2xl font-bold mb-6 text-center">Candidate Registration</h1>
                
                <form onSubmit={handleSubmit} className="space-y-6">
                    <div>
                        <label className="block text-sm font-medium text-gray-400 mb-2">Full Name*</label>
                        <input 
                            name="name"
                            type="text" 
                            required
                            autoFocus
                            placeholder="John Doe"
                            className="w-full bg-darkBg border border-gray-700 rounded-lg p-3.5 text-white focus:border-accent focus:ring-1 focus:ring-accent outline-none transition-all duration-200"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-400 mb-2">Email Address*</label>
                        <input 
                            name="email"
                            type="email" 
                            required
                            placeholder="john@example.com"
                            className="w-full bg-darkBg border border-gray-700 rounded-lg p-3.5 text-white focus:border-accent focus:ring-1 focus:ring-accent outline-none transition-all duration-200"
                        />
                    </div>

                    <div className="pt-4">
                        <button 
                            type="submit" 
                            disabled={submitting}
                            className="w-full bg-accent hover:bg-blue-600 font-bold text-white py-4 rounded-xl transition-all duration-300 transform hover:scale-[1.02] shadow-lg shadow-blue-500/20 disabled:opacity-50"
                        >
                            Register & Continue →
                        </button>
                    </div>
                </form>
                
                <p className="text-xs text-center text-gray-500 mt-8 leading-relaxed">
                    By registering, you agree to be placed in the assessment queue.<br/>
                    An admin will review your details and assign problems.
                </p>
            </div>
        </div>
    );
}
