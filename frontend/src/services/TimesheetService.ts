import axiosInstance from "./AxiosInstance";

/**
 * Signs the current timesheet for the user.
 * @returns The response data from the timesheet sign request.
 * @throws An error if the request fails.
 */
const signTimesheet = async () => {
  try {
    const response = await axiosInstance.post('/timesheet/signTimesheet');
    return response.data;
  } catch (error) {
    console.error('Signing timesheet failed');
    throw error;
  }
};

/**
 * Approves the specified timesheet.
 * @returns The response data from the timesheet approve request.
 * @throws An error if the request fails.
 */
const approveTimesheet = async () => {
  try {
    const response = await axiosInstance.post('/timesheet/approveTimesheet');
    return response.data;
  } catch (error) {
    console.error('Approving timesheet failed');
    throw error;
  }
};

/**
 * Requests a change to the current timesheet.
 * @returns The response data from the timesheet change request.
 * @throws An error if the request fails.
 */
const requestChange = async () => {
  try {
    const response = await axiosInstance.post('/timesheet/requestChange');
    return response.data;
  } catch (error) {
    console.error('Requesting timesheet change failed');
    throw error;
  }
};

/**
 * Retrieves all timesheets.
 * @returns The list of all timesheets.
 * @throws An error if the retrieval fails.
 */
const getTimesheets = async () => {
  try {
    const response = await axiosInstance.get('/timesheet/getTimesheets');
    return response.data;
  } catch (error) {
    console.error('Fetching timesheets failed');
    throw error;
  }
};

/**
 * Fetches the timesheet by month and year.
 * @returns The timesheet for the specified month and year.
 * @throws An error if the retrieval fails.
 */
const getTimesheetByMonthYear = async (month: number, year: number) => {
  try {
    const response = await axiosInstance.get('/timesheet/getTimesheetByMonthYear', { params: { month, year } });
    return response.data;
  } catch (error) {
    console.error('Fetching timesheet by month and year failed');
    throw error;
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
        data: { username: username }
    });
    return response.data;
  } catch (error) {
    console.error('Fetching current timesheet failed', error);
    throw error;
  }
};

export { signTimesheet, approveTimesheet, requestChange, getTimesheets, getTimesheetByMonthYear, getTimesheetByUsernameStatus, getCurrentTimesheet };
