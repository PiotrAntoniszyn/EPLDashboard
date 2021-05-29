import React from "react";
import logo from "../../imgs/football-badge.svg";
import "./PlayerInfo.css";
import { API_ROOT_URL } from "../radar_chart/RadarChart";
import * as QueryString from "query-string"

class PlayerInfo extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      teamName: null,
      position: null,
      age: 0,
      first_name: null,
      last_name: null,
      score: 0,
      loaded: false,
    };
  }

  componentDidUpdate(prevProps, _) {
    if (prevProps.playerID !== this.props.playerID) {
      this.getTeamData();
    }
  }

  async getTeamData() {
    const apiUrl = QueryString.stringifyUrl({
      url: API_ROOT_URL + `/teams/players/${this.props.playerID}`,
    });
    console.log(apiUrl)
    await fetch(apiUrl)
      .then((response) => response.json())
      .then((data) => {
        this.setState({
          teamName: data["team_name"],
          position: data["position"],
          age: data["age"],
          first_name: data["first_name"],
          last_name: data["last_name"],
          loaded: true,
          score: data["score"],
        });
      })
      .catch((error) => {
        console.log("LOL, ERROR", error);
      });
  }

  render() {
    let info = <div />;
    if (this.state.loaded) {
      info = (
        <div className="player-card">
          <div className="player-metric">
            <h3>{this.state.first_name}</h3>
            <h2>{this.state.last_name}</h2>
            <h3>{this.state.position}</h3>
            <h5>Age: {this.state.age}</h5>
            <h5>Team: {this.state.teamName}</h5>
          </div>
          <div className="player-score">
            <h1>{this.state.score}</h1>
          </div>
        </div>
      );
    }
    return (
      <div className="radar-team-data-container">
        <div style={{ padding: "0em 0 0 1.5em", width: "100%" }}>
          <img alt="football-badge" src={logo} width="80" height="80"></img>
        </div>
        <hr />
        {info}
      </div>
    );
  }
}

export default PlayerInfo;
