import React from 'react';

interface ListTileInfoProps {
  items: string[];
  gap?: string;
}

const ListTileInfo: React.FC<ListTileInfoProps> = ({ items, gap = 'gap-12' }) => {
  return (
    <div id="listTileInformation" className={`listTileInformation flex flex-row ${gap}`}>
      {items.map((item, index) => (
        <p key={index} className="text-md font-semibold text-[#3B3B3B]">{item}</p>
      ))}
    </div>
  );
};

export default ListTileInfo;
