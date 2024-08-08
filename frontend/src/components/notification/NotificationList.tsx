import React from 'react';
import NotificationItem from './NotificationItem';
import HorizontalSeparator from "../../shared/HorizontalSeparator";
import {NotificationMessage} from "../../interfaces/Message";

interface NotificationsListProps {
    notifications: NotificationMessage[];
    limit?: number;
    onRemove: (id: string) => void;
}

const NotificationsList: React.FC<NotificationsListProps> = ({ notifications, limit, onRemove}) => {
    const limitedNotifications = limit ? notifications.slice(0, limit) : notifications;

    return (
        <div>
            {limitedNotifications.map((notification: NotificationMessage, index) => (
                <div key={index}>
                    <NotificationItem
                        notification={notification}
                        onRemove={() => onRemove(notification._id)}
                    />
                    <HorizontalSeparator/>
                </div>
            ))}
        </div>
    );
};

export default NotificationsList;
