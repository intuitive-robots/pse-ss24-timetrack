import React from 'react';
import SearchIcon from '../../assets/images/search_icon.svg';

interface SearchInputProps {
  placeholder: string;
  onChange?: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

/**
 * SearchInput component that renders a search input field.
 *
 * @component
 * @param {SearchInputProps} props - The props passed to the SearchInput component.
 * @returns {React.ReactElement} A React Element that renders a search input field.
 */
const SearchInput: React.FC<SearchInputProps> = ({ placeholder, onChange }: SearchInputProps): React.ReactElement => {
  return (
      <div className="relative flex items-center">
        <input
            type="text"
            placeholder={placeholder}
            className="input border border-gray-300 py-2 pl-4 pr-12 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
            onChange={onChange}
        />
        <img src={SearchIcon} alt="Search" className="absolute right-5"/>
      </div>
  );
};

export default SearchInput;
