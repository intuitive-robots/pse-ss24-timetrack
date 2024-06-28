import React from 'react';

interface ListTileInfoProps {
  items: string[];
}

const ListTileInfo: React.FC<ListTileInfoProps> = ({ items }) => {
  return (
    <div className="flex flex-row gap-12">
      {items.map((item, index) => (
        <p key={index} className="text-md font-semibold text-[#3B3B3B]">{item}</p>
      ))}
    </div>
  );
};

export default ListTileInfo;
