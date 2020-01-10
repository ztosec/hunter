import React, {Component} from 'react';
import {request, STATUS_CODES} from '../utils/request';
import {Col, Row, Collapse, Card, Tooltip, Icon, Form, Input, Button, Checkbox, message, Switch} from 'antd';

const {TextArea} = Input;


/**
 * 代理基础设置表单，发送保存请求
 */
export default class SysProxyBaseSetForm extends Component {
    /**
     * 构造
     * @param props
     */
    constructor(props) {
        super(props);
        this._isMounted = true;
        this.state = {
            noticeMessage: '',
            //生成证书按钮
            loading: false,
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
        const result = await request("/admin/setting/proxy/", false);
        this.props.form.setFieldsValue(result.data);
    }

    /**
     * 发送数据
     */
    async putData(values) {
        await request("/admin/setting/proxy/", true, {method: 'PUT', body: JSON.stringify(values)});
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
    /**
     * 生成证书，按钮
     */
    enterLoading = () => {
        this.setState({loading: true});
    };

    render() {
        const {getFieldDecorator} = this.props.form;
        const data = this.state;
        const formItemLayout = {
            labelCol: {
                xs: {span: 8},
                sm: {span: 4},
            },
            wrapperCol: {
                xs: {span: 12},
                sm: {span: 16},
            },
        };
        return (
            <Form onSubmit={this.handleSubmit} {...formItemLayout}>
                <Form.Item label="免认证域名">
                    {getFieldDecorator('white_host_list', {
                        rules: [{required: false, message: 'Please input your white_host_list!'}],
                    })(
                        <TextArea rows={4} placeholder="免认证域名/IP"/>,
                    )}
                </Form.Item>

                <Form.Item label="代理设置">
                    {getFieldDecorator('account_auth_switch', {
                        valuePropName: 'checked',
                        initialValue: true,
                    })(<Checkbox>启用账号认证</Checkbox>)}

                    {getFieldDecorator('ldap_auth_switch', {
                        valuePropName: 'checked',
                        initialValue: true,
                    })(<Checkbox>启用LDAP认证</Checkbox>)}
                    <Button type="primary" htmlType="submit" style={{width: '100%'}}>
                        保存设置
                    </Button>
                </Form.Item>

            </Form>
        )
    }

}