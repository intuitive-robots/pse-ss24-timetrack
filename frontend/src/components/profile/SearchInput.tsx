import React, {useState} from 'react';
import {SearchIcon} from "../../assets/iconComponents/SearchIcon";
import {AiOutlineClose} from "react-icons/ai";
import {useSearch} from "../../context/SearchContext";

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
    const [inputValue, setInputValue] = useState('');

    const {setSearchString} = useSearch();

    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setInputValue(event.target.value);
        setSearchString(event.target.value);
        // onChange(event.target.value);
    };
    const clearInput = () => {
        setInputValue('');
        setSearchString('');
        // onChange('');
    };

  return (
      <div className="relative flex items-center">
        <input
            type="text"
            value={inputValue}
            placeholder={placeholder}
            className="input border border-gray-300 py-2 pl-4 pr-12 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
            onChange={handleInputChange}
        />
        {/*<div className="absolute right-5">*/}
        {/*    <SearchIcon/>*/}
        {/*</div>*/}
          <div className="absolute right-5">
              {inputValue ? (
                <button onClick={clearInput} className="py-2">
                  <AiOutlineClose size={20} className="text-[#717171]" />
                </button>
              ) : (
                <SearchIcon/>
              )}
          </div>
      </div>
  );
};

export default SearchInput;
