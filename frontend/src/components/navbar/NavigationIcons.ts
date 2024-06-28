import HomeIcon from '../../assets/images/navbar/home.svg';
import HomeIconActive from '../../assets/images/navbar/home_active.svg';
import DocumentIcon from '../../assets/images/navbar/document.svg';
import DocumentIconActive from '../../assets/images/navbar/document_active.svg';
import AnalysisIcon from '../../assets/images/navbar/analysis.svg';
import AnalysisIconActive from '../../assets/images/navbar/analysis_active.svg';
import ContractIcon from '../../assets/images/navbar/contract.svg';
import ContractIconActive from '../../assets/images/navbar/contract_active.svg';
import GuidelineIcon from '../../assets/images/navbar/guidelines.svg';
import GuidelineIconActive from '../../assets/images/navbar/guidelines.svg';

interface IconPair {
  default: string;
  active: string;
}

interface NavigationIcons {
  [key: string]: IconPair;
}

const navigationIcons: NavigationIcons = {
  Home: { default: HomeIcon, active: HomeIconActive },
  Analysis: { default: AnalysisIcon, active: AnalysisIconActive },
  Documents: { default: DocumentIcon, active: DocumentIconActive },
  Contract: { default: ContractIcon, active: ContractIconActive },
  Guidelines: { default: GuidelineIcon, active: GuidelineIcon },
};

export default navigationIcons;
