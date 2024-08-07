import React, {useEffect, useState} from 'react';
import { NotificationIconActive } from "../../assets/iconComponents/NotificationIconActive";
import HorizontalSeparator from "../../shared/HorizontalSeparator";
import NotificationsList from "./NotificationList";
import {NotificationService} from "../../services/NotificationService";
import {NotificationMessage} from "../../interfaces/Message";

export const NotificationShowcase = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [notifications, setNotifications] = useState<NotificationMessage[]>([]);

    useEffect(() => {
        const fetchNotifications = async () => {
            const notificationService = new NotificationService();
            try {
                const fetchedNotifications = await notificationService.readAllNotifications();
                setNotifications(fetchedNotifications);
            } catch (error) {
                console.error('Failed to fetch notifications:', error);
                setNotifications([]);
            }
        };

        fetchNotifications();
    }, [isOpen]);

    const toggleOverlay = () => {
        setIsOpen(!isOpen);
    };

    return (
        <div className="relative">
            <button
                onClick={toggleOverlay}
                className="p-0 border-none bg-transparent cursor-pointer flex items-center justify-center"
            >
                <NotificationIconActive className={`fill-current ${isOpen ? "text-gray-800" : "text-[#424242]"} hover:text-gray-800`}/>
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
                    <NotificationsList notifications={notifications} limit={5}/>
                </div>
            )}
        </div>
    );
}
