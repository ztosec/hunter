import React, {Component} from 'react';
import {request, STATUS_CODES} from '../utils/request';
import {Col, Row, Collapse, Card, Tooltip, Icon, Form, Input, Button, Checkbox, message} from 'antd';

const {TextArea} = Input;

/**
 * web设置页面，设置邮箱配置表单
 */
export default class SysEmailSetForm extends Component {

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
        const result = await request("/admin/setting/email/", false);
        this.props.form.setFieldsValue(result.data);
    }

    /**
     * 发送数据
     */
    async putData(values) {
        await request("/admin/setting/email/", true, {method: 'PUT', body: JSON.stringify(values)});
    };

    handleSubmit = e => {
        //e.preventDefault();
        this.props.form.validateFields((err, values) => {
            console.log("SysEmailSetForm，Received");
            if (!err) {
                console.log('Received values of form: ', values);
                this.putData(values);
            }
        });
    };

    render() {
        const {getFieldDecorator} = this.props.form;
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
                {
                    /* 邮件配置信息 start*/
                }
                <Form.Item label="smtp服务器">
                    {getFieldDecorator('smtp_host', {
                        rules: [{required: true, message: 'Please input smtp host!'}],
                    })(
                        <Input
                            prefix={<Icon type="shop" style={{color: 'rgba(0,0,0,.25)'}}/>}
                            type="text"
                            placeholder="smtp服务器"
                        />,
                    )}
                </Form.Item>
                <Form.Item label="smtp端口">
                    {getFieldDecorator('smtp_port', {
                        rules: [{required: true, message: 'Please input smtp port!'}],
                    })(
                        <Input
                            prefix={<Icon type="rocket" style={{color: 'rgba(0,0,0,.25)'}}/>}
                            type="text"
                            placeholder="smtp端口"
                        />,
                    )}
                </Form.Item>
                <Form.Item label="发件邮箱">
                    {getFieldDecorator('sender_email', {
                        rules: [{required: true, message: 'Please input your email!'}],
                    })(
                        <Input
                            prefix={<Icon type="mail" style={{color: 'rgba(0,0,0,.25)'}}/>}
                            type="text"
                            placeholder="邮箱"
                        />,
                    )}
                </Form.Item>
                <Form.Item label="发件邮箱密码">
                    {getFieldDecorator('sender_password', {
                        rules: [{required: true, message: 'Please input your Password!'}],
                    })(
                        <Input.Password
                            prefix={<Icon type="lock" style={{color: 'rgba(0,0,0,.25)'}}/>}
                            type="password"
                            placeholder="邮箱密码"
                        />,
                    )}
                    <Button type="primary" htmlType="submit" style={{width: '100%'}}>
                        提交保存
                    </Button>
                </Form.Item>
                {
                    /* 邮件配置信息 end*/
                }
            </Form>
        )
    }

}