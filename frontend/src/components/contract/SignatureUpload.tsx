import React, {useCallback} from 'react';
import { useDropzone } from 'react-dropzone';
import UploadIcon from "../../assets/images/upload_icon.svg"
import {uploadFile} from "../../services/FileService";
import {useAuth} from "../../context/AuthContext";
import SignatureDisplay from "./SignatureDisplay";

const SignatureUpload = () => {
    const {user} = useAuth();

    const onDrop = useCallback(async (acceptedFiles: File[]) => {
        const file = acceptedFiles[0];

        try {
          await uploadFile(file, 'Signature');
          window.location.reload();
        } catch (error: any) {
          alert('Error uploading file: ' + error.message);
        }
    }, []);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

    const containerClasses = `py-9 border-dashed border-2 border-[#BFC5EA] rounded-lg text-center cursor-pointer ${
        isDragActive ? 'bg-purple-200' : 'bg-[#F8F8FF]'
    }`;

  return (
      <div {...getRootProps()} className={containerClasses}>
          <input {...getInputProps()} />
          <div className="flex justify-center items-center mb-2">
              {user ? <SignatureDisplay username={user.username} fileType="Signature" /> :
                  <img src={UploadIcon} alt="Upload Icon"/>}
          </div>
          <div className="text-sm text-gray-600">
              {isDragActive ? <p className="text-purple-500">Drop the files here ...</p> :
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
