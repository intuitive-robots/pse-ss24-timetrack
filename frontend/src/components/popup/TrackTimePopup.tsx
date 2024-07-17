import React, {useState} from 'react';
import {usePopup} from "./PopupContext";
import ShortInputField from "../input/ShortInputField";
import TrackTimeIcon from "../../assets/images/add_track_time.svg";
import ActivityIcon from "../../assets/images/activity_icon.svg";
import BreakIcon from "../../assets/images/coffee_icon.svg";
import DialogButton from "../input/DialogButton";
import {createWorkEntry} from "../../services/TimeEntryService";
import RoundedIconBox from "../../shared/RoundedIconBox";
import HorizontalSeparator from "../../shared/HorizontalSeparator";
import IntuitiveDatePicker from "../input/IntuitiveDatePicker";
import IntuitiveTimePicker from "../input/IntuitiveTimePicker";
import Dropdown from "../input/Dropdown";
import {createTimeEntryValidation} from "../validation/InputValidation";

const TrackTimePopup: React.FC = () => {
    const { closePopup } = usePopup();

    const [activity, setActivity] = useState('');
    const [activityType, setActivityType] = useState('');
    const [project, setProject] = useState('');
    const [selectedDate, setSelectedDate] = useState<Date>(new Date());
    const [startTime, setStartTime] = useState('');
    const [endTime, setEndTime] = useState('');
    const [breakTime, setBreakTime] = useState(0);
    const [workingTimeWarning, setWorkingTimeWarning] = useState(false);


    const activityTypeOptions = ["Projektbesprechung", "Projektarbeit"].map(role => ({
        label: role,
        value: role
    }));

    /*TODO: add activity type */
    const handleSubmit = async () => {
        const result = createTimeEntryValidation(activity, project, selectedDate, startTime, endTime, breakTime);
        if (!result.valid) {
            if (result.errors && result.errors.length > 0) {
                result.errors.forEach(error => {
                    if (error.property === "workTimeSpan") {
                        setWorkingTimeWarning(true);
                    }
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
                <RoundedIconBox iconSrc={TrackTimeIcon} width={"w-[60px]"} height={"h-[60px] p-3.5"}/>
                <div className="flex flex-col gap-[1px]">
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
                <div className="w-7/12">
                    <Dropdown title="Activity Type" value={activityType} onChange={setActivityType} icon={ActivityIcon}
                              options={activityTypeOptions}/>
                </div>
                <div className="flex flex-col gap-1.5">
                    <h2 className="text-md font-semibold">{"Working Time"}</h2>
                    <IntuitiveDatePicker onDateSelect={setSelectedDate}/>
                    <div className="flex flex-row items-center mt-2 w-full">
                        <div className="flex flex-row justify-between items-center w-7/12">
                            <IntuitiveTimePicker value={startTime} onChange={setStartTime}/>
                            <p className="text-center items-center justify-center text-gray-700 font-extrabold">—</p>
                            <IntuitiveTimePicker value={endTime} onChange={setEndTime}/>
                        </div>
                        {workingTimeWarning && (
                            <p className="text-red-600 font-bold ml-4 whitespace-nowrap">Warning: Working time {'>'} 8h.</p>
                        )}
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
