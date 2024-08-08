import React from 'react';
import {SubmissionReminderIcon} from "../../assets/iconComponents/SubmissionReminderIcon";
import {NotificationMessage} from "../../interfaces/Message";
import {RemoveIcon} from "../../assets/iconComponents/RemoveIcon";

interface NotificationItemProps {
  notification: NotificationMessage;
  onRemove: () => void;
}

const NotificationItem: React.FC<NotificationItemProps> = ({ notification, onRemove }) => {


    return (
        <div className="flex flex-row items-center gap-4 bg-white rounded-lg px-4 py-3">
            <div className="flex h-10 w-12 rounded-md border-border-gray border-1.7 items-center justify-center">
                <SubmissionReminderIcon/>
            </div>
            {/*<p className="text-wrap text-sm font-medium text-[#ABABAB]">*/}
            {/*    <span className="font-semibold text-[#2E2E2E]">{notification.sender} </span>*/}
            {/*    requests change: {notification.message}*/}
            {/*</p>*/}
            <p className="text-wrap text-sm font-medium text-[#ABABAB]">
                {notification.message}
            </p>
            <div className="pr-1 cursor-pointer text-[#ABABAB] hover:text-gray-500"
                onClick={onRemove}
            >
                <RemoveIcon className="w-3"/>
            </div>
        </div>
    );
};

export default NotificationItem;
