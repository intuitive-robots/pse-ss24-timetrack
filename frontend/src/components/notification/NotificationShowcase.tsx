import React, { useState } from 'react';
import { NotificationIconActive } from "../../assets/iconComponents/NotificationIconActive";
import HorizontalSeparator from "../../shared/HorizontalSeparator";
import NotificationsList from "./NotificationList";

export const NotificationShowcase = () => {
    const [isOpen, setIsOpen] = useState(false);

    const toggleOverlay = () => {
        setIsOpen(!isOpen);
    };

    return (
        <div className="relative">
            <button
                onClick={toggleOverlay}
                className="p-0 border-none bg-transparent cursor-pointer flex items-center justify-center"
            >
                <NotificationIconActive />
            </button>
            {isOpen && (
                <div className={`absolute right-[-0.5rem] top-11 mt-2 w-96 min-h-52 rounded-xl bg-white border-[#EBEBEB] border-[1px] shadow-profile-popup-shadow py-4 transform transition-opacity duration-200 ease-out ${isOpen ? 'scale-100 opacity-100' : 'scale-95 opacity-0 hidden'} origin-top`}>
                    <div>
                        <div className="flex flex-row justify-between items-end mb-4 px-4">
                            <h1 className="text-md font-semibold text-black">Notifications</h1>
                            <p className="text-xs font-medium underline text-[#3A3A3A] hover:cursor-pointer">Mark all as
                                read</p>
                        </div>
                        <HorizontalSeparator/>
                    </div>
                    <NotificationsList/>
                </div>
            )}
        </div>
    );
}
