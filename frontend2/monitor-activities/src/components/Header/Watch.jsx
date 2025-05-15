import React from "react";

class Watch extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      time: new Date().toLocaleTimeString()
    };
  }

  componentDidMount() {
    this.timerID = setInterval(
      () => this.tick(),
      1000
    );
  }

  componentWillUnmount() {
    clearInterval(this.timerID);
  }

  tick() {
    this.setState({
      time: new Date().toLocaleTimeString()
    });
  }

  render() {
    return (
      <React.Fragment>
        <div className="watch-timer">
          {/* <h2>Текущее время:</h2> */}
          <div className="time-display">{this.state.time}</div>
        </div>
      </React.Fragment>
    );
  }
}

export default Watch;