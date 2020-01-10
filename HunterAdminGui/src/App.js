/**
 * Created by b5mali4 on 2019/7/30.
 */
import React, {Component} from 'react';
import LoginPage from './LoginPage';
import ManageIndexPage from './Manage';

import {BrowserRouter as Router, Route, Link, Switch, NavLink, Redirect} from "react-router-dom";

export default class App extends Component {
    render() {
        return (
            <Router>
                <Switch>
                    <Route path="/login" component={LoginPage}/>
                    <Route path="/manage" component={ManageIndexPage}/>
                    <Redirect from="/" to="/manage"/>
                </Switch>
            </Router>
        )
    }
}