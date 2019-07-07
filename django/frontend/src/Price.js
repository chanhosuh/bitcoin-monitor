import React from 'react';
import './Price.css';


class Price extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			ticker: 'BTCUSD',
			price: '',
			change: '',
		};
	}

	componentDidMount() {
		// this is an "echo" websocket service
		const hostname = window.location.hostname;
		this.connection = new WebSocket(
			`ws://${hostname}:8000/ws/BTC/USD`
		);
		// listen to onmessage event
		this.connection.onmessage = event => {
			console.debug(event);
			const data = JSON.parse(event.data);
			if ('price' in data) {
				this.setState({
					price: data['price'],
					change: data['price'] - this.state.price,
				})
			};
			console.debug(this.state);
		};
	}
 
	render() {
		const ticker = this.state.ticker;
		const price = this.state.price;
		const classes = this.state.change >= 0 ? 'form-control Price-display-increase' : 'form-control Price-display-decrease';

		return (
			<div className="ticker input-group">
				<div className="input-group-prepend">
					<button type="button" value={ticker} className="btn-info" disabled>{ticker}</button>
				</div>
				<input id={ticker} className={classes} value={price} key={Math.random()} placeholder="..." type="text" readOnly="readonly"/>
			</div>
		);
	}
}

export default Price;
