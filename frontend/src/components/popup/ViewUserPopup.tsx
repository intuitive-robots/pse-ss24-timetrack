import React from 'react';
import { usePopup } from "./PopupContext";
import DialogButton from "../input/DialogButton";
import DisplayField from "../display/DisplayField";
import ActivityIcon from "../../assets/images/activity_icon.svg";
import { User } from "../../interfaces/User";
import {Roles} from "../auth/roles";
import {UserIcon} from "../../assets/iconComponents/UserIcon";
import {RoleIcon} from "../../assets/iconComponents/RoleIcon";
import {NameIcon} from "../../assets/iconComponents/NameIcon";
import {MailIcon} from "../../assets/iconComponents/MailIcon";
import {IdIcon} from "../../assets/iconComponents/IdIcon";
import {SalaryIcon} from "../../assets/iconComponents/SalaryIcon";
import {BriefcaseIcon} from "../../assets/iconComponents/BriefcaseIcon";
import {SupervisorIcon} from "../../assets/iconComponents/SupervisorIcon";
import HorizontalSeparator from "../../shared/HorizontalSeparator";

interface ViewUserPopupProps {
    userData: User;
}

const ViewUserPopup: React.FC<ViewUserPopupProps> = ({ userData }) => {
    const { closePopup } = usePopup();

    return (
        <div className="px-4 py-4">
            <h1 className="text-2xl font-bold mb-4">User Details</h1>
            <div className="grid grid-cols-3 gap-4">
                <DisplayField label="Username" value={userData.username} icon={<UserIcon/>}/>
                <DisplayField label="Role" value={userData.role} icon={<RoleIcon/>}/>
                <div className="col-span-full">
                    <HorizontalSeparator/>
                </div>
                <h1 className="col-span-full text-md text-[#B5B5B5] font-bold">Personal Information</h1>

                <DisplayField label="First Name" value={userData.personalInfo.firstName} icon={<NameIcon/>}/>
                <DisplayField label="Last Name" value={userData.personalInfo.lastName} icon={<NameIcon/>}/>
                <div className="col-span-1"></div>
                <DisplayField label="Email" value={userData.personalInfo.email} icon={<MailIcon/>}/>
                <DisplayField label="Personal Number" value={userData.personalInfo.personalNumber} icon={<IdIcon/>}/>
                <DisplayField label="Slack-ID" value={userData.slackId ?? "N/A"} icon={<IdIcon/>}/>

                {userData.role === Roles.Hiwi && (
                    <>
                        <div className="col-span-full">
                            <HorizontalSeparator/>
                        </div>
                        <h1 className="col-span-full text-md text-[#B5B5B5] font-bold">Contract Information</h1>
                        <DisplayField label="Hourly Wage"
                                      value={`${userData.contractInfo?.hourlyWage?.toFixed(2) ?? "N/A"} €`}
                                      icon={<SalaryIcon/>}/>
                        <DisplayField label="Monthly Working Hours"
                                      value={`${userData.contractInfo?.workingHours ?? "N/A"} hours`}
                                      icon={<BriefcaseIcon/>}/>
                        <DisplayField label="Supervisor" value={userData.supervisor ?? "N/A"} icon={<SupervisorIcon/>}/>
                    </>
                )}
            </div>

            <div className="mt-6 flex justify-end">
                <DialogButton label="Close" onClick={closePopup} primary={true}/>
            </div>
        </div>
    );
};

export default ViewUserPopup;
