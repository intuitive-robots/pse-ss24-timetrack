import React from 'react';
import {SubmissionReminderIcon} from "../../assets/iconComponents/SubmissionReminderIcon";
import {NotificationMessage} from "../../interfaces/Message";
import {RemoveIcon} from "../../assets/iconComponents/RemoveIcon";

interface NotificationItemProps {
  notification: NotificationMessage;
  onRemove: () => void;
}

const NotificationItem: React.FC<NotificationItemProps> = ({ notification, onRemove }) => {

    function timeAgo(timestamp: string): string {
        const currentTime = new Date();
        const notificationTime = new Date(timestamp);
        const differenceInSeconds = Math.floor((currentTime.getTime() - notificationTime.getTime()) / 1000);

        if (differenceInSeconds < 60) {
            return `${differenceInSeconds}s ago`;
        } else if (differenceInSeconds < 3600) {
            const minutes = Math.floor(differenceInSeconds / 60);
            return `${minutes}min ago`;
        } else if (differenceInSeconds < 86400) {
            const hours = Math.floor(differenceInSeconds / 3600);
            return `${hours}h ago`;
        } else {
            const days = Math.floor(differenceInSeconds / 86400);
            return `${days}d ago`;
        }
    }

    return (
        <div className="flex flex-row w-full items-center gap-4 bg-white rounded-lg px-4 py-3">
            <div className="flex gap-3.5">
                <div
                    className="flex h-10 w-10 min-w-10 rounded-md border-border-gray border-1.7 items-center justify-center">
                    <SubmissionReminderIcon/>
                </div>
                <div className="flex flex-col gap-1">
                    <div className="flex flex-row items-center">
                        <p className="text-wrap text-sm font-medium text-[#ABABAB]">
                            {notification.message}
                        </p>
                        <div className="ml-auto pr-1 cursor-pointer text-[#ABABAB] hover:text-gray-500"
                             onClick={onRemove}
                        >
                            <RemoveIcon className="w-3"/>
                        </div>
                    </div>
                    <p className="text-wrap text-xs font-medium text-[#CDCDCD]">
                        {notification.messageType} • {timeAgo(notification.timestamp)}
                    </p>
                </div>
            </div>


        </div>
    );
};

export default NotificationItem;
