import React, {useEffect, useState} from 'react';
import { getUserFile } from '../../services/FileService';
import UploadIcon from "../../assets/images/upload_icon.svg";


interface SignatureDisplayProps {
  username: string;
  fileType: string;
}

const SignatureDisplay: React.FC<SignatureDisplayProps> = ({ username, fileType }) => {
  const [imageUrl, setImageUrl] = useState<string | null>(null);

  useEffect(() => {
    const fetchImage = async () => {
      const url = await getUserFile(username, fileType);
      setImageUrl(url);
    };

    fetchImage();
  }, [username, fileType]);

  if (!imageUrl) {
    return <div>
      <img src={UploadIcon} alt={"UploadIcon"}/>
    </div>;
  }

  return (
      <div className="border border-border-gray">
        <img src={imageUrl} alt={`${username}'s ${fileType}`} className="w-30 max-h-24"/>
      </div>
  );
};

export default SignatureDisplay;
