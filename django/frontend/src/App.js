import React from "react";
import { BrowserRouter as Router, Route, Link, Switch } from "react-router-dom";
import "./App.css";
import Block from "./Block.js";
import Home from "./Home.js";

class App extends React.Component {
  state = {
    latestBlockHeight: 0,
    // map block hash to block object
    blocks: {}
  };

  getBlock = blockHash => this.state.blocks[blockHash];

  setBlocks = blocks => {
    this.setState({ blocks });
  };

  setHeight = blockHeight => {
    this.setState({ latestBlockHeight: blockHeight });
  };

  async componentDidMount() {
    fetch("/blocks/")
      .then(response => {
        console.log(response);
        return response.json();
      })
      .then(data => {
        console.log(data);
        const latestBlockHeight = data.count - 1;
        const blocks = data.results.reduce(function(map, obj) {
          map[obj.hash] = obj;
          return map;
        }, {});
        this.setHeight(latestBlockHeight);
        this.setBlocks(blocks);
      })
      .catch(err => {
        console.log("Error Reading data " + err);
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
                <span class="navigationSpace" />
                <Link to="/transactions">Transactions</Link>
              </h2>
              <Switch>
                <Route
                  exact
                  path="/"
                  render={props => (
                    <Home
                      {...props}
                      blocks={this.state.blocks}
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
