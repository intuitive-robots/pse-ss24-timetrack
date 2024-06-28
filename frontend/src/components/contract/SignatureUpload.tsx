import React from 'react';

import UploadIcon from "../../assets/images/upload_icon.svg"

const SignatureUpload = () => {
  return (
    <div className="py-9 border-dashed border-2 border-gray-400 rounded-lg text-center">
      <div className="flex justify-center items-center mb-2">
        <img src={UploadIcon} alt="Upload Icon" />
      </div>
      <div className="text-sm text-gray-600">
        Drag & drop Signature or <button className="text-purple-500 underline">Browse</button>
      </div>
      <div className="text-xs text-gray-500 mt-2">
        Supported formats: JPEG, PNG, GIF (300x400px)
      </div>
    </div>
  );
}

export default SignatureUpload;
