/**
 * Created by b5mali4 on 2019/7/30.
 */
import Logo from './assets/logo.png';
import React, {Component} from 'react';
import {request, STATUS_CODES} from './utils/request';
import {Col, Row, Collapse, Card, Tooltip, message, Form, Input, Button, Checkbox, Icon, Tabs} from 'antd';
const {TabPane} = Tabs;

export default class LoginPage extends React.Component {
    render() {
        const WrappedNormalLoginForm = Form.create({name: 'normal_login'})(NormalLoginForm);
        const WrappedLdapLoginForm = Form.create({name: 'normal_login'})(LdapLoginForm);
        return (
            <div id="main">
                <Row style={{"padding": "50px 0 24px"}}>
                    <div id="login-top">
                        <a href="/">
                            <img src={Logo}
                                 style={{'height': '44px', 'margin-right': '16px', 'vertical-align': 'top'}}/>
                            <span style={{
                                position: "relative",
                                "top": "2px",
                                "color": "rgba(0, 0, 0, .85)",
                                "font-weight": "600",
                                "font-size": "33px",
                                "font-family": "Avenir, Helvetica Neue, Arial, Helvetica, sans-serif;"
                            }}>HUNTER</span>
                        </a>
                        <div style={{
                            "margin-top": "12px",
                            "margin-bottom": "40px",
                            "color": "rgba(0,0,0,.45)",
                            "font-size": "14px"
                        }}>HUNTER,离您最近的安全专家
                        </div>
                    </div>
                    <div id="login-main">
                        <Col span={8}/>
                        <Col span={8}>
                            <Tabs defaultActiveKey="1">
                                <TabPane tab="默认" key="1">
                                    <WrappedNormalLoginForm/>
                                </TabPane>
                                <TabPane tab="LDAP" key="2">
                                    <WrappedLdapLoginForm/>
                                </TabPane>
                            </Tabs>
                        </Col>
                        <Col span={8}/>
                    </div>
                </Row>
            </div>
        )
    }
}

/**
 * 默认的账号密码登录模块，使用数据库账号密码登录
 */
class NormalLoginForm extends React.Component {
    handleSubmit = e => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            if (!err) {
                this.login(values);
                //console.log('Received values of form: ', values);
            }
        });
    };

    /**
     * 登录
     * @returns {Promise.<void>}
     * @constructor
     */
    async login(values) {
        const options = {
            method: "POST",
            body: JSON.stringify(values),
            headers: {"Content-Type": "application/json"},
        };
        await request("/account/login/", true, options);
    };

    render() {
        const {getFieldDecorator} = this.props.form;
        return (
            <Form onSubmit={this.handleSubmit} className="login-form">
                <Form.Item>
                    {getFieldDecorator('user_name', {
                        rules: [{required: true, message: 'Please input your username!'}],
                    })(
                        <Input
                            prefix={<Icon type="user" style={{color: 'rgba(0,0,0,.25)'}}/>}
                            placeholder="Username"
                        />,
                    )}
                </Form.Item>
                <Form.Item>
                    {getFieldDecorator('pass_word', {
                        rules: [{required: true, message: 'Please input your Password!'}],
                    })(
                        <Input
                            prefix={<Icon type="lock" style={{color: 'rgba(0,0,0,.25)'}}/>}
                            type="password"
                            placeholder="Password"
                        />,
                    )}
                </Form.Item>
                <Form.Item>
                    <Button type="primary" htmlType="submit" className="login-form-button" style={{width: "100%"}}>
                        Log in
                    </Button>
                </Form.Item>
            </Form>
        );
    }
}

/**
 * ldap账号密码登录模块，使用ldap账号密码登录
 */
class LdapLoginForm extends React.Component {
    handleSubmit = e => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            if (!err) {
                this.login(values);
                //console.log('Received values of form: ', values);
            }
        });
    };

    /**
     * 登录
     * @returns {Promise.<void>}
     * @constructor
     */
    async login(values) {
        const options = {
            method: "POST",
            body: JSON.stringify(values),
            headers: {"Content-Type": "application/json"},
        };
        await request("/ldap/login/", true, options);
    };

    render() {
        const {getFieldDecorator} = this.props.form;
        return (
            <Form onSubmit={this.handleSubmit} className="login-form">
                <Form.Item>
                    {getFieldDecorator('user_name', {
                        rules: [{required: true, message: 'Please input your username!'}],
                    })(
                        <Input
                            prefix={<Icon type="user" style={{color: 'rgba(0,0,0,.25)'}}/>}
                            placeholder="Username"
                        />,
                    )}
                </Form.Item>
                <Form.Item>
                    {getFieldDecorator('pass_word', {
                        rules: [{required: true, message: 'Please input your Password!'}],
                    })(
                        <Input
                            prefix={<Icon type="lock" style={{color: 'rgba(0,0,0,.25)'}}/>}
                            type="password"
                            placeholder="Password"
                        />,
                    )}
                </Form.Item>
                <Form.Item>
                    <Button type="primary" htmlType="submit" className="login-form-button" style={{width: "100%"}}>
                        Log in
                    </Button>
                </Form.Item>
            </Form>
        );
    }
}