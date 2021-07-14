import React from "react";
import {
  Chart,
  RadarController,
  RadialLinearScale,
  PointElement,
  LineElement,
} from "chart.js";
import * as QueryString from "query-string";


import "./RadarChart.css";
import RedCardIcon from '../../imgs/red-card.svg';

Chart.register(RadarController, RadialLinearScale, PointElement, LineElement);

const API_ROOT_URL = "http://localhost:2137";

class RadarChart extends React.Component {
  constructor(props) {
    super(props);
    this.chartRef = React.createRef();
    this.getRadarChart = this.getRadarChart.bind(this);
    this.state = {
        chart: null,
        error: null
    }
  }

  componentDidUpdate(prevProps, _) {
    if (
      (prevProps.playerID !== this.props.playerID && this.props.playerID !== "") ||
      prevProps.metrics !== this.props.metrics
    ) {
      this.setState({error: null});
      if (this.state.chart != null) {
        this.state.chart.destroy();
      }
      this.getRadarChart();
    }
  }

  async getMetrics() {
    if (this.props.playerID === null | this.props.playerID === ""){
      this.setState({error: "You must pick a player, dummy!"})
      return
    }
    const apiUrl = QueryString.stringifyUrl({
      url: API_ROOT_URL + "/radar",
      query: {
        player_id: this.props.playerID,
        metrics_ids: this.props.metrics.length === 0 ? [] : this.props.metrics,
      },
    });
    const response = await fetch(apiUrl);
    if (response.status !== 200){
      this.setState({error: "Cannot process request"})
      return
    }
    const data = await response.json();

    return {
      labels: data["labels"],
      playerName: data["name"],
      metrics: data["metrics"],
    };
  }

  async getRadarChart() {
    const metricsData = await this.getMetrics();
    if (metricsData){
      const myChartRef = this.chartRef.current.getContext("2d");
      const chart_data = {
        labels: metricsData.labels,
        datasets: [
          {
            label: metricsData["playerName"],
            data: metricsData["metrics"],
            fill: true,
            backgroundColor: "rgba(255, 99, 132, 0.2)",
            borderColor: "rgb(255, 99, 132)",
            pointBackgroundColor: "rgb(255, 99, 132)",
            pointBorderColor: "#fff",
            pointHoverBackgroundColor: "#fff",
            pointHoverBorderColor: "rgb(255, 99, 132)",
          },
        ],
      };
      let chart = new Chart(myChartRef, {
        type: "radar",
        data: chart_data,
        options: {
          maintainAspectRatio: false,
        },
      });
      this.setState({ chart: chart });
    }
  }

  render() {
    let element = null;
    if (this.state.error){
      element = <div className="error-div">
        <div className="error-card">
          <img
            src={RedCardIcon}
            style={{ height: 80, width: 80 }}
            alt="red-card"
          />
        </div>
        <p>Sorry, we are unable to process your request.</p>
        <p>{this.state.error}</p>
      </div>
    }
    else{
      element = <canvas ref={this.chartRef} />;
    }
    return (
      <div className="radar-instance" data-testid="radar-instance">
        {element}
      </div>
    );
  }
}

export {
  RadarChart,
  API_ROOT_URL
}
