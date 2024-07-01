import axiosInstance from "./AxiosInstance";

interface UploadFileResponse {
  message: string;
  status: string;
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

export {
  uploadFile,
};
