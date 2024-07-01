import React, {useCallback} from 'react';
import { useDropzone } from 'react-dropzone';
import UploadIcon from "../../assets/images/upload_icon.svg"
import {uploadFile} from "../../services/FileService";

const SignatureUpload = () => {
    const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];

    try {
      const response = await uploadFile(file, 'Signature');
      alert('File uploaded successfully: ' + response.message);
    } catch (error: any) {
      alert('Error uploading file: ' + error.message);
    }
  }, []);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  return (
      <div {...getRootProps()}
           className="py-9 border-dashed border-2 border-gray-400 rounded-lg text-center cursor-pointer">
          <input {...getInputProps()} />
          <div className="flex justify-center items-center mb-2">
              <img src={UploadIcon} alt="Upload Icon"/>
          </div>
          <div className="text-sm text-gray-600">
              {isDragActive ? <p>Drop the files here ...</p> :
                  <>Drag & drop a signature or <button className="text-purple-500 underline">Browse</button></>
              }
          </div>
          <div className="text-xs text-gray-500 mt-2">
              Supported formats: JPEG, PNG, GIF (300x400px)
          </div>
      </div>
  );
}

export default SignatureUpload;
