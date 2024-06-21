import React from 'react';
import LayoutWrapper from "../../components/LayoutWrapper";

/**
 * HiwiHomePage component serves as the main landing page for the application.
 *
 * @returns {React.ReactElement} A React Element that renders the main homepage of the application.
 */
const HiwiHomePage = (): React.ReactElement => {

    return (
        <LayoutWrapper
            pageContent={
                <div className="px-6 py-6">
                    <p className="text-lg font-medium text-subtitle">Institute for Intuitive Robotics</p>
                    <h1 className="text-3xl font-bold text-gray-800 mt-5">Hello Nico,</h1>
                    <h2 className="text-md font-medium text-subtitle mt-1">You are an HiWi</h2>
                    <div className="h-5"/>
                </div>
            }
        />
    );
};

export default HiwiHomePage;
