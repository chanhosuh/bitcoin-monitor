import React from "react";
import "./Price.css";

class Price extends React.Component {
  state = {
    BTCUSD: {
      price: NaN,
      change: NaN
    },
    ETHUSD: {
      price: NaN,
      change: NaN
    }
  };

  connections = {};

  componentDidMount() {
    this.connectPriceWebsockets();
  }

  connectPriceWebsockets() {
    const hostname = process.env.REACT_APP_WEBSOCKET_HOST;
    console.log(`Connecting price websockets at ${hostname} ...`);

    this.connections["BTCUSD"] = new WebSocket(`ws://${hostname}/ws/BTC/USD`);
    this.connections["ETHUSD"] = new WebSocket(`ws://${hostname}/ws/ETH/USD`);

    for (const ticker of ["BTCUSD", "ETHUSD"]) {
      const conn = this.connections[ticker];
      // eslint-disable-next-line no-loop-func
      conn.onmessage = event => {
        console.debug(event);
        const data = JSON.parse(event.data);
        if ("price" in data) {
          const price = data["price"];
          const last_price = this.state[ticker].price;
          const change = last_price ? price - last_price : NaN;
          this.setState(state => {
            const new_state = { ...state };
            new_state[ticker] = { price, change };
            return new_state;
          });
          console.debug(
            `${ticker} price updating: price - ${price}, change - ${change}`
          );
        }
      };
    }
  }

  render() {
    var rows = [];
    for (const ticker in this.state) {
      const classes =
        this.state[ticker].change >= 0
          ? "panel Price-display-increase"
          : "panel Price-display-decrease";
      const price = this.state[ticker].price;

      rows.push(
        <div key={ticker}>
          <div>{ticker}</div>
          <div className={classes} key={Math.random()}>
            {price}
          </div>
        </div>
      );
    }
    return <div className="price-rows">{rows}</div>;
  }
}

export default Price;
