import React from "react";
import { NavLink } from "react-router-dom";


class AssemblyDepartment extends React.Component {
  render() {
    return (
      <NavLink to="/kanban/assembly" activeClassName="active-area">
        <div className="assembly-area kanban-area">
            <i className="material-icons">build</i>
            <span>Сборка</span>
        </div>
      </NavLink>
    );
  }
}

export default AssemblyDepartment;