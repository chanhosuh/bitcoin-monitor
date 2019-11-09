import React, { Component } from "react";
import "./Home.css";
import _ from "lodash";
import { Link } from "react-router-dom";

class Home extends Component {
  render() {
    var tableRows = [];
    _.each(this.props.blocks, (value, index) => {
      console.log(value, index);
      /*
      age: "10 years, 9 months ago"
      bits: "ffff001d"
      hash: "00000000f8246f56ac5bf25d799247bac3d0b1349ba72c105092f5a022a48f68"
      height: 2118
      merkle_root: "97919e93371b8648967e1e1be9d30511cf642903bd9b388f51acd4debc306fb0"
      nonce: "1cbe648e"
      num_transactions: 1
      prev_hash: "0000000087fcd3a97d43df5fea343a41e1dfdbe0a4cc5f61bbebf9589fd7e01d"
      timestamp: 1233150472
      version: 1
      */
      const { height, hash, age } = value;
      tableRows.push(
        <tr key={hash}>
          <td className="tdCenter">{height}</td>
          <td>
            <Link to={`/block/${hash}`}>{hash}</Link>
          </td>
          <td className="tdCenter">{age}</td>
        </tr>
      );
    });

    return (
      <div className="Home">
        <h2> Current Block: {this.props.latestBlockHeight} </h2>
        <table>
          <thead>
            <tr>
              <th>Block Height</th>
              <th>Hash</th>
              <th>Age</th>
            </tr>
          </thead>
          <tbody>{tableRows}</tbody>
        </table>
      </div>
    );
  }
}

export default Home;
