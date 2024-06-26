import React from 'react';
import ContractInfo from "./ContractInfo";
import {useAuth} from "../../context/AuthContext";

const ContractDetails = () => {
    const {user} = useAuth();
    const team = user?.personalInfo?.instituteName || "Not Available";
    const startDate = "Feb 5th, 2024"; //TODO: Get from user object
    const workingTime = `${user?.contractInfo?.workingHours || "N/A"}h per Month`;
    const hourlyWage = `${user?.contractInfo?.hourlyWage || "Not Available"} €`;

    return (
        <div className="mb-6">
            <h2 className="font-bold text-md text-[#B5B5B5] mb-3">Your Contract</h2>
            <div className="grid grid-cols-2 gap-4 text-sm">
                <ContractInfo label="Team" value={team}/>
                <ContractInfo label="Start Date" value={startDate}/>
                <ContractInfo label="Working Time" value={workingTime}/>
                <ContractInfo label="Hourly Wage" value={hourlyWage}/>
            </div>
        </div>
  );
}

export default ContractDetails;
