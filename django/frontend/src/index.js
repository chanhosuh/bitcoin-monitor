import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import Price from './Price';
import Blockchain from './Blockchain';
import * as serviceWorker from './serviceWorker';

ReactDOM.render(<Price />, document.getElementById('markets'));
ReactDOM.render(<Blockchain />, document.getElementById('blockchain'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
