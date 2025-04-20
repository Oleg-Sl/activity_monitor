import React from "react";
import thompsonImg from "../../assets/img/thompson.jpg";


class Info extends React.Component {
  render() {
    return (
      <React.Fragment>
        <div className="name-user">Слепцов О.</div>
        <div className="avatar-user">
          <img src={thompsonImg} alt="Thompson" />
        </div>
      </React.Fragment>
    );
  }
}

export default Info;
