import React, { useState } from 'react';
import { usePopup } from "./PopupContext";
import VacationIcon from "../../assets/images/vacation_icon.svg";
import DialogButton from "../input/DialogButton";
import RoundedIconBox from "../../shared/RoundedIconBox";
import HorizontalSeparator from "../../shared/HorizontalSeparator";
import IntuitiveDatePicker from "../input/IntuitiveDatePicker";
import { updateTimeEntry } from "../../services/TimeEntryService";
import {VacationEntry} from "../../interfaces/TimeEntry";
import IntuitiveTimePicker from "../input/IntuitiveTimePicker";
import {validateCreateVacationEntry} from "../validation/InputValidation";

interface EditVacationEntryPopupProps {
    entryData: VacationEntry;
}

const EditVacationEntryPopup: React.FC<EditVacationEntryPopupProps> = ({ entryData }) => {
    const { closePopup } = usePopup();
    const [selectedDate, setSelectedDate] = useState<Date>(new Date(entryData.startTime));
    const [duration, setDuration] = useState<string>(() => {
        const start = new Date(entryData.startTime);
        const end = new Date(entryData.endTime);
        const durationHours = end.getHours() - start.getHours();
        const durationMinutes = end.getMinutes() - start.getMinutes();
        return `${durationHours.toString().padStart(2, '0')}:${durationMinutes.toString().padStart(2, '0')}`;
    });

    const handleSubmit = async () => {
        if (!validateCreateVacationEntry(selectedDate, duration).valid) {
            return;
        }

        const hours = parseInt(duration);
        const startDate = new Date(selectedDate);
        startDate.setHours(8, 0);
        const endDate = new Date(startDate);
        endDate.setHours(startDate.getHours() + hours);

        const updatedEntryData = {
            ...entryData,
            startTime: startDate.toISOString(),
            endTime: endDate.toISOString(),
        };

        try {
            await updateTimeEntry(updatedEntryData);
            console.log('Vacation entry updated:', updatedEntryData);
            closePopup();
            window.location.reload();
        } catch (error) {
            alert(`Failed to update vacation entry:\n${error}`);
            console.error('Error updating vacation entry:', error);
        }
    };

    return (
        <div className="flex flex-col gap-4">
            <div className="flex flex-row gap-4">
                <RoundedIconBox icon={VacationIcon} width={"w-[60px]"} height={"h-[60px] p-3.5"} />
                <div className="flex flex-col gap-[1px]">
                    <h2 className="text-2xl font-bold">Edit Vacation Entry</h2>
                    <p className="text-lg font-medium text-[#707070]">Update the fields below to edit the vacation entry</p>
                </div>
            </div>

            <HorizontalSeparator />

            <form className="space-y-6">
                <div>
                    <h2 className="text-md font-semibold mb-1.5">{"Vacation Date"}</h2>
                    <IntuitiveDatePicker externalSelectedDate={selectedDate} onDateSelect={setSelectedDate} />
                </div>
                <div>
                    <h2 className="text-md font-semibold mb-1.5">Vacation Duration</h2>
                    <IntuitiveTimePicker value={duration} onChange={setDuration}/>
                </div>

                <div className="flex flex-row gap-3 justify-end">
                    <DialogButton
                        label="Cancel"
                        secondary={true}
                        onClick={closePopup}
                    />
                    <DialogButton
                        label="Save Changes"
                        primary={true}
                        onClick={handleSubmit}
                    />
                </div>
            </form>
        </div>
    );
};

export default EditVacationEntryPopup;
