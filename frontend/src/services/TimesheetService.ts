import axiosInstance from "./AxiosInstance";
import {Timesheet} from "../interfaces/Timesheet";
import axios from "axios";
import {handleAxiosError} from "../utils/AxiosUtils";

/**
 * Signs the current timesheet for the user.
 * @returns The response data from the timesheet sign request.
 * @throws An error if the request fails.
 */
const signTimesheet = async (timesheetId: string) => {
  try {
    const response = await axiosInstance.patch('/timesheet/sign',
        {"_id": timesheetId });
    return response.data;
  } catch (error) {
    console.error('Signing timesheet failed', error);
    handleAxiosError(error);
  }
};

/**
 * Approves the specified timesheet.
 * @returns The response data from the timesheet approve request.
 * @throws An error if the request fails.
 */
const approveTimesheet = async (timesheetId: string) => {
  try {
    const response = await axiosInstance.patch('/timesheet/approve', {"_id": timesheetId});
    return response.data;
  } catch (error) {
    console.error('Approving timesheet failed');
    handleAxiosError(error);
  }
};

/**
 * Requests a change to the current timesheet.
 * @param timesheetId - The ID of the timesheet for which a change is requested.
 * @param description - A message describing the requested change.
 * @returns The response data from the timesheet change request.
 * @throws An error if the request fails.
 */
const requestChange = async (timesheetId: string, description: string) => {
  try {
    const response = await axiosInstance.patch('/timesheet/requestChange', {
      "_id": timesheetId,
      "message": description
    });
    return response.data;
  } catch (error) {
    console.error('Requesting timesheet change failed');
    handleAxiosError(error);
  }
};

/**
 * Retrieves an array of timesheets for a specific user or an empty array if none are found.
 * @param username The username for which to retrieve timesheets.
 * @returns A Promise that resolves to an array of Timesheet objects.
 */
const getTimesheets = async (username: string): Promise<Timesheet[]> => {
  try {
    const response = await axiosInstance.get('/timesheet/get', {
      params: { username }
    });
    if (response.data && Array.isArray(response.data)) {
      return response.data as Timesheet[];
    } else {
      return [];
    }
  } catch (error) {
    console.error('Fetching timesheets failed', error);
    handleAxiosError(error);
    return [];
  }
};

/**
 * Fetches the timesheet for the specified user, month, and year.
 * @param username The username of the user whose timesheet is being requested.
 * @param month The month of the timesheet.
 * @param year The year of the timesheet.
 * @returns A Promise that resolves to a Timesheet object or null if not found.
 */
const getTimesheetByMonthYear = async (username: string, month: number, year: number): Promise<Timesheet | null> => {
  try {
    const response = await axiosInstance.get('/timesheet/getByMonthYear', {
      params: {
        username: username,
        month: month,
        year: year
      }
    });
    if (response.status === 404) {
      return null;
    }
    return response.data ? (response.data as Timesheet) : null;
  } catch (error) {
    handleAxiosError(error);
    return null;
  }
};

/**
 * Fetches the timesheet by username and status.
 * @returns The timesheet for the specified username and status.
 * @throws An error if the retrieval fails.
 */
const getTimesheetByUsernameStatus = async (username: string, status: string) => {
  try {
    const response = await axiosInstance.get('/timesheet/getTimesheetByUsernameStatus', { params: { username, status } });
    return response.data;
  } catch (error) {
    console.error('Fetching timesheet by username and status failed');
    throw error;
  }
};

/**
 * Fetches the current timesheet for the user.
 * @returns The current timesheet data.
 * @throws An error if the retrieval fails.
 */
const getCurrentTimesheet = async (username: string) => {
  try {
    console.log(`Fetching current Timesheet of ${username}`);
    const response = await axiosInstance.get('/timesheet/getCurrentTimesheet', {
        params: { username: username }
    });
    return response.data;
  } catch (error) {
    console.error('Fetching current timesheet failed', error);
    throw error;
  }
};

/**
 * Fetches the highest priority timesheet for a user.
 * @param username The username of the user whose highest priority timesheet is being requested.
 * @returns A Promise that resolves to a Timesheet object or null if not found.
 */
const getHighestPriorityTimesheet = async (username: string): Promise<Timesheet | null> => {
  try {
    const response = await axiosInstance.get('/timesheet/getHighestPriorityTimesheet', {
      params: { username }
    });
    return response.data ? (response.data as Timesheet) : null;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response && error.response.status === 404) {
      console.log('No priority timesheet found for the given username', username);
    } else {
      handleAxiosError(error);
    }
    return null;
  }
};

export {
  signTimesheet,
  approveTimesheet,
  requestChange,
  getTimesheets,
  getTimesheetByMonthYear,
  getTimesheetByUsernameStatus,
  getCurrentTimesheet,
    getHighestPriorityTimesheet
};
