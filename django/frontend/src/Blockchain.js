import React from 'react';
import './Blockchain.css';


class Blockchain extends React.Component {
	constructor(props) {
		super(props);
	}

	componentDidMount() {
	}
 
	render() {
		var rows = [];
		rows.push(
			<div className="row">
				<div className="col">
					<div className="panel">Total Transactions</div>   
				</div>
				<div className="col">
					<div className="panel">1000000000</div>   
				</div>
			</div>
		);
		rows.push(
			<div className="row">
				<div className="col">
					<div className="panel">Hashrate</div>   
				</div>
				<div className="col">
					<div className="panel">1000000000</div>   
				</div>
			</div>
		);
		rows.push(
				<div className="row">
					<div className="col">
						<div className="panel">Difficulty</div>   
					</div>
					<div className="col">
						<div className="panel">1000000000</div>   
					</div>
				</div>
		);
		return (
			<div className="col">
			   	<div className="panel panel-grey">Blockchain
			   		{rows}
				</div>
			</div>
		);
	}
}

export default Blockchain;
