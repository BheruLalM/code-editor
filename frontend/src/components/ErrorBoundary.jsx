import React from 'react';

export default class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false };
    }

    static getDerivedStateFromError() {
        return { hasError: true };
    }

    render() {
        if (this.state.hasError) {
            return (
                <div className="min-h-screen bg-[#0F1629] text-white flex items-center justify-center p-4">
                    <div className="bg-[#1E2A45] border border-gray-800 p-8 rounded-xl max-w-md w-full text-center shadow-lg">
                        <div className="w-16 h-16 bg-red-900/30 text-red-500 rounded-full flex items-center justify-center mx-auto mb-4 text-2xl border border-red-800">
                            !
                        </div>
                        <h2 className="text-2xl font-bold mb-2">Something went wrong</h2>
                        <p className="text-gray-400 mb-6">An unexpected error occurred. Please try refreshing the page.</p>
                        <button
                            onClick={() => window.location.reload()}
                            className="bg-[#2563EB] hover:bg-blue-600 text-white font-medium py-2.5 px-6 rounded transition"
                        >
                            Refresh Page
                        </button>
                    </div>
                </div>
            );
        }

        return this.props.children;
    }
}
