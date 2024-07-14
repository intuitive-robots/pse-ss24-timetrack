import React, {useEffect, useState} from "react";
import VerticalTimeLine from "../../assets/images/time_line_vertical.svg";
import YearTimespan from "../../components/timesheet/YearTimespan";
import TimesheetListView from "../../components/timesheet/TimesheetListView";
import {Timesheet} from "../../interfaces/Timesheet";
import {useAuth} from "../../context/AuthContext";
import {getTimesheets} from "../../services/TimesheetService";
import {StatusType} from "../../interfaces/StatusType";
import StatusFilter from "../../components/status/StatusFilter";


const DocumentPage: React.FC = () => {
    const [filter, setFilter] = useState<StatusType | null>(null);
    const [timesheets, setTimesheets] = useState<Timesheet[]>([]);
    const { user } = useAuth();

     useEffect(() => {
    if (user && user.username) {
      getTimesheets(user.username)
        .then(sheets => {
          setTimesheets(sheets);
          console.log('Loaded timesheets:', sheets);
        })
        .catch(error => {
          console.error('Failed to load timesheets:', error);
          setTimesheets([]);
        });
    }
  }, [user]);

    return (
        <div className="px-6 py-6">
            <div className="flex flex-row gap-8 items-center">
                <div className="flex flex-row gap-4">
                    <p className="text-lg font-semibold text-subtitle">This Year,</p>
                    <YearTimespan year={2024}/>
                </div>
            </div>

            <h1 className="text-3xl font-bold text-headline mt-4">Your monthly documents</h1>
            <StatusFilter setFilter={setFilter}/>

            <div className="flex flex-row mt-8 gap-12">
        
                <img src={VerticalTimeLine} alt="Vertical Time Line"/>

                <div className="flex flex-col w-full h-full justify-between">
                    <p className="mb-3 text-sm font-semibold text-[#434343]">Today</p>
                    <TimesheetListView sheets={timesheets} />
                    <div className="flex mt-8 flex-col gap-2 items-center">
                        <div className="w-full h-[2.7px] rounded-md bg-[#EFEFEF]"/>
                        <div className="flex flex-row ml-12">
                            <div className="w-24"/>
                            <div className="flex mr-20 text-sm font-semibold text-[#B5B5B5]">
                                <p>Work</p>
                                <div className="w-20"/>
                                <p>Vacation days</p>
                                <div className="w-16"/>
                                <p>Overtime</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default DocumentPage;













