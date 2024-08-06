import { Roles } from "../auth/roles";
import TrackTimePopup from "../popup/TrackTimePopup";
import React, {ReactElement} from "react";
import AddUserPopup from "../popup/AddUserPopup";
import AddVacationPopup from "../popup/AddVacationPopup";
import {TrackTimeActionIcon} from "../../assets/iconComponents/navbar/TrackTimeActionIcon";
import {AddVacationActionIcon} from "../../assets/iconComponents/navbar/AddVacationActionIcon";

interface ButtonConfig {
  icon: any;
  label: string;
  action: () => void;
  popup: ReactElement;
}

type ButtonConfigurations = {
  [K in Roles]: ButtonConfig[];
};

export const buttonConfigurations: ButtonConfigurations  = {

  Admin: [
    {
      icon: <TrackTimeActionIcon/>,
      label: "Add User",
      action: () => console.log("Managing users"),
      popup: <AddUserPopup/>
    },
  ],
  Hiwi: [
    {
      icon: <TrackTimeActionIcon/>,
      label: "Track Time",
      action: () => console.log("Track Time"),
      popup: <TrackTimePopup/>
    },
    {
      icon: <AddVacationActionIcon/>,
      label: "Add Vacation",
      action: () => console.log("Add Vacation"),
      popup: <AddVacationPopup/>
    }
  ],
  Supervisor: [
    {
      icon: <TrackTimeActionIcon/>,
      label: "Add Project",
      action: () => console.log("Add Project"),
      popup: <TrackTimePopup/>
    },
  ],
  Secretary: [

  ],
};

