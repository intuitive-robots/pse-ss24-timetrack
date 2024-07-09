import React, { useState } from 'react';
import { usePopup } from "./PopupContext";
import ShortInputField from "../input/ShortInputField";
import VacationIcon from "../../assets/images/vacation_icon.svg";
import TimeIcon from "../../assets/images/time_icon.svg";
import DialogButton from "../input/DialogButton";
import RoundedIconBox from "../../shared/RoundedIconBox";
import HorizontalSeparator from "../../shared/HorizontalSeparator";
import IntuitiveDatePicker from "../input/IntuitiveDatePicker";
import {createVacationEntry} from "../../services/TimeEntryService";
import {VacationEntry} from "../../interfaces/TimeEntry";

const AddVacationPopup: React.FC = () => {
    const { closePopup } = usePopup();

    const [selectedDate, setSelectedDate] = useState<Date>(new Date());
    const [startTime, setStartTime] = useState('');
    const [endTime, setEndTime] = useState('');

    const handleSubmit = async () => {
        if (!selectedDate || !startTime || !endTime) {
            alert("Please fill all the fields correctly.");
            return;
        }

        const startDate = new Date(selectedDate);
        startDate.setHours(parseInt(startTime.split(':')[0]), parseInt(startTime.split(':')[1]));
        const endDate = new Date(selectedDate);
        endDate.setHours(parseInt(endTime.split(':')[0]), parseInt(endTime.split(':')[1]));

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
            alert("Failed to create vacation entry.");
            console.error('Error creating vacation entry:', error);
        }
    };

    return (
        <div className="flex flex-col gap-4">
            <div className="flex flex-row gap-4">
                <RoundedIconBox iconSrc={VacationIcon} width={"w-[60px]"} height={"h-[60px] p-3.5"} />
                <div className="flex flex-col gap-[1px]">
                    <h2 className="text-2xl font-bold">Add Vacation Entry</h2>
                    <p className="text-lg font-medium text-[#707070]">Fill in the fields below to add a vacation entry</p>
                </div>
            </div>

            <HorizontalSeparator />

            <form className="space-y-6">
                <div className="flex flex-col gap-3">
                    <h2 className="text-md font-semibold mb-1.5">{"Vacation Date"}</h2>
                    <IntuitiveDatePicker onDateSelect={setSelectedDate} />
                    <div className="flex gap-10">
                        <ShortInputField
                            icon={TimeIcon}
                            type="time"
                            placeholder="08:00 AM"
                            value={startTime}
                            onChange={setStartTime}
                        />
                        <ShortInputField
                            icon={TimeIcon}
                            type="time"
                            placeholder="05:00 PM"
                            value={endTime}
                            onChange={setEndTime}
                        />
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
