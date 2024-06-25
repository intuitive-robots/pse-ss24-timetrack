import React, {useEffect, useState} from 'react';
import LayoutWrapper from "../../components/LayoutWrapper";
import {useAuth} from "../../context/AuthContext";
import {getCurrentTimesheet} from "../../services/TimesheetService";
import ListIconCardButton from "../../components/navbar/ListIconCardButton";
import LeftNavbarIcon from "../../assets/images/nav_button_left.svg"
import RightNavbarIcon from "../../assets/images/nav_button_right.svg"
import VerticalTimeLine from "../../assets/images/time_line_vertical.svg"
import TimeEntryTile from "../../components/TimeEntryTile";
import SignSheetIcon from "../../assets/images/sign_icon.svg";
import QuickActionButton from "../../components/input/QuickActionButton";
import MonthTimespan from "../../components/MonthTimespan";

/**
 * HiwiHomePage component serves as the main landing page for the application.
 *
 * @returns {React.ReactElement} A React Element that renders the main homepage of the application.
 */
const HiwiHomePage = (): React.ReactElement => {
    const [timesheet, setTimesheet] = useState(null);
    const { user } = useAuth();

    useEffect(() => {
        console.log(user)
        if (user && user.username) {
            getCurrentTimesheet(user.username)
                .then(setTimesheet)
                .catch(error => console.error('Failed to fetch timesheet:', error));
        }
    }, [user]);

    const entries = [
        { entryName: "Entwicklung des Backends", projectName: "Project Alpha", workTime: "4,5h", breakTime: "15m", period: "11:00 - 15:45", date: "2022-05-01T12:20:30.656+00:00" },
        { entryName: "Frontend Überarbeitung", projectName: "Project Beta", workTime: "3,5h", breakTime: "10m", period: "09:00 - 12:30", date: "2022-05-02T12:20:30.656+00:00" },
        { entryName: "Datenbank Optimierung", projectName: "Project Gamma", workTime: "5h", breakTime: "20m", period: "10:00 - 15:00", date: "2022-05-03T12:20:30.656+00:00" },
        { entryName: "API Entwicklung", projectName: "Project Delta", workTime: "6h", breakTime: "30m", period: "08:00 - 14:30", date: "2022-05-04T12:20:30.656+00:00" },
        { entryName: "Performance Tests", projectName: "Project Epsilon", workTime: "7h", breakTime: "45m", period: "07:30 - 15:15", date: "2022-05-05T12:20:30.656+00:00" },
        { entryName: "UI/UX Design", projectName: "Project Zeta", workTime: "4h", breakTime: "15m", period: "13:00 - 17:00", date: "2022-05-06T12:20:30.656+00:00" },
        { entryName: "System Integration", projectName: "Project Eta", workTime: "3,5h", breakTime: "10m", period: "12:00 - 15:30", date: "2022-05-07T12:20:30.656+00:00" },
        { entryName: "Dokumentation Erstellung", projectName: "Project Theta", workTime: "2h", breakTime: "5m", period: "10:00 - 12:00", date: "2022-05-08T12:20:30.656+00:00" }
    ];

    return (
        <LayoutWrapper
            pageContent={
                <div className="px-6 py-6">

                    <div className="flex flex-row gap-8 items-center">
                        <div className="flex flex-row gap-4">
                            <p className="text-lg font-semibold text-subtitle">This Month,</p>
                            <MonthTimespan month={4} year={2024}/>
                        </div>
                        <div className="flex gap-4">
                            <ListIconCardButton
                                iconSrc={LeftNavbarIcon}
                                label={"Before"}
                                onClick={() => {}}
                            />
                            <ListIconCardButton
                                iconSrc={RightNavbarIcon}
                                label={"Next"}
                                orientation={"right"}
                                onClick={() => {}}
                            />
                        </div>
                    </div>

                    <h1 className="text-3xl font-bold text-headline mt-4">Hello Nico,</h1>

                    <div className="flex mt-6 gap-12">
                        <img src={VerticalTimeLine} alt="Vertical Time Line"/>

                        <div className="flex flex-col w-full h-full justify-between">
                            <p className="mb-3 text-sm font-semibold text-[#434343]">Today</p>
                            <div className="overflow-y-auto max-h-[28rem]">
                                 {entries.map((entry, index) => (
                                     <TimeEntryTile
                                        key={index}
                                        entryName={entry.entryName}
                                        projectName={entry.projectName}
                                        workTime={entry.workTime}
                                        breakTime={entry.breakTime}
                                        period={entry.period}
                                        date={entry.date.replace(/-..T/, `-${index + 1 < 10 ? '0' : ''}${index + 1}T`)}
                                        onDelete={() => {}}
                                        onEdit={() => {}}
                                    />
                                ))}

                            </div>

                            <div className="flex mt-8 flex-col gap-2 items-center">
                                <div className="w-full h-[2.7px] rounded-md bg-[#EFEFEF]"/>
                                <div className="flex ml-8 text-sm font-semibold text-[#B5B5B5] gap-10">
                                    <p>Work</p>
                                    <p>Breaks</p>
                                    <p>Period</p>
                                </div>
                            </div>

                        </div>


                    </div>


                    <div className="flex">
                        <QuickActionButton
                            icon={SignSheetIcon}
                            label="Sign Sheet"
                            onClick={() => {

                            }}
                            bgColor="bg-purple-600"
                        hover="hover:bg-purple-700"
                    />
                    </div>


                </div>
            }
        />
    );
};

export default HiwiHomePage;
