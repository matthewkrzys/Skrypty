import React from 'react';
import BoardGame from './BoardGame';
import './Game.css';

class Game extends React.Component {
  constructor() {
    super();
    this.state = {
      list: ["", "", "", "", "", "", "", "", ""],
      player: 1,
      win: false
    };
  }

  isWinner() {
    const arrayWithWinField = [
      [0, 1, 2],
      [3, 4, 5],
      [6, 7, 8],
      [0, 3, 6],
      [1, 4, 7],
      [2, 5, 8],
      [0, 4, 8],
      [2, 4, 6],
    ]
    for (let i = 0; i < arrayWithWinField.length; i++) {
      const [a, b, c] = arrayWithWinField[i];
      if (this.state.list[a] !== "" && this.state.list[b] !== "" && this.state.list[c] !== "") {
        if (this.state.list[a] === this.state.list[b] && this.state.list[b] === this.state.list[c] && this.state.list[c] === this.state.list[a]) {
          return true;
        }
      }
    }
    return false;
  }

  handleClick(i) {
    let nextPlayer = 0;
    if (this.state.list[i] === "") {
      if (this.state.player == 0) {
        this.state.list[i] = "0";
        nextPlayer = 1;
      }
      else {
        this.state.list[i] = "X";
        nextPlayer = 0
      }
    }

    this.setState({
      list: this.state.list,
      player: nextPlayer
    });

  }

  render() {

    let message = "";
    if (this.isWinner()) {
      message = <div>Winner is Player {(this.state.player + 1) % 2}</div>;
    }
    else {
      message = <div>Player {this.state.player}</div>;
    }

    return (
      <div className="game">
        <div className="board">
          <h3> Board </h3>
          <BoardGame squares={this.state.list} onClick={(i) => this.handleClick(i)} />
        </div>
        <div className="info">
          <h3> Game Info </h3>
          <div>Player 0 = 0</div>
          <div>Player 1 = X</div>
          {message}
        </div>
      </div>
    );
  }
}
export default Game;