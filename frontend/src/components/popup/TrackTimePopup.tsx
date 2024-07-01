import React, {useState} from 'react';
import {usePopup} from "./PopupContext";
import ShortInputField from "../input/ShortInputField";
import ActivityIcon from "../../assets/images/activity_icon.svg";
import BreakIcon from "../../assets/images/coffee_icon.svg";
import TimeIcon from "../../assets/images/time_icon.svg";
import CalendarIcon from "../../assets/images/calendar_day.svg";
import DialogButton from "../input/DialogButton";
import {createWorkEntry} from "../../services/TimeEntryService";

const TrackTimePopup: React.FC = () => {
    const { closePopup } = usePopup();

    const [activity, setActivity] = useState('');
    const [project, setProject] = useState('');
    const [date, setDate] = useState('');
    const [startTime, setStartTime] = useState('');
    const [endTime, setEndTime] = useState('');
    const [breakTime, setBreakTime] = useState(0);

    const handleSubmit = async () => {
        if (!activity || !project || !date || !startTime || !endTime || !breakTime) {
            alert("Please fill all the fields correctly.");
            return;
        }

        const dateParts = date.split(".");
        if (dateParts.length !== 3) {
            alert("Invalid date format. Please use DD.MM.YYYY format.");
            return;
        }
        const formattedDate = `${dateParts[2]}-${dateParts[1]}-${dateParts[0]}`;

        const fullStartTime = new Date(`${formattedDate}T${startTime}:00`);
        const fullEndTime = new Date(`${formattedDate}T${endTime}:00`);

        if (isNaN(fullStartTime.getTime()) || isNaN(fullEndTime.getTime())) {
            alert("Invalid date or time values.");
            return;
        }

        const formattedStartTime = fullStartTime.toISOString();
        const formattedEndTime = fullEndTime.toISOString();


        const entryData = {
            activity,
            projectName: project,
            startTime: `${formattedStartTime}`,
            endTime: `${formattedEndTime}`,
            breakTime: breakTime,
        };
        console.log(entryData)

        try {
            const createdEntry = await createWorkEntry(entryData);
            console.log('Work entry created:', createdEntry);
            closePopup();
        } catch (error) {
            alert("Failed to create work entry.");
            console.error('Error creating work entry:', error);
        }
    };

    return (
        <div className="">
            <div className="flex flex-col gap-1">
                <h2 className="text-2xl font-bold">Create Time Entry</h2>
                <p className="text-lg font-medium text-[#707070] mb-6">Fill in the fields below to add a Working Day</p>
            </div>

            <form className="space-y-6">
                <div className="flex flex-row gap-4">
                    <ShortInputField
                        icon={ActivityIcon}
                        title="Activity"
                        type="text"
                        placeholder="Activity"
                        value={activity}
                        onChange={setActivity}
                    />
                    <ShortInputField
                        icon={ActivityIcon}
                        type="text"
                        title="Project"
                        placeholder="Project"
                        value={project}
                        onChange={setProject}
                    />
                </div>

                <div className="flex flex-col gap-3">
                    <ShortInputField
                            icon={CalendarIcon}
                            type="text"
                            title="Working Time"
                            placeholder="23.04.2024"
                            value={date}
                            onChange={setDate}
                    />
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
                            placeholder="12:00 AM"
                            value={endTime}
                            onChange={setEndTime}
                        />
                    </div>

                </div>

                <ShortInputField
                        icon={BreakIcon}
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
                        label="Add Entry"
                        primary={true}
                        onClick={handleSubmit}
                    />
                </div>
            </form>
        </div>
    );
};

export default TrackTimePopup;
