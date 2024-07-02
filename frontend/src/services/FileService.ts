import axiosInstance from "./AxiosInstance";

interface UploadFileResponse {
  message: string;
  status: string;
}

export interface FileData {
  url: string;
  name: string;
}

const fileURL = '/user';

/**
 * Lädt eine Datei zum Server hoch.
 * @param file Die Datei, die hochgeladen werden soll.
 * @param fileType Der Typ der Datei, der als Teil der Anfrage gesendet wird.
 * @returns Eine Promise mit der Antwort vom Server.
 */
async function uploadFile(file: File, fileType: string = "Signature"): Promise<UploadFileResponse> {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('fileType', fileType);

  try {
    const response = await axiosInstance.post(`${fileURL}/uploadFile`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    return response.data;
  } catch (error: any) {
    console.error('Error uploading file:', error.response?.data || error.message);
    throw new Error(error.response?.data || "An error occurred during file upload.");
  }
}

const getUserFile = async (username: string, fileType: string): Promise<string | null> => {
  try {
    const response = await axiosInstance.get(`${fileURL}/getFile`, {
      params: { username, fileType },
      responseType: 'blob'
    });

    if (response.status === 200 && response.data) {
      return window.URL.createObjectURL(new Blob([response.data]));
    }
    return null;
  } catch (error) {
    console.error('Error fetching file:', error);
    return null;
  }
}

export {
  uploadFile,
  getUserFile
};
