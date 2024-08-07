import React from 'react';
import NotificationItem from './NotificationItem';
import HorizontalSeparator from "../../shared/HorizontalSeparator";
import {NotificationMessage} from "../../interfaces/Message";

interface NotificationsListProps {
    notifications: NotificationMessage[];
    limit?: number;
}

const NotificationsList: React.FC<NotificationsListProps> = ({ notifications, limit}) => {
    const limitedNotifications = limit ? notifications.slice(0, limit) : notifications;

    return (
        <div>
            {limitedNotifications.map((notification: NotificationMessage, index) => (
                <div key={index}>
                    <NotificationItem
                        notification={notification}
                    />
                    <HorizontalSeparator/>
                </div>
            ))}
        </div>
    );
};

export default NotificationsList;
