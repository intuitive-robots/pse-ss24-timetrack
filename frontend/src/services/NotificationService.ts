import axiosInstance from './AxiosInstance';
import { handleAxiosError } from '../utils/AxiosUtils';
import {NotificationMessage} from "../interfaces/Message";

export class NotificationService {
    /**
     * Fetches all notifications from the backend and marks them as read.
     *
     * @returns {Promise<NotificationMessage[]>} A promise that resolves to an array of Notification objects.
     */
    public async readAllNotifications(): Promise<NotificationMessage[]> {
        try {
            const response = await axiosInstance.get<NotificationMessage[]>('notification/readAll');
            return response.data;
        } catch (error) {
            console.error('Failed to read all notifications', error);
            handleAxiosError(error);
            throw new Error('Failed to read all notifications');
        }
    }


    /**
     * Checks if there are any unread messages.
     *
     * @returns {Promise<boolean>} A promise that resolves to a boolean indicating if there are unread messages.
     */
    public async doesUnreadMessagesExist(): Promise<boolean> {
        try {
            const response = await axiosInstance.get<boolean>('notification/doesUnreadMessageExist');
            return response.data;
        } catch (error) {
            console.error('Error checking for unread messages', error);
            handleAxiosError(error);
            throw new Error('Failed to check for unread messages');
        }
    }

}
