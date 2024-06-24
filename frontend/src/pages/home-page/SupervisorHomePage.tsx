import React from 'react';
import LayoutWrapper from "../../components/LayoutWrapper";
import HiwiCard from "../../components/HiwiCard";
import ProfilePlaceholder from "../../assets/images/profile_placeholder.svg"

/**
 * Supervisor Homepage component serves as the main landing page for the application.
 *
 * @returns {React.ReactElement} A React Element that renders the main homepage of the application.
 */
const SupervisorHomePage = (): React.ReactElement => {

    return (
        <LayoutWrapper
            pageContent={
                <div className="px-6 py-6">
                    <p className="text-lg font-medium text-subtitle">Institute for Intuitive Robotics</p>
                    <h1 className="text-3xl font-bold text-gray-800 mt-5">Hello Nico,</h1>
                    <h2 className="text-md font-medium text-subtitle mt-1">You have X assigned employees with Y open timesheets</h2>
                    <div className="h-5"/>
                    <div className="px-4">
                        <div className="flex flex-row gap-6 text-md font-medium px-3 py-2 bg-stone-50 items-center rounded-lg max-w-80">
                            <div className="bg-white rounded-lg shadow-lg px-6 py-1">
                                <p className="text-[#212121]">View all</p>
                            </div>
                            <p className="text-[#606060]">Pending</p>
                            <p className="text-[#606060]">Waiting</p>
                        </div>

                        <div className="flex flex-col py-6">
                            <HiwiCard name={'Nico'} lastName={'Maier'} role={'Hilfswissenschaftler'} profileImageUrl={ProfilePlaceholder} onCheck={() => {}} />
                            <HiwiCard name={'Nico'} lastName={'Maier'} role={'Hilfswissenschaftler'} profileImageUrl={ProfilePlaceholder} onCheck={() => {}} />
                            <HiwiCard name={'Nico'} lastName={'Maier'} role={'Hilfswissenschaftler'} profileImageUrl={ProfilePlaceholder} onCheck={() => {}} />
                        </div>
                    </div>


                </div>
            }
        />
    );
};

export default SupervisorHomePage;
