import React, {useEffect, useState} from 'react';
import StatusFilter from "../../components/status/StatusFilter";
import {StatusType} from "../../interfaces/StatusType";
import {Timesheet} from "../../interfaces/Timesheet";
import {User} from "../../interfaces/User";
import {getTimesheetByMonthYear} from "../../services/TimesheetService";
import {useAuth} from "../../context/AuthContext";
import {getUsersByRole} from "../../services/UserService";
import ListIconCardButton from "../../components/input/ListIconCardButton";
import LeftNavbarIcon from "../../assets/images/nav_button_left.svg"
import RightNavbarIcon from "../../assets/images/nav_button_right.svg"
import {isValidTimesheetStatus, statusMapping, TimesheetStatus} from "../../components/status/StatusMapping";
import {getRole, isValidRole, Roles} from "../../components/auth/roles";
import {useNavigate} from "react-router-dom";
import VerticalTimeLine from "../../assets/images/time_line_vertical.svg";
import TimesheetListView from "../../components/timesheet/TimesheetListView";
import MonthTimespan from "../../components/timesheet/MonthTimespan";


const SecretaryDocumentPage: React.FC = () => {

    const [filter, setFilter] = useState<StatusType | null>(null);
    const [hiwis, setHiwis] = useState<User[] | null>(null);
    const [timesheets, setTimesheets] = useState<Timesheet[]>([]);
    const { user, role } = useAuth();

    const [month, setMonth] = useState(new Date().getMonth() + 1);
    const [year, setYear] = useState(new Date().getFullYear());

    const currentMonth = new Date().getMonth() + 1;
    const currentYear = new Date().getFullYear();

    const navigate = useNavigate();
    const defaultTimesheet = (
        id: string,
        username: string,
        month: number,
        year: number
    ): Timesheet => {
        return {
            _id: id,
            username: username,
            month: month,
            year: year,
            status: statusMapping[Roles.Secretary][TimesheetStatus.NoTimesheet],
            totalTime: 0,
            overtime: 0,
            lastSignatureChange: new Date().toISOString(),
            projectName: 'default project',
      };
    };

    useEffect(() => {
        getUsersByRole(Roles.Hiwi)
            .then(fetchedHiwis => {
                setHiwis(fetchedHiwis);
            })
            .catch(error => console.error('Failed to fetch hiwis for supervisor:', error));
    }, []);


    useEffect(() => {
        if (hiwis && hiwis.length > 0) {
            Promise.all(hiwis.map(async (hiwi) => {
                try {
                    const timesheet = await getTimesheetByMonthYear(hiwi.username, month, year);
                    return timesheet || defaultTimesheet(hiwi._id, hiwi.username, month, year);
                } catch (error) {
                    console.error(`Failed to fetch timesheet for ${hiwi.username}:`, error);
                    return null;
                }
            })).then(fetchedTimesheets => {
                const validTimesheets = fetchedTimesheets
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
                            status: statusMapping[Roles.Secretary][timesheet.status]
                        } as Timesheet;
                      });
                setTimesheets(validTimesheets);
                console.debug("timesheets set: " + fetchedTimesheets.map(timesheet => console.debug(timesheet))); // TODO Debug
            }).catch(error => {
                console.error('Failed to load timesheets:', error);
                setTimesheets([]);
            });
        }
    }, [hiwis, month, year]);

  const filteredTimesheets = timesheets
        ? (filter ? timesheets.filter(timesheet => timesheet && timesheet.status === filter) : timesheets)
        : [];


    // TODO: duplicate code with HiwiHomepage.tsx
    const handleMonthChange = (direction: string) => {
        if (direction === 'next') {
            if (month === 12) {
                setMonth(1);
                setYear(prevYear => prevYear + 1);
            } else {
                setMonth(prevMonth => prevMonth + 1);
            }
        } else if (direction === 'prev') {
            if (month === 1) {
                setMonth(12);
                setYear(prevYear => prevYear - 1);
            } else {
                setMonth(prevMonth => prevMonth - 1);
            }
        }
    };

    const handleDownloadTimesheet = (hiwi: User, month: number, year: number) => {
        // console.log("check timesheet");
        // console.log("Params on call:", { month, year });

        let monthString = month.toString();
        let yearString = year.toString();


        //const path = `/app/timesheet/${hiwi.username.replace(/\s+/g, '-')}/${month}/${year}`;
        //navigate(path);

    };

    console.log('All timesheets:', filteredTimesheets);
    return (
        <div className="px-6 py-6">
            <div className="flex flex-row gap-8 items-center">
                <div className="flex flex-row gap-4">
                    <p className="text-lg font-semibold text-subtitle">This Month,</p>
                    <MonthTimespan year={year} month={month} />
                </div>
                <div className="flex gap-4">
                    <ListIconCardButton
                        iconSrc={LeftNavbarIcon}
                        label={"Before"}
                        onClick={() => handleMonthChange('prev')}
                    />
                    <ListIconCardButton
                        iconSrc={RightNavbarIcon}
                        label={"Next"}
                        orientation={"right"}
                        onClick={() => handleMonthChange('next')}
                        disabled={month === currentMonth && year === currentYear}
                    />
                </div>
            </div>

            <h1 className="text-3xl font-bold text-gray-800 mt-5">All monthly Documents</h1>

            <h2 className="text-md font-medium text-subtitle mt-1">There are X documents ready to download</h2>


            <div className="h-5"/>
            <div className="px-4">
                <StatusFilter setFilter={setFilter}/>
                {hiwis ? (
                    <div className="flex flex-row mt-8 gap-12">

                        <img src={VerticalTimeLine} alt="Vertical Time Line"/>

                        <div className="flex flex-col w-full h-full justify-between">
                            <p className="mb-3 text-sm font-semibold text-[#434343]">Today</p>
                            <TimesheetListView sheets={filteredTimesheets} />
                            <div className="flex mt-8 flex-col gap-2 items-center">
                                <div className="w-full h-[2.7px] rounded-md bg-[#EFEFEF]"/>
                                <div className="flex ml-8 text-sm font-semibold text-[#B5B5B5] gap-10">
                                    <p>Work</p>
                                    <p>Vacation days</p>
                                    <p>Overtime</p>
                                    <p>Status</p>
                                </div>
                            </div>
                        </div>
                    </div>
                ) : (
                    <div className="p-4 bg-red-100 text-red-700 rounded shadow">
                        Keine HiWis gefunden.
                    </div>
                )}
            </div>
        </div>
    );
};

export default SecretaryDocumentPage;











