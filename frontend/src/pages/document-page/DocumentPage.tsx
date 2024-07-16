import React, {useEffect, useState} from "react";
import VerticalTimeLine from "../../assets/images/time_line_vertical.svg";
import YearTimespan from "../../components/timesheet/YearTimespan";
import TimesheetListView from "../../components/timesheet/TimesheetListView";
import {Timesheet} from "../../interfaces/Timesheet";
import {useAuth} from "../../context/AuthContext";
import {getTimesheets} from "../../services/TimesheetService";
import {StatusType} from "../../interfaces/StatusType";
import StatusFilter from "../../components/status/StatusFilter";
import {isValidTimesheetStatus, statusMapping} from "../../components/status/StatusMapping";
import {Roles} from "../../components/auth/roles";


const DocumentPage: React.FC = () => {
    const [filter, setFilter] = useState<StatusType | null>(null);
    const [timesheets, setTimesheets] = useState<Timesheet[]>([]);
    const { user } = useAuth();

     useEffect(() => {
    if (user && user.username) {
      getTimesheets(user.username)
        .then(sheets => {
          const validTimesheets = sheets
                .filter((timesheet): timesheet is Timesheet => timesheet !== null)
                    .map(timesheet => {
                        if (!isValidTimesheetStatus(timesheet.status)) {
                            return {
                              ...timesheet,
                                status: StatusType.Error,
                            } as Timesheet;
                        }
                        return {
                            ...timesheet,
                            status: statusMapping[Roles.Hiwi][timesheet.status],
                        } as Timesheet;
                      });
                setTimesheets(validTimesheets);
        }).catch(error => {
          console.error('Failed to load timesheets:', error);
          setTimesheets([]);
        });
    }
  }, [user]);

     console.log("status: " + filter);
  const filteredTimesheets = timesheets
    ? (filter ? timesheets.filter(timesheet => timesheet && timesheet.status === filter) : timesheets)
    : [];

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

                <div className="relative flex flex-col w-full h-full justify-between">
                    <p className="mb-3 text-sm font-semibold text-[#434343]">Today</p>
                    <TimesheetListView sheets={filteredTimesheets}/>
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
                    <div className="absolute bottom-10 left-0 right-0 h-20 complex-gradient pointer-events-none"></div>
                </div>

            </div>
        </div>
    );
};

export default DocumentPage;













