import React, {useEffect, useState} from 'react';
import HorizontalSeparator from "../../shared/HorizontalSeparator";
import SignatureUpload from "../../components/contract/SignatureUpload";
import {getHiwis} from "../../services/UserService";
import {User} from "../../interfaces/User";
import useDisableSearch from "../../components/hooks/useDisableSerach";

const SupervisorEmployeesPage: React.FC = () => {
    const [hiwis, setHiwis] = useState<User[] | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    useDisableSearch();

    useEffect(() => {
        getHiwis().then(hiwis => {
            setHiwis(hiwis);
            setIsLoading(false);
        }).catch(error => {
            console.error("Failed to fetch hiwis:", error);
            setIsLoading(true);
        });
    }, []);

    return (
        <div className="px-6 py-6">
            <h1 className="text-3xl font-bold text-gray-800 mt-5">Employees</h1>
            <div className="flex flex-col min-w-96 w-6/12 mt-5 py-7 px-10 bg-white shadow-card-shadow border-1.7 border-card-gray rounded-lg gap-5">
                <div className={""}>
                    <h2 className="font-bold text-md text-[#B5B5B5] mb-3">Assigned Hiwis - (Rework Planned Soon)</h2>
                    <div className={`transition-all duration-300 ease-in-out ${isLoading ? 'blur-sm' : 'blur-none'}`}>
                        {hiwis ? (
                            <ul className="flex flex-col gap-2 ml-2">
                                {hiwis.map(hiwi => (
                                    <li className="text-md font-medium text-gray-600" key={hiwi._id}>
                                        • {hiwi.personalInfo.firstName} {hiwi.personalInfo.lastName}
                                    </li>
                                ))}
                            </ul>
                        ) : (
                            <ul className="flex flex-col gap-2 ml-2">
                                <li className="text-md font-medium text-gray-600">
                                    • Peter Essig
                                </li>
                                <li className="text-md font-medium text-gray-600">
                                    • Peter Franke
                                </li>
                                <li className="text-md font-medium text-gray-600">
                                    • Peter Haag
                                </li>
                                <li className="text-md font-medium text-gray-600">
                                    • Peter Haag
                                </li>
                            </ul>
                        )}
                    </div>
                </div>
                <HorizontalSeparator/>
                <SignatureUpload/>
            </div>
        </div>
    );
};

export default SupervisorEmployeesPage;
