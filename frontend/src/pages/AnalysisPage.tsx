import React from 'react';
import useDisableSearch from "../components/hooks/useDisableSearch";

const AnalysisPage: React.FC = () => {
    useDisableSearch();

    return (
        <div className="px-6 py-6">
            <h1 className="text-3xl font-bold text-gray-800 mt-5">Analysis</h1>

        </div>
    );
};

export default AnalysisPage;
