import React from 'react';
import HorizontalSeparator from "../../shared/HorizontalSeparator";

interface StepIndicatorProps {
    steps: string[];
    currentStep: number;
}

const StepIndicator: React.FC<StepIndicatorProps> = ({ steps, currentStep }) => {
    return (
        <div className="flex flex-col gap-4">
            <HorizontalSeparator/>
            <div className="flex justify-center space-x-6">
                {steps.map((step, index) => (
                    <div key={index}
                         className={`text-center ${currentStep === index + 1 ? 'text-black font-bold' : 'text-gray-400'}`}>
                        <div className="text-xs uppercase tracking-wider">{`Step ${index + 1}`}</div>
                        <div className="text-sm">{step}</div>
                    </div>
                ))}
            </div>
            <HorizontalSeparator/>
        </div>
    );
};

export default StepIndicator;
