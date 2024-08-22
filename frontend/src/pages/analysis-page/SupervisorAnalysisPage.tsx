import React from 'react';
import useDisableSearch from "../../components/hooks/useDisableSerach";

const SupervisorAnalysisPage: React.FC = () => {
    useDisableSearch();

    return (
        <div className="px-6 py-6">
            <h1 className="text-3xl font-bold text-gray-800 mt-5 mb-4">Analysis</h1>
            <h2 className="text-lg text-gray-500 font-semibold">Analysis Feature is Coming Soon to Clockwise.</h2>
        </div>
    );
};

export default SupervisorAnalysisPage;
