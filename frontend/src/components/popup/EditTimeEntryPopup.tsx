import React, { useState } from 'react';
import { usePopup } from "./PopupContext";
import DialogButton from "../input/DialogButton";
import ShortInputField from "../input/ShortInputField";
import RoundedIconBox from "../../shared/RoundedIconBox";
import HorizontalSeparator from "../../shared/HorizontalSeparator";
import IntuitiveDatePicker from "../input/IntuitiveDatePicker";
import IntuitiveTimePicker from "../input/IntuitiveTimePicker";
import {TimeEntry} from "../../interfaces/TimeEntry";
import {updateTimeEntry} from "../../services/TimeEntryService";
import {createTimeEntryValidation} from "../validation/InputValidation";
import {BreakIcon} from "../../assets/iconComponents/BreakIcon";
import {TrackTimeIcon} from "../../assets/iconComponents/TrackTimeIcon";
import Dropdown from "../input/Dropdown";
import {ActivityIcon} from "../../assets/iconComponents/ActivityIcon";

interface EditTimeEntryPopupProps {
    entryData: TimeEntry;
}

const EditTimeEntryPopup: React.FC<EditTimeEntryPopupProps> = ({ entryData }) => {
    const { closePopup } = usePopup();
    const [activity, setActivity] = useState<string>(entryData.activity);
    const [project, setProject] = useState<string>(entryData.projectName);
    const [selectedDate, setSelectedDate] = useState<Date>(new Date(entryData.startTime));
    const [startTime, setStartTime] = useState<string>(new Date(entryData.startTime).toLocaleTimeString());
    const [endTime, setEndTime] = useState<string>(new Date(entryData.endTime).toLocaleTimeString());
    const [breakTime, setBreakTime] = useState<number>(entryData.breakTime);

    const activityTypeOptions = ["Projektbesprechung", "Projektarbeit"].map(role => ({
        label: role,
        value: role
    }));

    const [activityType, setActivityType] = useState(entryData.activityType || activityTypeOptions[0].value);

    const handleSubmit = async () => {
        const result = createTimeEntryValidation(activity, project, selectedDate, startTime, endTime, breakTime);
        if (!result.valid) {
            if (result.errors && result.errors.length > 0) {
                result.errors.forEach(error => {
                    alert(error.message);
                    console.log('Validation error:', error.message);
                    return;
                });
            }
            return;
        }

        const startDate = new Date(selectedDate);
        startDate.setHours(parseInt(startTime.split(':')[0]), parseInt(startTime.split(':')[1]));
        const endDate = new Date(selectedDate);
        endDate.setHours(parseInt(endTime.split(':')[0]), parseInt(endTime.split(':')[1]));

        const formattedStartTime = startDate.toISOString();
        const formattedEndTime = endDate.toISOString();

        const updatedEntryData = {
            ...entryData,
            activity,
            projectName: project,
            activityType: activityType,
            startTime: formattedStartTime,
            endTime: formattedEndTime,
            breakTime: breakTime,
        };

        try {
            console.log(updatedEntryData);
            await updateTimeEntry(updatedEntryData);
            closePopup();
            window.location.reload();
        } catch (error) {
            alert(`Failed to update work entry:\n${error}`);
            console.error('Error updating work entry:', error);
        }
    };

    return (
        <div className="flex flex-col gap-4">
            <div className="flex flex-row gap-4">
                <RoundedIconBox icon={<TrackTimeIcon/>} width={"w-[60px]"} height={"h-[60px] p-3.5"}/>
                <div className="flex flex-col gap-[1px]">
                    <h2 className="text-2xl font-bold">Edit Time Entry</h2>
                    <p className="text-lg font-medium text-[#707070]">Update the fields below to edit the entry</p>
                </div>
            </div>

            <HorizontalSeparator/>

            <form className="space-y-6">
                <div className="flex flex-row gap-4">
                    <ShortInputField
                        icon={<ActivityIcon/>}
                        title="Activity"
                        type="text"
                        placeholder="Activity"
                        value={activity}
                        onChange={setActivity}
                    />
                    <ShortInputField
                        icon={<ActivityIcon/>}
                        type="text"
                        title="Project"
                        placeholder="Project"
                        value={project}
                        onChange={setProject}
                    />
                </div>

                <div className="w-7/12">
                    <Dropdown title="Activity Type" value={activityType} onChange={setActivityType}
                              icon={<ActivityIcon/>}
                              options={activityTypeOptions}/>
                </div>

                <div className="flex flex-col gap-1.5">
                    <h2 className="text-md font-semibold">{"Working Time"}</h2>
                    <IntuitiveDatePicker externalSelectedDate={selectedDate} onDateSelect={setSelectedDate}/>
                    <div className="flex flex-row mt-2 justify-between w-7/12 items-center">
                        <IntuitiveTimePicker value={startTime} onChange={setStartTime}/>
                        <p className="text-center items-center justify-center text-gray-700 font-extrabold">—</p>
                        <IntuitiveTimePicker value={endTime} onChange={setEndTime}/>
                    </div>
                </div>

                <ShortInputField
                    icon={<BreakIcon/>}
                    type="number"
                    title={"Break Time"}
                    placeholder="15"
                    suffix={"min"}
                    value={breakTime.toString()}
                    onChange={(value) => setBreakTime(parseInt(value))}
                />

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

export default EditTimeEntryPopup;
