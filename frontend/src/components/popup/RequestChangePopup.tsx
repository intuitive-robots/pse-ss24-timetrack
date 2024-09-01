import React, {useState} from 'react';
import {usePopup} from "./PopupContext";
import {requestChange} from "../../services/TimesheetService";
import {Timesheet} from "../../interfaces/Timesheet";
import DialogButton from "../input/DialogButton";
import HorizontalSeparator from "../../shared/HorizontalSeparator";
import RoundedIconBox from "../../shared/RoundedIconBox";
import {RequestChangeIcon} from "../../assets/iconComponents/RequestChangeIcon";

interface RequestChangePopupProps {
  username: string | undefined;
  timesheet: Timesheet;

}

const RequestChangePopup: React.FC<RequestChangePopupProps> = ({ username, timesheet }) => {
    const { closePopup } = usePopup();

    const [description, setDescription] = useState('');


    const handleSubmit = async () => {
        if (!description) {
            alert("Please fill out the description field.");
            return;
        }


        try {
            const result = await requestChange(timesheet._id, description);
            closePopup();
            window.location.reload();
        } catch (error) {
            console.error('Error requesting change for timesheet:', error);
            alert('Failed to request change for the timesheet' + error);
        }
    };

    return (
        <div className="">
            <div className="flex flex-row gap-4 items-center mb-2">
                <RoundedIconBox icon={<RequestChangeIcon/>} width={"w-[60px]"} height={"h-[60px] p-3.5"}/>
                <div className="flex flex-col">
                    <h2 className="text-2xl font-bold">Request Change</h2>
                    <p className="text-lg font-medium text-[#707070]">Request changes to {username}'s
                        timesheet.</p>
                </div>
            </div>

            <HorizontalSeparator/>

            <form className="space-y-6 mt-4">
                <div className="flex flex-col gap-0.5">
                    <h2 className="text-md font-semibold">Description</h2>
                    <textarea
                        className="mt-1 block w-full text-md px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500"
                        placeholder="Describe the changes you request."
                        value={description}
                        maxLength={35}
                        onChange={(e) => setDescription(e.target.value)}
                        rows={3}
                    />
                </div>

                <div className="flex flex-row gap-3 justify-end">
                    <DialogButton
                        label="Cancel"
                        secondary={true}
                        onClick={closePopup}
                    />
                    <DialogButton
                        label="Request"
                        primary={true}
                        onClick={handleSubmit}
                    />
                </div>
            </form>
        </div>
    );
};

export default RequestChangePopup;
