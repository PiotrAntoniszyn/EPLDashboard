import React from 'react';
import './Main.css';
import RadarChartContainer from './components/radar_chart/RadarChartContainer.js'


class MainWindow extends React.Component{
  render() {
    return (
    <div id="app-root">
        <RadarChartContainer/>
      <div id="footer">
        Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from 
        <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>
      </div>
    </div>
    )
  }
}
export default MainWindow;