import React from 'react';

interface ContractInfoProps {
  label: string;
  value: string;
}


const ContractInfo: React.FC<ContractInfoProps> = ({ label, value }) => {
  return (
    <div className="flex flex-col gap-0.5">
      <span className="text-sm font-semibold text-subtitle">{label}</span>
      <span className="text-md text-[#494949] font-semibold">{value}</span>
    </div>
  );
}

export default ContractInfo;
