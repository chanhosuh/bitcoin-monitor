import React from "react";
import { Link } from "react-router-dom";
import "./Block.css";

const BlockRow = ({ items, index, style }) => {
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
  const { height, hash, age, num_transactions, timestamp } = items[index];
  return (
    <div style={style}>
      <div className="row">
        <span className="rowelem">{height}</span>
        <span className="rowelem">
          <Link to={`/block/${hash}`}>{hash}</Link>
        </span>
        <span className="rowelem">{age}</span>
      </div>
    </div>
  );
};

export default BlockRow;
