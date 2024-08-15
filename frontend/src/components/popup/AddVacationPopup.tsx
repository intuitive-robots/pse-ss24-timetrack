import React, { useState } from 'react';
import { usePopup } from "./PopupContext";
import DialogButton from "../input/DialogButton";
import RoundedIconBox from "../../shared/RoundedIconBox";
import HorizontalSeparator from "../../shared/HorizontalSeparator";
import IntuitiveDatePicker from "../input/IntuitiveDatePicker";
import {createVacationEntry} from "../../services/TimeEntryService";
import IntuitiveTimePicker from "../input/IntuitiveTimePicker";
import {validateCreateVacationEntry} from "../validation/InputValidation";
import {useAuth} from "../../context/AuthContext";
import {minutesToHourMinuteFormatted} from "../../utils/TimeUtils";
import {VacationIcon} from "../../assets/iconComponents/VacationIcon";

const AddVacationPopup: React.FC = () => {
    const { closePopup } = usePopup();

    const [selectedDate, setSelectedDate] = useState<Date>(new Date());
    const [duration, setDuration] = useState('');

    const {user} = useAuth();

    const handleSubmit = async () => {
        if (!validateCreateVacationEntry(selectedDate, duration).valid) {
            return;
        }

        const hours = parseInt(duration.split(':')[0]);
        const minutes = parseInt(duration.split(':')[1]);

        const startDate = new Date(selectedDate);
        startDate.setHours(8, 0);  // Start time is always 08:00 AM
        const endDate = new Date(startDate);
        endDate.setHours(startDate.getHours() + hours, startDate.getMinutes() + minutes);

        const formattedStartTime = startDate.toISOString();
        const formattedEndTime = endDate.toISOString();

        const entryData = {
            startTime: formattedStartTime,
            endTime: formattedEndTime,
        };

        try {
            const createdEntry = await createVacationEntry(entryData);
            console.log('Vacation entry created:', createdEntry);
            closePopup();
            window.location.reload();
        } catch (error) {
            alert(`Failed to create vacation entry:\n${error}`);
            console.error('Error creating vacation entry:', error);
        }
    };

    return (
        <div className="flex flex-col gap-4 min-w-[30rem]">
            <div className="flex flex-row gap-4">
                <RoundedIconBox icon={<VacationIcon/>} width={"w-[60px]"} height={"h-[60px] p-3.5"} />
                <div className="flex flex-col gap-[1px]">
                    <h2 className="text-2xl font-bold">Add Vacation Entry</h2>
                    <p className="text-lg font-medium text-[#707070]">Fill in the fields below to add a vacation entry</p>
                </div>
            </div>

            <HorizontalSeparator />

            {user && user.contractInfo && (
                <div className="p-4 bg-white border border-gray-200 rounded-lg shadow-sm w-fit h-fit">
                    <h2 className="text-md text-[#C1C1C1] font-semibold mb-1">Available Vacation</h2>
                    <p className="text-2xl font-bold text-[#343434] ml-1">
                        {minutesToHourMinuteFormatted(user.contractInfo.vacationMinutes ?? 0)}
                    </p>
                </div>
            )}

            <HorizontalSeparator/>

            <form className="space-y-6">
                <div className="flex flex-col gap-5">
                    <div>
                    <h2 className="text-md font-semibold mb-1.5">{"Vacation Date"}</h2>
                        <IntuitiveDatePicker onDateSelect={setSelectedDate}/>
                    </div>
                    <div>
                        <h2 className="text-md font-semibold mb-1.5">Vacation Duration</h2>
                        <IntuitiveTimePicker value={duration} onChange={setDuration}/>
                    </div>
                </div>

                <div className="flex flex-row gap-3 justify-end">
                    <DialogButton
                        label="Cancel"
                        secondary={true}
                        onClick={closePopup}
                    />
                    <DialogButton
                        label="Add Entry"
                        primary={true}
                        onClick={handleSubmit}
                    />
                </div>
            </form>
        </div>
    );
};

export default AddVacationPopup;
