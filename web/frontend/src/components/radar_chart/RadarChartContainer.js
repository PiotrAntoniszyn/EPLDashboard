import React from "react";

import "./RadarChartContainer.css";
import RadarChartPicker from "../../pickers/RadarCharPicker";
import { RadarChart } from "./RadarChart";
import PlayerInfo from "../team_info/PlayerInfo";



class RadarChartContainer extends React.Component {
  constructor() {
    super();
    this.state = {
      playerID: null,
      metrics: [],
    };
  }

  pickersData = (playerID, metrics) => {
    this.setState({ playerID, metrics });
  };

  render() {
    return (
      <div className="radar-container">
        <RadarChartPicker pickersData={this.pickersData} />
        <PlayerInfo playerID={this.state.playerID}/>
        <RadarChart playerID={this.state.playerID} metrics={this.state.metrics}/>
      </div>
    );
  }
}

export default RadarChartContainer;
