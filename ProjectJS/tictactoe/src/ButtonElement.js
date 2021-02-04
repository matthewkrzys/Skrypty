import React from 'react';
import './ButtonElement.css';

function ButtonElement(props){
		return (
			<button className="square" onClick={() => props.onClick()}>
			{props.value}
			</button>
		)
}
export default ButtonElement;