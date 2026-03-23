import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import api from '../../api/axios';
import BackButton from '../../components/BackButton';

export default function CreateSessionPage() {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const [successData, setSuccessData] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const fd = new FormData(e.target);
        const maxAttempts = fd.get('max_attempts');
        const expiresAt = fd.get('expires_at');
        
        const payload = {
            title: fd.get('title'),
            description: fd.get('description'),
            difficulty_filter: fd.get('difficulty_filter'),
            time_limit_minutes: parseInt(fd.get('time_limit_minutes')),
            max_attempts: maxAttempts ? parseInt(maxAttempts) : null,
            expires_at: expiresAt ? new Date(expiresAt).toISOString() : null
        };

        setLoading(true);
        try {
            const res = await api.post('/admin/sessions/', payload);
            setSuccessData(res.data);
            toast.success("Session created!");
        } catch (error) {
            toast.error("Failed to create session");
        } finally {
            setLoading(false);
        }
    };

    if (successData) {
        return (
            <div className="min-h-screen bg-darkBg text-white p-8">
                <div className="max-w-2xl mx-auto">
                    <BackButton to="/admin" label="Back to Dashboard" />
                    
                    <div className="mt-6 bg-cardBg border border-gray-800 rounded-lg p-8 shadow-xl text-center">
                        <div className="w-16 h-16 bg-green-900/30 text-green-400 border border-green-800 rounded-full flex items-center justify-center mx-auto mb-4 text-3xl">✓</div>
                        <h2 className="text-2xl font-bold mb-6">Session Created Successfully!</h2>
                        
                        <div className="grid grid-cols-2 gap-4 text-left max-w-md mx-auto mb-8 bg-darkBg p-4 rounded border border-gray-800">
                            <div className="text-gray-400 text-sm">Title</div>
                            <div className="font-semibold">{successData.session.title}</div>
                            
                            <div className="text-gray-400 text-sm">Difficulty</div>
                            <div className="font-semibold capitalize">{successData.session.difficulty_filter}</div>
                            
                            <div className="text-gray-400 text-sm">Time Limit</div>
                            <div className="font-semibold">{successData.session.time_limit_minutes} minutes</div>
                        </div>

                        <div className="mb-6">
                            <div className="text-sm text-gray-400 mb-2">Share this link with candidates:</div>
                            <div className="bg-[#111827] border border-gray-700 p-3 rounded font-mono text-accent text-sm break-all select-all flex justify-between items-center">
                                <span>{successData.shareable_link}</span>
                            </div>
                        </div>

                        <div className="flex space-x-4 justify-center mt-8">
                            <button 
                                onClick={() => {
                                    navigator.clipboard.writeText(successData.shareable_link);
                                    toast.success("Copied!");
                                }}
                                className="px-6 py-2 border border-gray-600 rounded hover:bg-gray-800 transition"
                            >
                                Copy Link
                            </button>
                            <Link 
                                to={`/admin/sessions/${successData.session.id}`}
                                className="px-6 py-2 bg-accent hover:bg-blue-600 rounded transition font-medium text-white"
                            >
                                View Results Page
                            </Link>
                        </div>
                        
                        <div className="mt-8">
                            <button onClick={() => setSuccessData(null)} className="text-sm text-gray-400 hover:text-white underline">Create Another Session</button>
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-darkBg text-white p-6 md:p-10">
            <div className="max-w-3xl mx-auto">
                <BackButton to="/admin" />
                <h1 className="text-3xl font-bold mt-4 mb-8">Create Test Session</h1>

                <div className="bg-cardBg border border-gray-800 rounded-xl p-6 md:p-8 shadow-lg">
                    <form onSubmit={handleSubmit} className="space-y-6">
                        <div>
                            <label className="block text-sm font-medium text-gray-300 mb-1">Session Title*</label>
                            <input 
                                name="title"
                                type="text" 
                                required
                                placeholder="e.g. Python Developer Round 1"
                                className="w-full bg-darkBg border border-gray-700 rounded p-3 text-white focus:border-accent focus:ring-1 focus:ring-accent outline-none transition"
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-300 mb-1">Description (optional)</label>
                            <textarea 
                                name="description"
                                rows={3}
                                placeholder="Instructions or internal notes..."
                                className="w-full bg-darkBg border border-gray-700 rounded p-3 text-white focus:border-accent focus:ring-1 focus:ring-accent outline-none transition"
                            />
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <label className="block text-sm font-medium text-gray-300 mb-1">Difficulty Filter</label>
                                <select 
                                    name="difficulty_filter"
                                    className="w-full bg-darkBg border border-gray-700 rounded p-3 text-white focus:border-accent focus:ring-1 focus:ring-accent outline-none transition"
                                >
                                    <option value="any">Any Difficulty (Random)</option>
                                    <option value="easy">Easy Only</option>
                                    <option value="medium">Medium Only</option>
                                    <option value="hard">Hard Only</option>
                                </select>
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-300 mb-1">Time Limit</label>
                                <select 
                                    name="time_limit_minutes"
                                    defaultValue={45}
                                    className="w-full bg-darkBg border border-gray-700 rounded p-3 text-white focus:border-accent focus:ring-1 focus:ring-accent outline-none transition"
                                >
                                    <option value={30}>30 Minutes</option>
                                    <option value={45}>45 Minutes</option>
                                    <option value={60}>60 Minutes</option>
                                    <option value={90}>90 Minutes</option>
                                    <option value={120}>120 Minutes</option>
                                </select>
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-300 mb-1">Link Expiry (optional)</label>
                                <input 
                                    name="expires_at"
                                    type="datetime-local" 
                                    className="w-full bg-darkBg border border-gray-700 rounded p-3 text-white focus:border-accent focus:ring-1 focus:ring-accent outline-none transition [color-scheme:dark]"
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-300 mb-1">Max Candidates (optional, leave empty for unlimited)</label>
                                <input 
                                    name="max_attempts"
                                    type="number"
                                    min={1}
                                    placeholder="e.g. 50"
                                    className="w-full bg-darkBg border border-gray-700 rounded p-3 text-white focus:border-accent focus:ring-1 focus:ring-accent outline-none transition"
                                />
                            </div>
                        </div>

                        <div className="pt-4 border-t border-gray-800">
                            <button 
                                type="submit" 
                                disabled={loading}
                                className="w-full bg-accent hover:bg-blue-600 text-white font-medium py-3 rounded-lg transition shadow-lg shadow-blue-900/20 disabled:opacity-50"
                            >
                                {loading ? 'Creating...' : 'Create Session'}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
}
