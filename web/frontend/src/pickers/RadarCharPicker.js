import React from "react";
import Select from "react-select";

import "./RadarChartPicker.css";
import boot from "../imgs/boot.svg";
import strategy from "../imgs/strategy.svg";

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
    const metricsUrl = await "http://localhost:2137/radar/metrics";
    const metricsResponse = await fetch(metricsUrl);
    const metricsNames = await metricsResponse.json();

    const playerUrl = await "http://localhost:2137/metrics/player";
    const playerResponse = await fetch(playerUrl);
    const playerNames = await playerResponse.json();
    this.setState({ metricsNames: metricsNames, playerNames: playerNames });
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
    console.log("Updating metrics");
    this.setState({ selectedMetrics: event });
  }

  handleNoPlayersOptions() {
    return (
      <div>
        <img
          src={boot}
          style={{ transform: "rotate(-45deg)", width: "3em", height: "3em" }}
        ></img>
        <p>Sorry, but it seems like we cannot fetch any players!</p>
      </div>
    );
  }

  handleNoMetricsOptions() {
    return (
      <div>
        <img src={strategy} style={{ width: "3em", height: "3em" }}></img>
        <p>Sorry, but it seems like we cannot fetch any metrics!</p>
      </div>
    );
  }

  render() {
    return (
      <form
        onSubmit={(event) => this.handleSubmit(event)}
        className="radar-chart-selector"
        data-testid="DUPA"
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
