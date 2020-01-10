import React, {Component} from 'react';
import {request, STATUS_CODES} from '../utils/request';
import {Col, Row, Collapse, Card, Tooltip, Icon, Form, Input, Button, Checkbox, message, Switch} from 'antd';

const {TextArea} = Input;

/**
 * web设置页面，设置ldap同步账户配置HunterLogSetPage
 */
export default class SysLdapSetPage extends Component {

    render() {
        const WrappedSysLdapBaseSetForm = Form.create({name: 'SysLdapSet'})(SysLdapBaseSetForm);
        return (<Row>
            <Col span={2}/>
            <Col span={20}>
                <Card title="LDAP设置">
                    < WrappedSysLdapBaseSetForm />
                </Card>
            </Col>
            <Col span={2}/>
        </Row>);
    }
}


/**
 * LDAP基础设置表单，发送保存请求
 */
class SysLdapBaseSetForm extends Component {
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
        const result = await request("/admin/setting/ldap/", false);
        this.props.form.setFieldsValue(result.data);
    }

    /**
     * 发送数据
     */
    async putData(values) {
        await request("/admin/setting/ldap/", true, {method: 'PUT', body: JSON.stringify(values)});
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
                <Form.Item label="LDAP服务器" layout="inline">
                    {getFieldDecorator('ldap_host', {
                        rules: [{required: true, message: 'ldap_host is required!'}],
                    })(<Input placeholder="ldap://127.0.0.1"/>)}
                </Form.Item>
                <Form.Item label="BindDN">
                    {getFieldDecorator('ldap_bind_dn', {
                        rules: [{required: true, message: 'ldap_bind_dn is required!'}],
                    })(<Input placeholder="cn=Manager,dc=xxxxx,dc=com"/>)}
                </Form.Item>
                <Form.Item label="BindDN密码">
                    {getFieldDecorator('ldap_bind_dn_password', {
                        rules: [{required: true, message: 'ldap_bind_dn_password is required!'}],
                    })(<Input.Password type="password" placeholder="BindDN密码"/>)}
                </Form.Item>
                <Form.Item label="BaseDN">
                    {getFieldDecorator('ldap_base_dn', {
                        rules: [{required: true, message: 'ldap_base_dn is required!'}],
                    })(<Input placeholder="ou=People,dc=xxx,dc=com"/>)}
                </Form.Item>
                < Form.Item label="Search filter">
                    {getFieldDecorator('ldap_search_filter', {
                        rules: [{required: true, message: 'search filter is required!'}],
                    })(<Input placeholder="(&(objectclass=person)(sAMAccountName={user_name}))"/>)}
                </Form.Item>
                <Form.Item label="账号字段">
                    {getFieldDecorator('ldap_user_name_field', {
                        rules: [{required: true, message: 'ldap_user_name_field is required!'}],
                    })(<Input placeholder="sAMAccountName"/>)}
                </Form.Item>
                <Form.Item label="中文名称">
                    {getFieldDecorator('ldap_full_name_field', {
                        rules: [{required: false, message: 'ldap_full_name_field is required!'}],
                    })(<Input placeholder="displayName"/>)}
                </Form.Item>
                <Form.Item label="邮件字段">
                    {getFieldDecorator('ldap_email_field', {
                        rules: [{required: false, message: 'ldap_email_field is required!'}],
                    })(<Input placeholder="mail"/>)}
                </Form.Item>
                <Form.Item label="部门名称">
                    {getFieldDecorator('ldap_dept_name_field', {
                        rules: [{required: false, message: 'ldap_dept_name_field is required!'}],
                    })(<Input placeholder="dept"/>)}
                </Form.Item>
                <Form.Item label="手机字段">
                    {getFieldDecorator('ldap_mobile_field', {
                        rules: [{required: false, message: 'ldap_mobile_field is required!'}],
                    })(<Input placeholder="dept"/>)}
                </Form.Item>
                <Form.Item label="LDAP认证">
                    {getFieldDecorator('ldap_switch', {valuePropName: 'checked'})(<Switch checkedChildren="是"
                                                                                          unCheckedChildren="否"/>)}

                    <Button type="primary" htmlType="submit" style={{width: '100%'}}>
                        保存设置
                    </Button>
                </Form.Item>
            </Form>
        )
    }

}