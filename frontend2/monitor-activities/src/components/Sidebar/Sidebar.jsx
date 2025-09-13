import React from "react";
import SawingDepartment from "./SawingDepartment.jsx";
import AssemblyDepartment from "./AssemblyDepartment.jsx";

import Manage from "./Manage.jsx";
import Boards from "./Boards.jsx";
import Reports from "./Reports.jsx";
import Schedule from "./Schedule.jsx";
import Settings from "./Settings.jsx";

class Sidebar extends React.Component {
  render() {
    return (
      <section className="kanban__sidebar">
        <div className="kanban__sidebar-menu">
          <SawingDepartment />
          <AssemblyDepartment />
          {/* <Manage />
          <Boards />
          <Schedule />
          <Reports /> */}
        </div>
        <Settings />
      </section>
    );
  }
}

export default Sidebar;
