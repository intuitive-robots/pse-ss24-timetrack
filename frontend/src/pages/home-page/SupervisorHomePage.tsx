import React, { useState } from 'react';
import HiwiCard from "../../components/HiwiCard";
import ProfilePlaceholder from "../../assets/images/profile_placeholder.svg";
import StatusFilter from "../../components/StatusFilter";
import { StatusType } from "../../interfaces/StatusType";

/**
 * Supervisor Homepage component serves as the main landing page for the application.
 *
 * @returns {React.ReactElement} A React Element that renders the main homepage of the application.
 */
const SupervisorHomePage = (): React.ReactElement => {
    const [filter, setFilter] = useState<StatusType | null>(null);

    const employees = [
        { name: 'Nico', lastName: 'Revision', role: 'Hilfswissenschaftler', profileImageUrl: ProfilePlaceholder, status: StatusType.Revision },
        { name: 'Tom', lastName: 'Revision', role: 'Hilfswissenschaftler', profileImageUrl: ProfilePlaceholder, status: StatusType.Revision },
        { name: 'Nico', lastName: 'Waiting', role: 'Hilfswissenschaftler', profileImageUrl: ProfilePlaceholder, status: StatusType.Waiting },
        { name: 'Tom', lastName: 'Pending', role: 'Hilfswissenschaftler', profileImageUrl: ProfilePlaceholder, status: StatusType.Pending },
        { name: 'Nico', lastName: 'Pending', role: 'Hilfswissenschaftler', profileImageUrl: ProfilePlaceholder, status: StatusType.Pending },
        { name: 'Tom', lastName: 'Complete', role: 'Hilfswissenschaftler', profileImageUrl: ProfilePlaceholder, status: StatusType.Complete },
        { name: 'Nico', lastName: 'Complete', role: 'Hilfswissenschaftler', profileImageUrl: ProfilePlaceholder, status: StatusType.Complete },
        { name: 'Tom', lastName: 'Complete', role: 'Hilfswissenschaftler', profileImageUrl: ProfilePlaceholder, status: StatusType.Complete },
    ];

    const filteredEmployees = filter
        ? employees.filter(employee => employee.status === filter)
        : employees;

    return (
        <div className="px-6 py-6">
            <p className="text-lg font-medium text-subtitle">Institute for Intuitive Robotics</p>
            <h1 className="text-3xl font-bold text-gray-800 mt-5">Hello Nico,</h1>
            <h2 className="text-md font-medium text-subtitle mt-1">You have X assigned employees with Y open
                timesheets</h2>
            <div className="h-5"/>
            <div className="px-4">
                <StatusFilter setFilter={setFilter}/>

                <div className="flex flex-col py-6 overflow-y-auto max-h-96">
                    {filteredEmployees.map((employee, index) => (
                        <HiwiCard
                            key={index}
                            name={employee.name}
                            lastName={employee.lastName}
                            role={employee.role}
                            profileImageUrl={employee.profileImageUrl}
                            status={employee.status}
                            onCheck={() => {
                            }}
                        />
                    ))}
                </div>
            </div>
        </div>
    );
};

export default SupervisorHomePage;
