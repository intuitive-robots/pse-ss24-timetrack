import React from 'react';
import ContractInfo from "./ContractInfo";
import {useAuth} from "../../context/AuthContext";

const ContractDetails = () => {
    const {user, isLoading} = useAuth();
    const team = user?.personalInfo?.instituteName || "Not Available";
    const startDate = "Coming Soon"; //TODO: Get from user object
    const workingTime = `${user?.contractInfo?.workingHours || "80"}h per Month`;
    const hourlyWage = user?.contractInfo?.hourlyWage !== undefined
        ? `${user.contractInfo.hourlyWage.toFixed(2)} €`
        : "12.0 €";
    return (
        <div className="mb-6">
            <h2 className="font-bold text-md text-[#B5B5B5] mb-3">Your Contract</h2>
            <div
                className={`grid grid-cols-2 gap-4 text-sm transition-all duration-300 ease-in-out ${user ? 'blur-none' : 'blur-sm'}`}>
                <ContractInfo label="Team" value={team}/>
                <ContractInfo label="Start Date" value={startDate}/>
                <ContractInfo label="Working Time" value={workingTime}/>
                <ContractInfo label="Hourly Wage" value={hourlyWage}/>
            </div>
        </div>
    );
}

export default ContractDetails;
