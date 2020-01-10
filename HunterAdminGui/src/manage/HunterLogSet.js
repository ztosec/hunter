/**
 * Created by b5mali4 on 2019/7/31.
 */
import React, {Component} from 'react';
import {Table, Button, Card} from 'antd';
import {request, STATUS_CODES} from '../utils/request';
import {Col, Row, Icon, Layout, Menu, Input, Breadcrumb, Form, Select, message, Switch} from 'antd';
const {SubMenu} = Menu;
const Option = Select.Option;
const FormItem = Form.Item;
const {TextArea} = Input;
const {Header, Content, Footer, Sider} = Layout;

/**
 * 设置SOCKET和配置DNS模块
 */
export default class HunterLogSetPage extends React.Component {

    render() {
        const WrappedSocketSetForm = Form.create({name: 'SocketSetForm'})(SocketSetForm);
        const WrappedDnsServerSetForm = Form.create({name: 'SocketSetForm'})(DnsServerSetForm);
        return (
            <div>
                <Row>
                    <Col span={12}>
                        <Card title="SOCKET服务设置">
                            < WrappedSocketSetForm />
                        </Card>
                    </Col>
                    <Col span={12}>
                        <Card title="DNS服务设置">
                            < WrappedDnsServerSetForm />
                        </Card>
                    </Col>
                </Row>
            </div>
        );
    }
}


/**
 * SocketServer 设置
 */
class SocketSetForm extends React.Component {
    /**
     * 构造
     * @param props
     */
    constructor(props) {
        super(props);
        this._isMounted = true;
        this.state = {
            noticeMessage: '',
        };
    }

    /**
     * 刷新加载时
     */
    componentWillMount() {
        this.onLoadData();

    };

    /**
     * 卸载时
     */
    componentWillUnmount() {
        this._isMounted = false;
    };

    /**
     * 加载数据
     */
    async onLoadData() {
        const result = await request("/admin/setting/hunter_log/socket/", false);
        //console.log(result);
        this.props.form.setFieldsValue(result.data);
    }

    /**
     * 发送数据
     */
    async putData(values) {
        //console.log(values);
        const result = await request("/admin/setting/hunter_log/socket/", true, {method: 'PUT', body: JSON.stringify(values)});
    };

    handleSubmit = e => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            if (!err) {
                console.log('Received values of form: ', values);
                this.putData(values);
            }
        });
    };

    render() {
        const {getFieldDecorator} = this.props.form;
        const data = this.state;
        console.log(data);
        return (
            <Form onSubmit={this.handleSubmit} className="login-form">
                {
                    /*监听的端口 start*/
                }
                <Row>
                    <Form.Item>
                        {getFieldDecorator('hunter_log_socket_host', {
                            rules: [{required: true, message: '请输入hunterLog平台socket模块的ip!'}],
                        })(
                            <Input
                                prefix={<Icon type="shop" style={{color: 'rgba(0,0,0,.25)'}}/>}
                                placeholder="hunter_log socket服务ip"
                            />,
                        )}
                    </Form.Item>
                </Row>
                {
                    /*监听的端口 end*/
                }
                <Row>
                    <Form.Item>
                        {getFieldDecorator('hunter_log_socket_port', {
                            rules: [{required: true, message: '请输入hunterLog平台socket模块监听的端口!'}],
                        })(
                            <Input
                                prefix={<Icon type="rocket" style={{color: 'rgba(0,0,0,.25)'}}/>}
                                placeholder="hunter_log socket端口"
                            />,
                        )}
                    </Form.Item>
                </Row>
                {
                    /* 是否开启 start*/
                }
                <Row>
                    <Form.Item label="开启">
                        {getFieldDecorator('hunter_log_socket_switch', {valuePropName: 'checked'})(<Switch />)}
                    </Form.Item>
                </Row>
                {
                    /* 是否开启 end*/
                }
                <Row>
                    <Form.Item>
                        <Button type="primary" htmlType="submit" style={{width: '100%'}}>
                            提交保存
                        </Button>
                    </Form.Item>
                </Row>
            </Form>
        )
    }

}

/**
 * DnsServer 设置
 */
class DnsServerSetForm extends React.Component {
    /**
     * 构造
     * @param props
     */
    constructor(props) {
        super(props);
        this._isMounted = true;
        this.state = {
            noticeMessage: '',
        };
    }

    /**
     * 刷新加载时
     */
    componentWillMount() {
        this.onLoadData();

    };

    /**
     * 卸载时
     */
    componentWillUnmount() {
        this._isMounted = false;
    };

    /**
     * 加载数据
     */
    async onLoadData() {
        const result = await request("/admin/setting/hunter_log/dns/", false);
        this.props.form.setFieldsValue(result.data);
    }

    /**
     * 发送数据
     */
    async putData(values) {
        const result = await request("/admin/setting/hunter_log/dns/", true, {method: 'PUT', body: JSON.stringify(values)});
    };

    handleSubmit = e => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            if (!err) {
                console.log('Received values of form: ', values);
                this.putData(values);
            }
        });
    };

    render() {
        const {getFieldDecorator} = this.props.form;
        const data = this.state;
        console.log(data);
        return (
                        <Form onSubmit={this.handleSubmit} className="login-form">
                {
                    /*dns模块的hunter_log_dns_fake_root_domain start*/
                }
                <Row>
                    <Form.Item>
                        {getFieldDecorator('hunter_log_dns_fake_root_domain', {
                            rules: [{required: true, message: '请输入hunterLog平台dns模块的用于无回显的域名!'}],
                        })(
                            <Input
                                prefix={<Icon type="shop" style={{color: 'rgba(0,0,0,.25)'}}/>}
                                placeholder="hunter_log dns服务无回显的域名"
                            />,
                        )}
                    </Form.Item>
                </Row>
                {
                    /*dns模块的hunter_log_dns_fake_root_domain end*/
                }
                <Row>
                    <Form.Item>
                        {getFieldDecorator('hunter_api_url', {
                            rules: [{required: true, message: '请输入hunterLog平台api检测接口'}],
                        })(
                            <Input
                                prefix={<Icon type="rocket" style={{color: 'rgba(0,0,0,.25)'}}/>}
                                placeholder="hunter_log socket端口"
                            />,
                        )}
                    </Form.Item>
                </Row>
                {
                    /* 是否开启 start*/
                }
                <Row>
                    <Form.Item label="开启">
                        {getFieldDecorator('hunter_log_dns_switch', {valuePropName: 'checked'})(<Switch />)}
                    </Form.Item>
                </Row>
                {
                    /* 是否开启 end*/
                }
                <Row>
                    <Form.Item>
                        <Button type="primary" htmlType="submit" style={{width: '100%'}}>
                            提交保存
                        </Button>
                    </Form.Item>
                </Row>
            </Form>
        )
    }

}