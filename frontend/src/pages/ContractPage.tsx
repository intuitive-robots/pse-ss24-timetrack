import React from "react";
import UserInfo from "../components/UserInfo";
import ProfilePicture from "../assets/images/profile_placeholder.png"
import ContactButton from "../components/input/ContactButton";
import MailIcon from "../assets/images/contact_mail.svg"
import SlackIcon from "../assets/images/contact_slack.svg"
import HorizontalSeparator from "../shared/HorizontalSeparator";
import ContractDetails from "../components/contract/ContractDetails";
import SignatureUpload from "../components/contract/SignatureUpload";
import UserContactInfo from "../components/contract/UserContactInfo";
import {useAuth} from "../context/AuthContext";

const ContractPage = (): React.ReactElement => {
    const { user } = useAuth();

    return (
        <div className="px-6 py-6">
            <h1 className="text-3xl font-bold text-gray-800 mt-5">Contract Details</h1>
            <div className="flex flex-col min-w-96 w-7/12 mt-5 py-7 px-10 bg-white shadow-card-shadow border-1.7 border-card-gray rounded-lg gap-5">
                <div className="">
                    <h2 className="font-bold text-md text-[#B5B5B5] mb-3">Your Supervisor</h2>
                    {/*<div className="flex flex-row justify-between">*/}
                    {/*    <UserInfo name="Max" lastName="Muster" role="Supervisor" profileImageUrl={ProfilePicture}/>*/}
                    {/*    <div className="flex flex-row gap-3">*/}
                    {/*        <ContactButton icon={MailIcon} onClick={() => {}}/>*/}
                    {/*        <ContactButton icon={SlackIcon} onClick={() => {}}/>*/}
                    {/*    </div>*/}
                    {/*</div>*/}
                    {user ? <UserContactInfo username={user.username}/> : <div/>}

                </div>
                <HorizontalSeparator/>
                <ContractDetails/>
                <SignatureUpload/>
            </div>
        </div>
    );
};

export default ContractPage;