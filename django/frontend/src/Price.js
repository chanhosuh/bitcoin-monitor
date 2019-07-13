import React from 'react';
import './Price.css';


class Price extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			'BTCUSD': {
				price: '',
				change: '',
			},
			'ETHUSD': {
				price: '',
				change: '',
			},
		};
	}

	componentDidMount() {
		const hostname = window.location.hostname;
		this.connections = {
			'BTCUSD': new WebSocket(`ws://${hostname}:8000/ws/BTC/USD`),
			'ETHUSD': new WebSocket(`ws://${hostname}:8000/ws/ETH/USD`),
		};
	
		for (const ticker in this.connections) {
			const conn = this.connections[ticker];
			conn.onmessage = event => {
				console.debug(event);
				const data = JSON.parse(event.data);
				if ('price' in data) {
					let new_state = this.state;
					new_state[ticker] = {
						price: data['price'],
						change: data['price'] - this.state[ticker].price,
					};
					this.setState(new_state);
				};
				console.debug(this.state);
			};
		}
	}
 
	render() {
		var rows = [];
		for (const ticker in this.state) {
			const classes = this.state[ticker].change >= 0 ? 'panel Price-display-increase' : 'panel Price-display-decrease';
			const price = this.state[ticker].price;

			rows.push(
			  <div className="row" key={ticker}>
				  <div className="col-md-7">
					 <div className="panel panel-purple">{ticker}</div>   
				  </div>
				  <div className="col-md-5">
					  <div id={ticker} className={classes} key={Math.random()}>{price}</div>
				  </div>
			  </div>
			)
		}
		return (
				<div className="col-sm-8">
					<div className="panel panel-blue">Markets
						{rows}
					</div>
				 </div>
		);
	}
}

export default Price;
