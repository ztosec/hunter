import React, {Component} from 'react';
import {request, STATUS_CODES} from '../utils/request';
import SysEmailSetForm from './SysEmailSet';
import {BrowserRouter as Router, Route, Link, Switch, NavLink, Redirect} from "react-router-dom";
import {Col, Row, Layout, Menu, Collapse, Card, Tooltip, Icon, Form, Input, Button, Checkbox, message} from 'antd';
import SysLdapSetPage from './SysLdapSet';
import SysProxySetPage from './SysProxySet';
import SysBaseSetPage from './SysBaseSet';
import HunterLogSetPage from './HunterLogSet';

const {TextArea} = Input;
const {SubMenu} = Menu;
const {Header, Content, Footer, Sider} = Layout;

/**
 * 设置黑白名单抓取规则规则，socketlog地址等
 */
export default class SysSetPage extends Component {

    render() {
        return (
            <Router>
                <Content style={{padding: '0 5px'}}>
                    <Layout style={{padding: '24px 0', background: '#fff'}}>
                        <Sider width={200} style={{background: '#fff'}}>
                            <Menu
                                mode="inline"
                                defaultSelectedKeys={['1']}
                                defaultOpenKeys={['sub1']}
                                style={{height: '100%'}}
                            >
                                <Menu.Item key="1">
                                    <Link style={{display: "inline"}}
                                          to={"/manage/setting/base"}><span>基础设置</span></Link>

                                </Menu.Item>
                                <Menu.Item key="2">
                                    <Link style={{display: "inline"}}
                                          to={"/manage/setting/hunterlog"}><span>回显设置</span></Link>
                                </Menu.Item>
                                <Menu.Item key="3">
                                    <Link style={{display: "inline"}}
                                          to={"/manage/setting/ldap"}><span>LDAP设置</span></Link>
                                </Menu.Item>
                            </Menu>
                        </Sider>
                        <Content style={{padding: '0 24px', minHeight: 280}}>
                            <Switch>
                                <Route path="/manage/setting/ldap" component={SysLdapSetPage}/>
                                <Route path="/manage/setting/hunterlog" component={HunterLogSetPage}/>
                                <Route path="/manage/setting/base" component={SysBaseSetPage}/>
                                <Redirect from="/" to="/manage/setting/base"/>
                            </Switch>
                        </Content>
                    </Layout>
                </Content>
            </Router>
        );
    }
}