import React, { PureComponent } from "react";
import { BrowserRouter as Router, Route, Link, Switch } from "react-router-dom";
import "./App.css";
import Block from "./Block.js";
import ExampleWrapper from "./ExampleWrapper";

const PAGE_LENGTH = 50;

class App extends PureComponent {
  state = {
    latestBlockHeight: -1,
    // map block hash to block object
    blocks: {},
    blockList: [],

    // list paging
    currentPage: 0,
    hasNextPage: false,
    isNextPageLoading: false
  };

  getBlock = blockHash => this.state.blocks[blockHash];

  setBlocks = newBlocks => {
    const blockList = [...this.state.blockList];
    for (const block of newBlocks) {
      if (!(block.hash in this.state.blocks)) {
        blockList.push(block);
      }
    }
    const blocks = blockList.reduce(function(map, obj) {
      map[obj.hash] = obj;
      return map;
    }, {});
    this.setState({ blocks, blockList });
  };

  setHeight = blockHeight => {
    this.setState({ latestBlockHeight: blockHeight });
  };

  componentDidMount() {
    this.fetchInitialBlocks();
    this.connectWebSockets();
  }

  componentDidUpdate() {
    const state = this.state;
    this.setState({
      hasNextPage: state.blockList.length < state.latestBlockHeight + 1,
      currentPage: Math.ceil(state.blockList.length / PAGE_LENGTH)
    });
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
          let { blockList, blocks } = { ...this.state };
          blockList = [new_block, ...blockList];
          blocks = { ...blocks };
          blocks[new_block.hash] = new_block;
          const latestBlockHeight = new_block.height;
          this.setState({ blockList, blocks, latestBlockHeight });
          console.log(
            `Block list updated: height - ${latestBlockHeight}, hash - ${new_block.hash}`
          );
        }
      };
    }
  }

  fetchInitialBlocks = () => {
    console.log("Fetching initial blocks ...");
    fetch("/blocks/")
      .then(response => {
        console.debug(response);
        return response.json();
      })
      .then(data => {
        console.log("Blocks retrieved:", data);
        if (data.count > 0) {
          const latestBlockHeight = data.count - 1;
          this.setHeight(latestBlockHeight);
          this.setBlocks(data.results);
        }
      })
      .catch(err => {
        console.error("Error Reading data " + err);
      });
  };

  fetchBlocks = pageNumber => {
    console.log(`Fetching blocks for page ${pageNumber} ...`);
    fetch(`/blocks/?page=${pageNumber}`)
      .then(response => {
        console.debug(response);
        return response.json();
      })
      .then(data => {
        console.log("Blocks retrieved:", data);
        this.setBlocks(data.results);
        this.setState({ isNextPageLoading: false });
        console.log(this.state);
      })
      .catch(err => {
        console.error("Error Reading data " + err);
      });
  };

  _loadNextPage = (...args) => {
    console.log("loadNextPage:", ...args);
    this.setState({ isNextPageLoading: true });
    if (this.state.blockList.length % PAGE_LENGTH === 0) {
      this.fetchBlocks(this.state.currentPage + 1);
    } else {
      this.fetchBlocks(this.state.currentPage);
    }
  };

  render() {
    const { hasNextPage, isNextPageLoading, blockList } = this.state;
    console.log(
      `Rendering... next page: ${hasNextPage}, loading: ${isNextPageLoading}, length: ${blockList.length}`
    );

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
                    <ExampleWrapper
                      hasNextPage={hasNextPage}
                      isNextPageLoading={isNextPageLoading}
                      items={blockList}
                      loadNextPage={this._loadNextPage}
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
