import React from 'react';
import './Main.css';
import RadarChartContainer from './components/radar_chart/RadarChartContainer.js'
import HomePageContainer from "./components/home_page/HomePageContainer.js"
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

class MainWindow extends React.Component{
  render() {
    return (
      <Router>
      <div id="app-root">
          <div id="nav-bar">
            <h1>Piłkarzyki</h1> 
            <div className="links">
              <a href="/">Home</a>
              <a href="/radar">Radar Chart</a>
              </div>            
          </div>
          <div className="base-container">
            <Switch>
            <Route exact path="/">
                <HomePageContainer/>
              </Route>
              <Route exact path="/radar">
                <RadarChartContainer/>
              </Route>
            </Switch>
          </div>
        <div id="footer">
          Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from 
          <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>
        </div>
      </div>
      </Router>
    )
  }
}
export default MainWindow;
