import React, {useState} from 'react';
import {usePopup} from "./PopupContext";
import ShortInputField from "../input/ShortInputField";
import ActivityIcon from "../../assets/images/activity_icon.svg";
import BreakIcon from "../../assets/images/coffee_icon.svg";
import TimeIcon from "../../assets/images/time_icon.svg";
import CalendarIcon from "../../assets/images/calendar_day.svg";
import DialogButton from "../input/DialogButton";
import {createWorkEntry} from "../../services/TimeEntryService";
import "react-datepicker/dist/react-datepicker.css";
import RoundedIconBox from "../../shared/RoundedIconBox";
import HorizontalSeparator from "../../shared/HorizontalSeparator";
import IntuitiveDatePicker from "../input/IntuitiveDatePicker";

const TrackTimePopup: React.FC = () => {
    const { closePopup } = usePopup();

    const [activity, setActivity] = useState('');
    const [project, setProject] = useState('');
    const [selectedDate, setSelectedDate] = useState<Date>(new Date());
    const [startTime, setStartTime] = useState('');
    const [endTime, setEndTime] = useState('');
    const [breakTime, setBreakTime] = useState(0);

    const handleSubmit = async () => {
        if (!activity || !project || !selectedDate || !startTime || !endTime || !breakTime) {
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
            activity,
            projectName: project,
            startTime: `${formattedStartTime}`,
            endTime: `${formattedEndTime}`,
            breakTime: breakTime,
        };

        try {
            const createdEntry = await createWorkEntry(entryData);
            console.log('Work entry created:', createdEntry);
            closePopup();
            window.location.reload();
        } catch (error) {
            alert("Failed to create work entry.");
            console.error('Error creating work entry:', error);
        }
    };

    return (
        <div className="flex flex-col gap-4">
            <div className="flex flex-row gap-4">
                <RoundedIconBox iconSrc={ActivityIcon}/>
                <div className="flex flex-col gap-1">
                    <h2 className="text-2xl font-bold">Create Time Entry</h2>
                    <p className="text-lg font-medium text-[#707070]">Fill in the fields below to add a Working
                        Day</p>
                </div>
            </div>

            <HorizontalSeparator/>


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
                    <h2 className="text-md font-semibold mb-1.5">{"Working Time"}</h2>
                    <IntuitiveDatePicker onDateSelect={setSelectedDate}/>
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
