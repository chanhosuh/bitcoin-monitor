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
		const hostname = window.location.hostname;
		this.connection = new WebSocket(
			`ws://${hostname}/ws/BTC/USD`
		);
	
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
		const classes = this.state.change >= 0 ? 'panel Price-display-increase' : 'panel Price-display-decrease';

		return (
				<div class="col-sm-8">
					<div class="panel panel-blue">Markets
				          <div class="row">
				              <div class="col-md-7">
				                 <div class="panel panel-purple">{ticker}</div>   
				              </div>
				              <div class="col-md-5">
				              	<div id={ticker} className={classes} key={Math.random()}>{price}</div>
				              </div>
				          </div>
				     </div>
				 </div>
		);
	}
}

export default Price;
