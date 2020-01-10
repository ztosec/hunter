import React, {Component} from 'react';
import {BrowserRouter as Router, Route, Link, Switch, NavLink, Redirect} from "react-router-dom";
import {Layout, Menu, Icon, Dropdown, Rate} from 'antd';
import logo from '../src/assets/logo.png';
import {request} from './utils/request';
import UserScanRecordsTable from './user/ScanRecords';
import VulnDetails from './user/VulnDetails';
import StaticsChar from './user/StaticsChar';
import user_avatar from '../src/assets/user_avatar.png';
import './index.css';
import {Avatar, Badge} from 'antd';
import logout from './utils/logout';
import UsersTable from './manage/UserManage';
import AdminTaskManagement from './manage/TaskManage';
import AdminScanRecordTable from './manage/ScanRecord';
import UserTaskManagement from  './user/TaskManagement';
import AdminStaticsChar from './manage/StaticsChar';
import PluginManagement from './manage/PluginManagement';
import SysSetPage from './manage/SysSet';
import ClientDownloadPage from './user/ClientPage';
import ClientManagePage from './manage/ClientManagePage';
import VulnTable from './manage/VulnManage';
const {Sider, Header, Content, Footer} = Layout;
const SubMenu = Menu.SubMenu;

export default class ManageIndexPage extends Component {
    state = {
        collapsed: false,
    };
    onCollapse = (collapsed) => {
        this.setState({collapsed});
    };

    constructor(props) {
        super(props);
        this.state = {
            userinfo: {},
            notice: {}
        };

    }

    componentWillMount() {
        this.onLoadData();
    };

    //加载用户基本信息和最新通知
    async onLoadData() {
        const userinfo = await request("/user/user_info/");
        this.setState({
            userinfo: userinfo.data
        });
        const notice = await request("/user/notice/");
        console.log(notice.data);
        if (notice.data !== "null") {
            //console.log("232323");
            this.setState({
                notice: notice
            });
        }
    };

    /**
     * 根据有用权限来判断显示管理菜单栏
     */
    showManageMenu(role) {
        if (role == 4) {
            return (
                <SubMenu key="sub1" title={<span><Icon type="setting" theme="outlined"/><span>管理设置</span></span>}>
                    <Menu.Item key="5">
                        <Icon type="team" theme="outlined"/>
                        <Link style={{display: "inline"}} to={"/manage/users"}><span>用户管理</span></Link>
                    </Menu.Item>

                    <Menu.Item key="6">
                        <Icon type="safety" theme="outlined"/>
                        <Link style={{display: "inline"}} to={"/manage/vulnerability"}><span>漏洞管理</span></Link>
                    </Menu.Item>

                    <Menu.Item key="7">
                        <Icon type="project" theme="outlined"/>
                        <Link style={{display: "inline"}} to={"/manage/task"}><span>任务管理</span></Link>
                    </Menu.Item>

                    <Menu.Item key="8">
                        <Icon type="api" theme="outlined"/>
                        <Link style={{display: "inline"}} to={"/manage/plugin"}><span>插件管理</span></Link>
                    </Menu.Item>

                    <Menu.Item key="9">
                        <Icon type="area-chart" theme="outlined"/>
                        <Link style={{display: "inline"}} to={"/manage/datachart"}><span>数据大盘</span></Link>
                    </Menu.Item>
                    <Menu.Item key="10">
                        <Icon type="tool" theme="outlined"/>
                        <Link style={{display: "inline"}} to={"/manage/setting/"}><span>系统设置</span></Link>
                    </Menu.Item>

                    <Menu.Item key="11">
                        <Icon type="shop" theme="outlined"/>
                        <Link style={{display: "inline"}} to={"/manage/client"}><span>客户端管理</span></Link>
                    </Menu.Item>
                </SubMenu>);
        }
        else {
            return null;
        }
    }

    /**
     *
     * @param avatar 头像地址
     * @param fullname 用户名
     */
    showAvatarMenu(full_name, message, avatar = user_avatar) {
        //退出按钮
        const userMenu = (
            <Menu>
                <Menu.Item>
                    <a href="#" onClick={() => logout()}><Icon type="logout" theme="outlined"/>退出登录</a>
                </Menu.Item>
            </Menu>
        );
        return (
            <Menu
                theme="dark"
                mode="horizontal"
                defaultSelectedKeys={['2']}
                style={{lineHeight: '64px', background: '#fff', fontSize: 14}}
            >
                <Menu.Item style={{width: '80%', textAlign: 'center', color: '#000', backgroundColor: '#fff'}}>
                    <p className="marquee">
                        {message}
                    </p>
                </Menu.Item>
                <Menu.Item style={{width: '10%', float: 'right', color: '#000', backgroundColor: '#fff'}}>
                    <Dropdown overlay={userMenu} overlayStyle={{paddingTop: 25}}>
                        <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<Avatar src={avatar}/>&nbsp;{full_name}</span>
                    </Dropdown>
                </Menu.Item>
            </Menu>
        )

    }

    render() {
        const userinfo = this.state.userinfo;
        const notice = this.state.notice;
        const userMenu = (
            <Menu>
                <Menu.Item>
                    <a href="#" onClick={() => logout()}><Icon type="logout" theme="outlined"/>退出登录</a>
                </Menu.Item>
            </Menu>
        );
        return (
            <Router>
                <Layout>
                    <Sider width={200} style={{background: '#fff', height: '100%'}}>
                        <div className="logo"><img src={logo} style={{marginLeft: '10px'}}/>&nbsp;
                            <div style={{float: 'right', marginTop: '2px', marginRight: '35px', fontSize: '25px'}}>
                                <span>HUNTER</span></div>
                        </div>
                        <Menu
                            mode="inline"
                            defaultSelectedKeys={['0']}
                            theme="dark"
                            style={{height: '100%', borderRight: 0, background: '#283643'}}
                            onClick={({item, key, keyPath}) => {
                                this.setState({key})
                            }}
                        >
                            <Menu.Item key="0" style={{height: 60, paddingLeft: 24, paddingTop: 8}}>
                                <Icon type="form"/><Link style={{display: "inline"}} to={"/taskmanagement"}>任务管理</Link>
                            </Menu.Item>
                            <Menu.Item key="1" style={{height: 60, paddingLeft: 24, paddingTop: 8}}>
                                <Icon type="dashboard"/><Link style={{display: "inline"}} to={"/scanrecords"}>扫描记录</Link>
                            </Menu.Item>
                            <Menu.Item key="2" style={{height: 60, paddingLeft: 24, paddingTop: 8}}>
                                <Icon type="pie-chart"/><Link style={{display: "inline"}} to={"/statics"}><span>统计报表</span></Link>
                            </Menu.Item>
                            <Menu.Item key="3" style={{height: 60, paddingLeft: 24, paddingTop: 8}}>
                                <Icon type="cloud"/><Link style={{display: "inline"}} to={"/client"}><span>用户下载</span></Link>
                            </Menu.Item>
                            <Menu.Item key="4" style={{height: 60, paddingLeft: 24, paddingTop: 8}}>
                                <a href="/doc/" target="_blank"><span><Icon type="file-pdf"/>API文档</span></a>
                            </Menu.Item>
                            {this.showManageMenu(userinfo.role)}
                        </Menu>
                    </Sider>
                    <Layout>
                        <Header className="header" style={{background: '#fff'}}>
                            {this.showAvatarMenu(userinfo.full_name, notice.data)}
                        </Header>
                        <Layout style={{padding: '0 24px 24px'}}>
                            <Content style={{padding: 24, margin: 0, minHeight: 280, overflow: 'auto'}}>
                                <Switch>
                                    <Route path="/taskmanagement" component={UserTaskManagement}/>
                                    <Route path="/client" component={ClientDownloadPage}/>
                                    <Route path="/scanrecords" component={UserScanRecordsTable}/>
                                    <Route path="/scanrecord/:id" component={VulnDetails}/>
                                    <Route path="/statics" component={StaticsChar}/>
                                    <Route path="/manage/users" component={UsersTable}/>
                                    <Route path="/manage/vulnerability" component={VulnTable}/>
                                    <Route path="/manage/task" component={AdminTaskManagement}/>
                                    <Route path="/manage/plugin" component={PluginManagement}/>
                                    <Route path="/manage/setting/" component={SysSetPage}/>
                                    <Route path="/manage/datachart" component={AdminStaticsChar}/>
                                    <Route path="/manage/client" component={ClientManagePage} />
                                    <Route path="/manage/scanrecord/userid/:userid" component={AdminScanRecordTable}/>
                                    <Redirect from="/" to="/taskmanagement"/>
                                </Switch>
                            </Content>
                            <Footer style={{textAlign: 'center'}}>
                                Hunter Design ©2019 Created by Zto Sec
                            </Footer>
                        </Layout>
                    </Layout>
                </Layout>
            </Router>
        )
    }
}