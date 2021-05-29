import React from "react";
import Select from "react-select";
import * as QueryString from "query-string";

import "./RadarChartPicker.css";
import boot from "../imgs/boot.svg";
import strategy from "../imgs/strategy.svg";

import { API_ROOT_URL } from "../components/radar_chart/RadarChart";
class RadarChartPicker extends React.Component {
  constructor() {
    super();
    this.state = {
      metricsNames: [],
      playerNames: [],
      selectedMetrics: [],
      selectedPlayer: "",
    };

    this.handlePlayerOnChange = this.handlePlayerOnChange.bind(this);
    this.handleMetricsOnChange = this.handleMetricsOnChange.bind(this);
  }

  async componentDidMount() {
    let apiUrl = QueryString.stringifyUrl({ url: API_ROOT_URL + "/metrics/radar" });
    await fetch(apiUrl)
      .then((response) => response.json())
      .then((data) => { this.setState({metricsNames: data})})
      .catch((error) => { console.log("Unable to get metrics: ", error)});
    

    apiUrl = QueryString.stringifyUrl({ url: API_ROOT_URL + "/metrics/player" });
    fetch(apiUrl)
      .then((response) => response.json())
      .then((data) => { this.setState({playerNames: data})})
      .catch((error) => { console.log("Unable to get playerNames: ", error)});
  }

  pickersData = () => {
    this.props.pickersData(
      this.state.selectedPlayer,
      this.state.selectedMetrics.map((met) => met.value)
    );
  };

  handleSubmit(event) {
    event.preventDefault();
    this.pickersData();
  }

  handlePlayerOnChange(event) {
    this.setState({ selectedPlayer: event.value });
  }

  handleMetricsOnChange(event) {
    this.setState({ selectedMetrics: event });
  }

  handleNoPlayersOptions() {
    return (
      <div>
        <img
          src={boot}
          style={{ transform: "rotate(-45deg)", width: "3em", height: "3em" }}
          alt="Players not found"
        ></img>
        <p>Sorry, but it seems like we cannot fetch any players!</p>
      </div>
    );
  }

  handleNoMetricsOptions() {
    return (
      <div>
        <img
          src={strategy}
          style={{ width: "3em", height: "3em" }}
          alt="Metrics not found"
        ></img>
        <p>Sorry, but it seems like we cannot fetch any metrics!</p>
      </div>
    );
  }

  render() {
    return (
      <form
        onSubmit={(event) => this.handleSubmit(event)}
        className="radar-chart-selector"
      >
        <Select
          className="player-selector"
          options={this.state.playerNames}
          noOptionsMessage={this.handleNoPlayersOptions}
          onChange={this.handlePlayerOnChange}
          placeholder="Pick your player!"
        />
        <Select
          className="metrics-selector"
          options={this.state.metricsNames}
          isMulti={true}
          onChange={this.handleMetricsOnChange}
          noOptionsMessage={this.handleNoMetricsOptions}
          placeholder="Pick your metrics"
        />
        <input type="submit" value="Go!" className="chart-picker-go" />
      </form>
    );
  }
}

export default RadarChartPicker;
