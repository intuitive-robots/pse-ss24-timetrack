import React, { createContext, useState, useContext, ReactNode, FC } from 'react';

interface SearchContextType {
  searchString: string;
  setSearchString: (search: string) => void;
  searchEnabled: boolean;
  setSearchEnabled: (enabled: boolean) => void;
}

const SearchContext = createContext<SearchContextType | undefined>(undefined);

interface SearchProviderProps {
  children: ReactNode;
}


export const SearchProvider: FC<SearchProviderProps> = ({ children }) => {
  const [searchString, setSearchString] = useState<string>('');
  const [searchEnabled, setSearchEnabled] = useState<boolean>(true);

  const value = { searchString, setSearchString, searchEnabled, setSearchEnabled };

  return (
    <SearchContext.Provider value={value}>
      {children}
    </SearchContext.Provider>
  );
};


export const useSearch = (): SearchContextType => {
  const context = useContext(SearchContext);
  if (context === undefined) {
    throw new Error('useSearch must be used within a SearchProvider');
  }
  return context;
};
