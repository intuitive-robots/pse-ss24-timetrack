import React, {useEffect, useState} from 'react';
import StatusFilter from "../../components/status/StatusFilter";
import {StatusType} from "../../interfaces/StatusType";
import {Timesheet} from "../../interfaces/Timesheet";
import {User} from "../../interfaces/User";
import {getTimesheetByMonthYear} from "../../services/TimesheetService";
import {getSupervisor, getUsersByRole} from "../../services/UserService";
import ListIconCardButton from "../../components/input/ListIconCardButton";
import LeftNavbarIcon from "../../assets/images/nav_button_left.svg"
import RightNavbarIcon from "../../assets/images/nav_button_right.svg"
import {isValidTimesheetStatus, statusMapping, TimesheetStatus} from "../../components/status/StatusMapping";
import {Roles} from "../../components/auth/roles";
import VerticalTimeLine from "../../assets/images/time_line_vertical.svg";
import MonthTimespan from "../../components/timesheet/MonthTimespan";
import SecretaryDocumentListView from "../../components/timesheet/SecretaryDocumentListView";
import QuickActionButton from "../../components/input/QuickActionButton";
import DownloadIcon from "../../assets/images/download_icon_white.svg";


const SecretaryDocumentPage: React.FC = () => {

    const [filter, setFilter] = useState<StatusType | null>(null);
    const [hiwis, setHiwis] = useState<User[]>([]);
    const [supervisors, setSupervisors] = useState<any[]>([]);
    const [timesheets, setTimesheets] = useState<Timesheet[]>([]);

    const [month, setMonth] = useState(new Date().getMonth() + 1);
    const [year, setYear] = useState(new Date().getFullYear());

    const currentMonth = new Date().getMonth() + 1;
    const currentYear = new Date().getFullYear();

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
      const storedMonth = localStorage.getItem('selectedMonth');
      const storedYear = localStorage.getItem('selectedYear');
      const newMonth = storedMonth ? parseInt(storedMonth) : new Date().getMonth() + 1;
      const newYear = storedYear ? parseInt(storedYear) : new Date().getFullYear();

      setMonth(newMonth);
      setYear(newYear);
    }, [month, year]);

    useEffect(() => {
        getUsersByRole(Roles.Hiwi)
            .then(fetchedHiwis => {
                setHiwis(fetchedHiwis);
            })
            .catch(error => console.error('Failed to fetch hiwis for supervisor:', error));
    }, []);

    useEffect(() => {
         if (hiwis && hiwis.length > 0) {
             hiwis.map(hiwi => {
                 getSupervisor(hiwi.username)
                     .then(fetchedSupervisor => {
                         setSupervisors(prevSupervisors => [...prevSupervisors, fetchedSupervisor]);
                     })
                     .catch(error => console.error(`Failed to fetch supervisor for ${hiwi.username}: `, error));
             })
         }
    }, [hiwis]);
    //console.log("supervisors: " + supervisors.map(s => s.lastName));
    useEffect(() => {
        if (hiwis && hiwis.length > 0) {
            Promise.all(hiwis.map(async (hiwi) => {
                try {
                    const timesheet = await getTimesheetByMonthYear(hiwi.username, month, year);
                    return timesheet || defaultTimesheet(hiwi._id, hiwi.username, month, year);
                } catch (error) {
                    console.error(`Failed to fetch timesheet for ${hiwi.username}: `, error);
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
                            status: statusMapping[Roles.Secretary][timesheet.status],
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
        let newMonth = month;
        let newYear = year;

        if (direction === 'next') {
            if (month === 12) {
                newMonth = 1;
                newYear = year + 1;
            } else {
                newMonth = month + 1;
            }
        } else if (direction === 'prev') {
            if (month === 1) {
                newMonth = 12;
                newYear = year - 1;
            } else {
                newMonth = month - 1;
            }
        }
        localStorage.setItem('selectedMonth', newMonth.toString());
        localStorage.setItem('selectedYear', newYear.toString());

        setMonth(newMonth);
        setYear(newYear);
    };

    const handleDownloadAll = () => {
        for (const sheet in filteredTimesheets.filter(sheet => sheet.status === StatusType.Complete && sheet.username != null)) {

        }

    };

    console.log('All timesheets:', filteredTimesheets);
    return (
        <div className="px-6 py-6">
            <div className="flex flex-row gap-8 items-center">
                <div className="flex flex-row gap-4">
                    <p className="text-lg font-semibold text-subtitle">This Month,</p>
                    <MonthTimespan year={year} month={month}/>
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

            <h1 className="text-3xl font-bold text-headline mt-4">All monthly Documents</h1>

            <h2 className="text-md font-medium text-subtitle mt-1">There are 3 documents ready to download</h2>


            <div className="h-5"/>
            <StatusFilter setFilter={setFilter}/>

            <div className="flex flex-row mt-8 gap-12">

                <img src={VerticalTimeLine} alt="Vertical Time Line"/>

                <div className="flex flex-col w-full h-full justify-between">
                    <p className="mb-3 text-sm font-semibold text-[#434343]">Today</p>
                    <SecretaryDocumentListView sheets={filteredTimesheets} hiwis={hiwis} supervisors={supervisors}/>
                    <div className="flex mt-8 flex-col gap-2 items-center">
                        <div className="w-full h-[2.7px] rounded-md bg-[#EFEFEF]"/>
                        <div className="flex flex-row ml-9">
                            <div className="w-40"/>
                            <div className="flex mr-20 text-sm font-semibold text-[#B5B5B5]">
                                <p>Work</p>
                                <div className="w-12"/>
                                <p>Vacation days</p>
                                <div className="w-12"/>
                                <p>Overtime</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div className="w-fit ml-auto absolute right-14 bottom-10">
                <QuickActionButton
                icon={DownloadIcon}
                label="Download All"
                onClick={() => console.log("Download all")}/>
            </div>

        </div>
    );
};

export default SecretaryDocumentPage;











