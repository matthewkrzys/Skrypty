import React from 'react';
import ButtonElement from './ButtonElement.js';
import './BoardGame.css'

class BoardGame extends React.Component {

    showButtomElement(i) {
        return <ButtonElement value={this.props.squares[i]} onClick={() => this.props.onClick(i)} />;
    }

    render() {
        return (
            <div>
        <div className="row">
          {this.showButtomElement(0)}
          {this.showButtomElement(1)}
          {this.showButtomElement(2)}
        </div>
        <div className="row">
          {this.showButtomElement(3)}
          {this.showButtomElement(4)}
          {this.showButtomElement(5)}
        </div>
        <div className="row">
          {this.showButtomElement(6)}
          {this.showButtomElement(7)}
          {this.showButtomElement(8)}
        </div>
            </div>
        );
    }
}
export default BoardGame;