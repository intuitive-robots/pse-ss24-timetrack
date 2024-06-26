import React from 'react';
import ContractInfo from "./ContractInfo";

const ContractDetails = () => {
  return (
    <div className="mb-6">
        <h2 className="font-bold text-md text-[#B5B5B5] mb-3">Your Contract</h2>
        <div className="grid grid-cols-2 gap-4 text-sm">
            <ContractInfo label={"Team"} value={"Institut für Intuitive Robotic"}/>
            <ContractInfo label={"Start Date"} value={"Feb 5th, 2024"}/>
            <ContractInfo label={"Working Time"} value={"80h per Month"}/>
            <ContractInfo label={"Hourly Wage"} value={"14,20 €"}/>
        </div>
    </div>
  );
}

export default ContractDetails;
