import React from "react";
import HorizontalSeparator from "../shared/HorizontalSeparator";
import ContractDetails from "../components/contract/ContractDetails";
import SignatureUpload from "../components/contract/SignatureUpload";
import SupervisorContactInfo from "../components/contract/SupervisorContactInfo";
import useDisableSearch from "../components/hooks/useDisableSearch";

const ContractPage = (): React.ReactElement => {

    useDisableSearch();

    return (
        <div className="px-6 py-6">
            <h1 className="text-3xl font-bold text-gray-800 mt-5">Contract Details</h1>
            <div className="flex flex-col min-w-96 w-7/12 mt-5 py-7 px-10 bg-white shadow-card-shadow border-1.7 border-card-gray rounded-lg gap-5">
                <div className="">
                    <h2 className="font-bold text-md text-[#B5B5B5] mb-3">Your Supervisor</h2>
                    <SupervisorContactInfo/>

                </div>
                <HorizontalSeparator/>
                <ContractDetails/>
                <SignatureUpload/>
            </div>
        </div>
    );
};

export default ContractPage;