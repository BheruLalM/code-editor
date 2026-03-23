import { CheckCircle, XCircle } from 'lucide-react';

export default function TestResults({ results = [], hiddenPassed = 0, hiddenTotal = 0 }) {
    return (
        <div className="space-y-4">
            {results.map((res, i) => (
                <div key={i} className={`p-4 rounded border ${res.passed ? 'bg-green-900/20 border-green-800' : 'bg-red-900/20 border-red-800'}`}>
                    <div className="flex items-center space-x-2 mb-2">
                        {res.passed ? <CheckCircle className="text-green-500" size={18} /> : <XCircle className="text-red-500" size={18} />}
                        <span className="font-semibold">{res.description || `Test Case ${i + 1}`}</span>
                        {res.execution_time_ms !== undefined && (
                            <span className="text-xs text-gray-400 ml-auto">{res.execution_time_ms} ms</span>
                        )}
                    </div>
                    
                    {!res.passed && (
                        <div className="mt-3 space-y-2 text-sm font-mono">
                            <div>
                                <div className="text-gray-400">Input:</div>
                                <div className="bg-darkBg p-2 rounded whitespace-pre-wrap">{res.input}</div>
                            </div>
                            <div>
                                <div className="text-gray-400">Expected:</div>
                                <div className="bg-darkBg p-2 rounded whitespace-pre-wrap">{res.expected}</div>
                            </div>
                            <div>
                                <div className="text-gray-400">Actual:</div>
                                <div className="bg-darkBg p-2 rounded text-red-400 whitespace-pre-wrap">{res.actual || res.error}</div>
                            </div>
                        </div>
                    )}
                </div>
            ))}

            {hiddenTotal > 0 && (
                <div className="p-4 rounded border bg-purple-900/20 border-purple-800 flex items-center space-x-2">
                    <span className="text-purple-400 font-semibold">
                        🔒 Hidden Tests: {hiddenPassed}/{hiddenTotal} passed
                    </span>
                </div>
            )}
        </div>
    );
}
