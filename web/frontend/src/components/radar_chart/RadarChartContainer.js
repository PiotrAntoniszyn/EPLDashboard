import React from "react";

import "./RadarChartContainer.css";
import RadarChartPicker from "../../pickers/RadarCharPicker";
import RadarChart from "./RadarChart"
import logo from "../../imgs/football-badge.svg";



class RadarChartContainer extends React.Component {
  constructor() {
    super();
    this.state = {
      teamID: null,
      metrics: [],
    };
  }

  pickersData = (teamID, metrics) => {
    this.setState({ teamID, metrics });
  };

  render() {
    return (
      <div className="radar-container">
        <RadarChartPicker pickersData={this.pickersData} />
        <div className="radar-team-data-container">
          <div style={{ width: "100%" }}>
            <img alt="football-badge" src={logo} width="80" height="80"></img>
          </div>
          <p>Team Info: {this.state.teamID}</p>
        </div>
        <RadarChart teamID={this.state.teamID} metrics={this.state.metrics}/>
      </div>
    );
  }
}

export default RadarChartContainer;
