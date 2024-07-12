import React from 'react';
import { usePopup } from "./PopupContext";
import DialogButton from "../input/DialogButton";
import DisplayField from "../display/DisplayField";
import ActivityIcon from "../../assets/images/activity_icon.svg";
import { User } from "../../interfaces/User";
import {Roles} from "../auth/roles";
import {UserIcon} from "../../assets/iconComponents/UserIcon";

interface ViewUserPopupProps {
    userData: User;
}

const ViewUserPopup: React.FC<ViewUserPopupProps> = ({ userData }) => {
    const { closePopup } = usePopup();

    return (
        <div className="px-4 py-4 ">
            <h1 className="text-2xl font-bold mb-4">User Details</h1>
            <div className="grid grid-cols-2 gap-4">
                <DisplayField label="Username" value={userData.username} icon={<UserIcon/>} />
                <DisplayField label="Role" value={userData.role} icon={<UserIcon/>} />
                <DisplayField label="First Name" value={userData.personalInfo.firstName} icon={<UserIcon/>} />
                <DisplayField label="Last Name" value={userData.personalInfo.lastName} icon={<UserIcon/>} />
                <DisplayField label="Email" value={userData.personalInfo.email} icon={<UserIcon/>} />
                <DisplayField label="Personal Number" value={userData.personalInfo.personalNumber} icon={<UserIcon/>} />

                {userData.role === Roles.Hiwi && (
                    <>
                        <DisplayField label="Hourly Wage" value={`${userData.contractInfo?.hourlyWage?.toFixed(2) ?? "N/A"} €`} icon={ActivityIcon} />
                        <DisplayField label="Monthly Working Hours" value={`${userData.contractInfo?.workingHours ?? "N/A"} hours`} icon={ActivityIcon} />
                        <DisplayField label="Supervisor" value={userData.supervisor ?? "N/A"} icon={<UserIcon/>} />
                    </>
                )}
            </div>

            <div className="mt-6 flex justify-end">
                <DialogButton label="Close" onClick={closePopup} primary={true} />
            </div>
        </div>
    );
};

export default ViewUserPopup;
