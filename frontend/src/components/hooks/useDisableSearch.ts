import { useEffect } from 'react';
import {useSearch} from "../../context/SearchContext";

const useDisableSearch = () => {
    const { setSearchEnabled } = useSearch();

    useEffect(() => {
        // Disable search when the component mounts
        setSearchEnabled(false);

        // re-enable search when the component unmounts
        return () => {
            setSearchEnabled(true);
        };
    }, [setSearchEnabled]);
};

export default useDisableSearch;
