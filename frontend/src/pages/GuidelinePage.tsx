import React from 'react';
import useDisableSearch from "../components/hooks/useDisableSerach";

const GuidelinePage: React.FC = () => {
    useDisableSearch();

    return (
        <div className="px-6 py-6">
            <h1 className="text-3xl font-bold text-gray-800 mt-5">Work Time Guidelines</h1>
            <div className="mt-8 text-gray-600">
                <h2 className="text-xl font-semibold text-gray-700 mb-3">General Provisions</h2>
                <ul className="list-disc list-inside text-gray-600 space-y-0.5">
                    <li>Regular working hours are from <span className="text-purple-600 font-semibold">08:00 to 18:00</span> daily.</li>
                    <li>The maximum permissible working time is <span className="text-purple-600 font-semibold">10 hours per day</span>, although no more than <span className="text-purple-600 font-semibold">8 hours</span> is recommended.</li>
                    <li>Working on Sundays and public holidays is not allowed.</li>
                    <li>Contractually agreed hours must be precisely adhered to.</li>
                </ul>

                <h2 className="text-xl font-semibold text-gray-700 mt-8 mb-3">Break Regulations</h2>
                <ul className="list-disc list-inside text-gray-600 space-y-0.5">
                    <li>A minimum break of <span className="text-purple-600 font-semibold">30 minutes</span> is required after 6 hours of working.</li>
                    <li>Breaks are defined implicit as part of the working time.</li>
                </ul>

                <h2 className="text-xl font-semibold text-gray-700 mt-8 mb-3">Additional Notes</h2>
                <p className="text-gray-600">
                    It is important that all work time entries are carefully documented and regularly reviewed
                    to ensure compliance with these guidelines. If there are any questions or uncertainties,
                    employees should contact their supervisors or the secretary.
                </p>
            </div>
        </div>
    );
};

export default GuidelinePage;
