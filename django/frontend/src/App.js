import React from "react";
import { BrowserRouter as Router, Route, Link, Switch } from "react-router-dom";
import "./App.css";
import Block from "./Block.js";
import Home from "./Home.js";

class App extends React.Component {
  state = {
    latestBlockHeight: 0,
    // map block hash to block object
    blocks: {},
    block_list: []
  };

  getBlock = blockHash => this.state.blocks[blockHash];

  setBlocks = block_list => {
    const blocks = block_list.reduce(function(map, obj) {
      map[obj.hash] = obj;
      return map;
    }, {});
    this.setState({ blocks, block_list });
  };

  setHeight = blockHeight => {
    this.setState({ latestBlockHeight: blockHeight });
  };

  async componentDidMount() {
    this.connectWebSockets();
    this.fetchBlocks();
  }

  connectWebSockets() {
    const hostname = process.env.REACT_APP_WEBSOCKET_HOST;
    console.log(`Connecting websockets at ${hostname} ...`);

    this.connections = {
      block: new WebSocket(`ws://${hostname}/ws/block`)
    };

    for (const message_type in this.connections) {
      const conn = this.connections[message_type];
      // eslint-disable-next-line no-loop-func
      conn.onmessage = event => {
        console.debug(event);
        const data = JSON.parse(event.data);
        if (data.block) {
          const new_block = data.block;
          let { block_list, blocks } = { ...this.state };
          if (block_list) block_list.pop();
          block_list = [new_block, ...block_list];
          blocks[new_block.hash] = new_block;
          const latestBlockHeight = new_block.height;
          this.setState({ block_list, blocks, latestBlockHeight });
          console.log(
            `Block list updated: height - ${latestBlockHeight}, hash - ${new_block.hash}`
          );
        }
      };
    }
  }

  async fetchBlocks() {
    console.log("Fetching blocks ...");
    fetch("/blocks/")
      .then(response => {
        console.debug(response);
        return response.json();
      })
      .then(data => {
        console.log("Blocks retrieved:", data);
        const latestBlockHeight = data.count - 1;
        const block_list = data.results;
        this.setHeight(latestBlockHeight);
        this.setBlocks(block_list);
      })
      .catch(err => {
        console.error("Error Reading data " + err);
      });
  }

  render() {
    return (
      <div className="App">
        <div className="App-header">
          <h2>Block Explorer</h2>
        </div>
        <div className="App-nav">
          <Router>
            <div>
              <h2>
                <Link to="/">Blocks</Link>
                <span className="navigationSpace" />
                <Link to="/transactions">Transactions</Link>
              </h2>
              <Switch>
                <Route
                  exact
                  path="/"
                  render={props => (
                    <Home
                      {...props}
                      block_list={this.state.block_list}
                      latestBlockHeight={this.state.latestBlockHeight}
                    />
                  )}
                />
                <Route
                  path="/block/:blockHash"
                  render={props => (
                    <Block {...props} getBlock={this.getBlock} />
                  )}
                />
              </Switch>
            </div>
          </Router>
        </div>
      </div>
    );
  }
}

export default App;
