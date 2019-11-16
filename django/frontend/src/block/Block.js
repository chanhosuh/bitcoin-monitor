import React, { Component } from "react";
import "./Block.css";

class Block extends Component {
  state = {
    block: null,
    blockHash: ""
  };

  setBlockState = blockHash => {
    console.log("Block hash: " + blockHash);
    const block = this.props.getBlock(blockHash);
    console.log(block);
    if (!block) return;
    const timestamp = Date(parseInt(block.timestamp, 10)).toString();
    const transactions = block.num_transactions;
    this.setState({ block, blockHash });
  };

  componentDidMount() {
    console.log(this.props);
    // Get the block hash from URL arguments (defined by Route pattern)
    const blockHash = this.props.match.params.blockHash;
    this.setBlockState(blockHash);
  }

  // componentWillReceiveProps(nextProps) {
  //   const old_hash = this.props.match.params.blockHash;
  //   const new_hash = nextProps.match.params.blockHash;
  //   // compare old and new URL parameter (block hash)
  //   // if different, reload state
  //   if (old_hash !== new_hash) this.setBlockState(new_hash);
  // }

  render() {
    const block = this.state.block;
    console.log(block);
    // const difficulty = parseInt(block.difficulty, 10);
    // const difficultyTotal = parseInt(block.totalDifficulty, 10);
    if (!block) {
      return (
        <div className="Block">
          <h2>Block Info</h2>
        </div>
      );
    }
    return (
      <div className="Block">
        <h2>Block Info</h2>
        <div>
          <table>
            <tbody>
              <tr>
                <td className="tdLabel">Height: </td>
                <td>{this.state.block.height}</td>
              </tr>
              <tr>
                <td className="tdLabel">Timestamp: </td>
                <td>{this.state.block.timestamp}</td>
              </tr>
              <tr>
                <td className="tdLabel">Transactions: </td>
                <td>{this.state.block_txs}</td>
              </tr>
              <tr>
                <td className="tdLabel">Hash: </td>
                <td>{this.state.block.hash}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    );
  }
}

export default Block;
