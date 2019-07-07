import React, {Component} from 'react';


class PriceComponent extends Component {
  constructor(props) {
    super(props);
    this.state = {
    	ticker: 'BTCUSD',
    	price: '',
    };
  }

  componentDidMount() {
    // this is an "echo" websocket service
	const hostname = window.location.hostname;
    this.connection = new WebSocket(
    	`ws://${hostname}/ws/BTC/USD`
    );
    // listen to onmessage event
    this.connection.onmessage = event => {
        console.log(event);
        const data = JSON.parse(event.data);
        if ('price' in data) {
            this.setState({
            	price: data['price']
            })
        };
    };
  }
 
  render() {
	  const ticker = this.state.ticker
	  const price = this.state.price
	  return (
		  <div className="ticker input-group">
			  <div className="input-group-prepend">
				  <button type="button" value={ticker} className="PriceButton btn-info btn-success">{ticker}</button>
			  </div>
			<input id={ticker} className="form-control" value={price} placeholder="..." type="text" readOnly="readonly"/>
		  </div>
	)
  }
}

export default PriceComponent;
