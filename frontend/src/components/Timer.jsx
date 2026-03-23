import { useState, useEffect } from 'react';

export default function Timer({ totalSeconds, onExpire, onTick }) {
    const getSavedRemaining = () => {
        const saved = localStorage.getItem('codearena-timer');
        if (saved !== null) {
            return parseInt(saved, 10);
        }
        return totalSeconds;
    };

    const [remaining, setRemaining] = useState(getSavedRemaining);

    useEffect(() => {
        // Init if not saved or different init total
        if (localStorage.getItem('codearena-timer-init') !== String(totalSeconds)) {
            setRemaining(totalSeconds);
            localStorage.setItem('codearena-timer-init', totalSeconds);
            localStorage.setItem('codearena-timer', totalSeconds);
        }
    }, [totalSeconds]);

    useEffect(() => {
        if (remaining <= 0) {
            if (onExpire) onExpire();
            return;
        }

        const interval = setInterval(() => {
            setRemaining((prev) => {
                const newTime = prev - 1;
                localStorage.setItem('codearena-timer', newTime);
                if (onTick) onTick(newTime);
                if (newTime <= 0) {
                    clearInterval(interval);
                    if (onExpire) onExpire();
                }
                return newTime;
            });
        }, 1000);

        return () => clearInterval(interval);
    }, [remaining, onExpire, onTick]);

    const formatTime = (seconds) => {
        const m = Math.floor(seconds / 60);
        const s = seconds % 60;
        return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
    };

    const isUrgent = remaining < 300; // < 5 mins

    return (
        <div className={`font-mono text-xl font-bold ${isUrgent ? 'text-red-500 animate-pulse' : 'text-gray-400'}`}>
            ⏱ {formatTime(remaining)}
        </div>
    );
}
