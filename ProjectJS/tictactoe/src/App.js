import React, { Component } from 'react';
import './App.css';
import Game from './Game.js';

class App extends Component {
  render() {
    return (
      <div className="App">
        <h2> Tic Tac Toe</h2>
          <Game></Game>
      </div>
    );
  }
}

export default App;
