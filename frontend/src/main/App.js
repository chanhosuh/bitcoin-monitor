import React, { PureComponent } from "react";
import { BrowserRouter as Router, Route, Link, Switch } from "react-router-dom";
import "./App.css";
import Block from "../block/Block";
import BlockRow from "../block/BlockRow";
import ExampleWrapper from "../common/ExampleWrapper";
import Price from "../price/Price";
import SearchBox from "../common/SearchBox";

// for testing
import testBlockData from "../test_data/blocks.json";

const PAGE_LENGTH = 50;

class App extends PureComponent {
  state = {
    latestBlockHeight: -1,

    // loaded blocks
    blocks: {}, // map hash to block
    blockList: [], // starting from latest height

    // list paging
    currentPage: 0,
    hasNextPage: false,
    isNextPageLoading: false,
  };

  componentDidMount() {
    this.fetchInitialBlocks();
    this.connectWebSockets();
    // for testing
    this.setBlocks(testBlockData);
  }

  componentDidUpdate() {
    const state = this.state;
    console.log("Current state: ", this.state);
    this.setState({
      hasNextPage: state.blockList.length < state.latestBlockHeight + 1,
      currentPage: Math.ceil(state.blockList.length / PAGE_LENGTH),
    });
  }

  getBlock = (blockHash) => this.state.blocks[blockHash];

  setBlocks = (newBlocks) => {
    const blockList = [...this.state.blockList];
    for (const block of newBlocks) {
      if (!(block.hash in this.state.blocks)) {
        blockList.push(block);
      }
    }
    const blocks = blockList.reduce(function (map, obj) {
      map[obj.hash] = obj;
      return map;
    }, {});
    this.setState({ blocks, blockList });
  };

  setHeight = (blockHeight) => {
    this.setState({ latestBlockHeight: blockHeight });
  };

  connectWebSockets() {
    const hostname = process.env.REACT_APP_WEBSOCKET_HOST;
    console.log(`Connecting websockets at ${hostname} ...`);

    this.connections = {
      block: new WebSocket(`ws://${hostname}/ws/block`),
    };

    for (const message_type in this.connections) {
      const conn = this.connections[message_type];
      // eslint-disable-next-line no-loop-func
      conn.onmessage = (event) => {
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
            `Block list updating: height - ${latestBlockHeight}, hash - ${new_block.hash}`
          );
        }
      };
    }
  }

  fetchInitialBlocks = () => {
    console.log("Fetching initial blocks ...");
    fetch("/blocks/")
      .then((response) => {
        console.debug(response);
        if (!response.ok) {
          throw new Error("HTTP status " + response.status);
        }
        return response.json();
      })
      .then((data) => {
        console.log("Blocks retrieved:", data);
        if (data.count > 0) {
          const latestBlockHeight = data.count - 1;
          this.setHeight(latestBlockHeight);
          this.setBlocks(data.results);
          // const jsonData = JSON.stringify(data.results);
          // console.log(jsonData);
        }
      })
      .catch((err) => {
        console.error("fetchInitialBlocks: " + err);
      });
  };

  fetchBlocks = (pageNumber) => {
    console.log(`Fetching blocks for page ${pageNumber} ...`);
    fetch(`/blocks/?page=${pageNumber}`)
      .then((response) => {
        console.debug(response);
        if (!response.ok) {
          throw new Error("HTTP status " + response.status);
        }
        return response.json();
      })
      .then((data) => {
        console.log("Blocks retrieved:", data);
        this.setBlocks(data.results);
        this.setState({ isNextPageLoading: false });
      })
      .catch((err) => {
        console.error("fetchBlocks: " + err);
      });
  };

  loadNextPage = (...args) => {
    console.log("loadNextPage:", ...args);
    this.setState({ isNextPageLoading: true });
    if (this.state.blockList.length % PAGE_LENGTH === 0) {
      this.fetchBlocks(this.state.currentPage + 1);
    } else {
      this.fetchBlocks(this.state.currentPage);
    }
  };

  displaySearchResults = (searchResults) => {
    this.setState({ blockList: searchResults });
  };

  displayBlockList = () => {
    this.setState({ blockList: [] }, this.fetchInitialBlocks);
  };

  render() {
    const { hasNextPage, isNextPageLoading, blockList } = this.state;
    console.log(
      `Rendering... next page: ${hasNextPage}, loading: ${isNextPageLoading}, length: ${blockList.length}`
    );

    return (
      <Router>
        <div className="container">
          <div className="menu-container">
            <div className="menu">
              <Price />
              <div className="links">
                <span style={{ padding: "10px" }}>
                  <Link to="/">Blocks</Link>
                </span>
                <span style={{ padding: "10px" }}>
                  <Link to="/transactions">Transactions</Link>
                </span>
              </div>
            </div>
          </div>
          <div className="header-container">
            <div className="header">
              <div className="title outlined">Bitcoin Block Explorer</div>
            </div>
          </div>
          <div className="search-container">
            <SearchBox
              onSubmit={this.displaySearchResults}
              onClear={this.displayBlockList}
            />
          </div>

          <div className="page">
            {/* <div className="sidebar"></div> */}
            <div className="content">
              <Switch>
                <Route
                  exact
                  path="/"
                  render={(props) => (
                    <ExampleWrapper
                      hasNextPage={hasNextPage}
                      isNextPageLoading={isNextPageLoading}
                      items={blockList}
                      loadNextPage={this.loadNextPage}
                      RowComponent={BlockRow}
                    />
                  )}
                />
                <Route
                  path="/block/:blockHash"
                  render={(props) => (
                    <Block {...props} getBlock={this.getBlock} />
                  )}
                />
              </Switch>
            </div>
          </div>

          <div className="footer">
            <div className="footer-item">donate</div>
            <div className="footer-item">about</div>
            <div className="footer-item">contact</div>
          </div>
        </div>
      </Router>
    );
  }
}

export default App;
