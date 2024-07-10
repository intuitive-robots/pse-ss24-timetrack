import React, {useEffect, useState} from 'react';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';

interface WorkingHoursProgressProps {
    totalHours: number;
    goalHours: number;
}

const WorkingHoursProgress: React.FC<WorkingHoursProgressProps> = ({ totalHours, goalHours }) => {
    const [progress, setProgress] = useState(0);
    const percentage = (totalHours / goalHours) * 100;

    useEffect(() => {
        const timeout = setTimeout(() => {
            setProgress(percentage);
        }, 0);
        return () => clearTimeout(timeout);
    }, [percentage]);



    return (
        <div className="bg-white flex px-5 py-4 pb-8 gap-4 shadow-card-shadow border-1.7 border-card-gray rounded-lg text-sm">
            <div className="flex flex-col gap-2">
                <p className="text-sm text-[#C1C1C1] font-semibold">Total hours working</p>
                <h1 className="ml-3 text-4xl font-bold text-gray-800">{totalHours} <span className="text-[#C1C1C1] text-2xl">/ {goalHours}</span></h1>
            </div>
            <div style={{width: 70, height: 70}}>
                <CircularProgressbar
                    value={progress}
                    strokeWidth={20}
                    styles={buildStyles({
                        strokeLinecap: 'butt',
                        pathTransitionDuration: 0.7,
                        pathColor: `rgba(176, 131, 255)`,
                        trailColor: '#F1EAFF',
                        backgroundColor: '#3e98c7',
                        textSize: '0px'
                    })}
                    minValue={0}
                    maxValue={100}
                />
            </div>
        </div>
    );
};

export default WorkingHoursProgress;
