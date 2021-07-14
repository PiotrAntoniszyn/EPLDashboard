import React from "react";

import "./HomePageContainer.css";



class HomePageContainer extends React.Component {
  render() {
    return (
      <div className="homepage-container">
          <div className="homepage-message">
                <h1>Cześć, witaj w Piłkarzykach! </h1>
                <p>Amatorskiej aplikacji do analizy danych piłkarskich.</p>
          </div>
      </div>
    );
  }
}

export default HomePageContainer;
