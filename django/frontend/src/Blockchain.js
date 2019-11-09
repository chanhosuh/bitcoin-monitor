import React from 'react';
import './Blockchain.css';

//
//class Blockchain extends React.Component {
//	constructor(props) {
//		super(props);
//	}
//
//	componentDidMount() {
//	}
// 
//	render() {
//		var rows = [];
//		rows.push(
//			<div className="row">
//				<div className="col">
//					<div className="panel">Total Transactions</div>   
//				</div>
//				<div className="col">
//					<div className="panel">1000000000</div>   
//				</div>
//			</div>
//		);
//		rows.push(
//			<div className="row">
//				<div className="col">
//					<div className="panel">Hashrate</div>   
//				</div>
//				<div className="col">
//					<div className="panel">1000000000</div>   
//				</div>
//			</div>
//		);
//		rows.push(
//				<div className="row">
//					<div className="col">
//						<div className="panel">Difficulty</div>   
//					</div>
//					<div className="col">
//						<div className="panel">1000000000</div>   
//					</div>
//				</div>
//		);
//		return (
//			<div className="col">
//			   	<div className="panel panel-grey">Blockchain
//			   		{rows}
//				</div>
//			</div>
//		);
//	}
//}
//
//export default Blockchain;


import { Column, Row } from 'simple-flexbox';

const Blockchain = () => {
	return (
		<Column flexGrow={1}>
			<Row horizontal='center'>
				<h1>HEADER</h1>
			</Row>
			<Row vertical='center'>
				<Column flexGrow={1} horizontal='center'>
					<h3> Column 1 </h3>
					<span> column 1 content </span>
				</Column>
				<Column flexGrow={1} horizontal='center'>
					<h3> Column 2 </h3>
					<span> column 2 content </span>
				</Column>
			</Row>
		</Column>
	);
}

export default Blockchain;