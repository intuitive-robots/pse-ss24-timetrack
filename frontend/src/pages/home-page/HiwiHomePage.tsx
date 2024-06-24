import React, {useEffect, useState} from 'react';
import LayoutWrapper from "../../components/LayoutWrapper";
import {useAuth} from "../../context/AuthContext";
import {getCurrentTimesheet} from "../../services/TimesheetService";
import ListIconCardButton from "../../components/navbar/ListIconCardButton";
import LeftNavbarIcon from "../../assets/images/nav_button_left.svg"
import RightNavbarIcon from "../../assets/images/nav_button_right.svg"
import VerticalTimeLine from "../../assets/images/time_line_vertical.svg"
import TimeEntryTile from "../../components/TimeEntryTile";

/**
 * HiwiHomePage component serves as the main landing page for the application.
 *
 * @returns {React.ReactElement} A React Element that renders the main homepage of the application.
 */
const HiwiHomePage = (): React.ReactElement => {
    const [timesheet, setTimesheet] = useState(null);
    const { user } = useAuth();

    useEffect(() => {
        if (user && user.username) {
            getCurrentTimesheet(user.username)
                .then(setTimesheet)
                .catch(error => console.error('Failed to fetch timesheet:', error));
        }
    }, [user]);

    return (
        <LayoutWrapper
            pageContent={
                <div className="px-6 py-6">

                    <div className="flex flex-row gap-8 items-center">
                        <div className="flex flex-row gap-4">
                            <p className="text-lg font-semibold text-subtitle">This Month,</p>
                            <p className="text-lg font-semibold text-nav-gray">April 30, 2024 - May 31, 2024</p>
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

                    <h1 className="text-3xl font-bold text-gray-800 mt-5">Hello Nico,</h1>

                    <div className="flex mt-6 gap-12">
                        <img src={VerticalTimeLine} alt="Vertical Time Line"/>

                        <div className="w-full">
                            <p className="mb-3 text-sm font-semibold text-[#434343]">Today</p>
                            <TimeEntryTile  entryName={"Entwicklung des Backends"} projectName={"Project Alpha"} workTime={"4,5h"} breakTime={"15m"} period="11:00 - 15:45" date={""}  onDelete={() => {}} onEdit={() => {}}  />
                        </div>
                    </div>

                </div>
            }
        />
    );
};

export default HiwiHomePage;
