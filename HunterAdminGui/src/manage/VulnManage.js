/**
 * Created by b5mali4 on 2018/8/2.
 */
import React, {Component} from 'react';
import {request, STATUS_CODES} from '../utils/request';
import {Table, Select, Row, Col, Input, Button, Icon, Form, Modal, Dropdown, Menu, message} from 'antd';
import {BrowserRouter as Router, Route, Link, Switch, NavLink} from "react-router-dom";
import '../index.css';
//import Form from "antd/es/form/Form.d";
//import FormItem from "antd/es/form/FormItem.d";
const Option = Select.Option;
const Search = Input.Search;
const FormItem = Form.Item;
const confirm = Modal.confirm;
//子控件改变父控件参考 https://blog.csdn.net/hypocrite_toukaj1/article/details/81096555
/**
 * 漏洞管理
 */
export default class VulnTable extends Component {

    constructor(props) {
        super(props);
        this._isMounted = true;
        this.state = {
            filterDropdownVisible: false,
            data: [],
            searchText: '',
            filtered: false,
        };
        Object.assign(this.state, this.props);
        this.setVulnList = this.setVulnList.bind(this);
    }

    componentWillMount() {
        this.onLoadData();

    };

    //卸载时
    componentWillUnMount() {
        this._isMounted = false;
    };

    async onLoadData() {
        const result = await request("/admin/vulnerabilitys/");
        if (this._isMounted) {
            this.setState({
                vulnList: result.data,
            });
        }

    };

    handleSubmit = (e) => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            if (!err) {
                console.log('Received values of form: ', values);
            }
        });
    }

    setVulnList(data) {
        if (this._isMounted) {
            this.setState({
                vulnList: data
            });
        }
    }


    render() {
        //console.log("UserTable==>render");
        //const WrappedVulnSearchForm = Form.create()(VulnSearchForm);
        const columns = [{
            title: 'ID',
            dataIndex: 'id',
            key: 'id',
        }, {
            title: '漏洞标题',
            dataIndex: 'info',
            key: 'info',
        }, {
            title: '漏洞类型',
            dataIndex: 'type',
            key: 'type',
        }, {
            title: '危害等级',
            dataIndex: 'level',
            key: 'level',
        }, {
            title: '任务记录',
            dataIndex: 'task_id',
            key: 'task_id',
            render: (text, record) => <Link to={"/scanrecord/" + record.task_id}>扫描任务</Link>
        }];
        return (
            <Row>
                <div style={{background: '#fff'}}>
                    <Row style={{paddingTop: 20, textAlign: 'center'}}>
                        {
                            //<WrappedVulnSearchForm callback={this.setVulnList}/>
                        }
                    </Row>
                    <Row style={{paddingLeft: 20, paddingRight: 20, marginTop: 20, textAlign: 'center'}}>
                        <Table rowKey={record => record.id} columns={columns} dataSource={this.state.vulnList}/>
                    </Row>
                </div>

            </Row>
        );
    }
}

/**
 * 搜索form表单
 */
class VulnSearchForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
        this._isMounted = true;
        Object.assign(this.state, this.props);
    }

    async onLoadData(values) {
        const result = await request("/admin/users/?fullname=" + values.data.fullname + "&role=" + values.data.role);
        this.props.callback(result.data);
        if (this._isMounted) {
            this.setState({
                userList: result.data
            });
        }


    };

    componentWillUnmount() {
        this._isMounted = false;
    };


    handleSubmit = (e) => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            if (!err) {
                this.onLoadData(values)
            }
        });
    };
    handleReset = () => {
        this.props.form.resetFields();
    };

    render() {
        const {getFieldDecorator} = this.props.form;
        return (
            <Form onSubmit={this.handleSubmit} className="login-form" layout="inline">
                <Row>
                    <Col span={1}/>
                    <Col span={18}>
                        <FormItem>
                            {getFieldDecorator('data', {
                                initialValue: {fullname: "", department: "", role: ""},
                            })(<UserSearchFormDataInput />)}
                        </FormItem>
                    </Col>
                    <Col span={4}>
                        <FormItem>
                            <Button type="primary" htmlType="submit">查询</Button>&nbsp;&nbsp;
                            <Button onClick={this.handleReset}>重置</Button>
                        </FormItem>
                    </Col>
                    <Col span={1}/>
                </Row>
            </Form>
        );
    }
}

class UserSearchFormDataInput extends React.Component {

    static getDerivedStateFromProps(nextProps) {
        // Should be a controlled component.
        if ('value' in nextProps) {
            return {
                ...(nextProps.value || {}),
            };
        }
        return null;
    }

    constructor(props) {
        super(props);

        const value = props.value || {};
        this.state = {
            fullname: value.fullname || "",
            department: value.department || "",
            role: value.role || "",
        };
    };

    handleFullNameChange = (e) => {
        const fullname = e.target.value;
        if (!('value' in this.props)) {
            this.setState({fullname});
        }
        this.triggerChange({fullname});
    };

    handleDepartMentChange = (department) => {
        if (!('value' in this.props)) {
            this.setState({department});
        }
        this.triggerChange({department});
    };

    handleRoleChange = (role) => {
        if (!('value' in this.props)) {
            this.setState({role});
        }
        this.triggerChange({role});
    };


    triggerChange = (changedValue) => {
        // Should provide an event to pass value to Form.
        const onChange = this.props.onChange;
        if (onChange) {
            onChange(Object.assign({}, this.state, changedValue));
        }
    };

    render() {
        const {size} = this.props;
        const state = this.state;
        return (
            <Row>
                <Col span={8}>
                    <Input
                        prefix={<Icon type="user" style={{color: 'rgba(0,0,0,.25)'}}/>}
                        size={size}
                        value={state.fullname}
                        onChange={this.handleFullNameChange}
                    />
                </Col>
                <Col span={8}>
                    <Select
                        value={state.department}
                        size={size}
                        style={{width: 200}}
                        onChange={this.handleDepartMentChange}
                    >
                        <Option value="">默认</Option>
                        <Option value="0">信息安全部</Option>
                        <Option value="1">应用平台部</Option>
                    </Select>
                </Col>
                <Col span={8}>
                    <Select
                        value={state.role}
                        size={size}
                        style={{width: 200}}
                        onChange={this.handleRoleChange}
                    >
                        <Option value="">默认</Option>
                        <Option value="0">普通用户</Option>
                        <Option value="4">管理员</Option>
                    </Select>
                </Col>
            </Row>
        );
    }
}

/**
 * 操作中编辑用户资料，用于更改默认没有部门的情况
 */
class UserInfoModal extends Component {
    constructor(props) {
        super(props);
        this.state = {
            visible: false,
            department: props.department,
            emails: props.emails,
            mobilePhone: props.mobilePhone,
            role: props.role,
            id: props.id,
        };
    };

    showModal = () => {
        this.setState({
            visible: true,
        });
    };

    handleOk = (e) => {
        console.log(e);
        this.setState({
            visible: false,
        });
        //这里调用提交表单的回调函数，UserInfoModalForm组件中
        console.log("提交了表单哦");
        let form = this.refs.getFormVlaue;//通过refs属性可以获得对话框内form对象
        form.validateFields((err, values) => {
            if (!err) {
                //console.log(values);//这里可以拿到数据
                this.changeUserInfo(this.state.id, values)
            }
        });
    };

    async changeUserInfo(userId, values) {
        const result = await request("/admin/users/" + userId + "/", {
            method: 'PUT',
            body: JSON.stringify(values.data)
        });
        if (result !== undefined) {
            if (result.status == STATUS_CODES.HTTP_OK) {
                message.success(result.message);
            } else if (result.status == STATUS_CODES.HTTP_BAD_REQUEST) {
                message.error(result.message + "," + result.extra_info);
            } else if (result.status == STATUS_CODES.HTTP_INTERNAL_SERVER_ERROR) {
                message.error(result.message);
            }
        }
    };

    handleCancel = (e) => {
        console.log(e);
        this.setState({
            visible: false,
        });
    }

    render() {
        const state = this.state;
        const WrappedUserInfoModalForm = Form.create()(UserInfoModalForm);
        return (
            <div>
                <a onClick={this.showModal}>编辑</a>
                <Modal
                    title="编辑用户信息"
                    visible={this.state.visible}
                    onOk={this.handleOk}
                    onCancel={this.handleCancel}
                    width="40%"
                >
                    <WrappedUserInfoModalForm department={state.department} emails={state.emails}
                                              mobilePhone={state.mobilePhone} role={state.role} ref="getFormVlaue"/>
                </Modal>
            </div>
        );
    }

}


/**
 * 操作中更多
 */
class MoreDropdown extends Component {
    constructor(props) {
        super(props)
    }

    /**
     * 拉黑用户对话框
     */
    pullBlackConfirm() {
        confirm({
            title: '拉黑用户',
            content: '确认要拉黑该用户吗?',
            okText: '确认',
            okType: 'danger',
            cancelText: '取消',
            onOk() {
                console.log('OK');
            },
            onCancel() {
                console.log('Cancel');
            },
        });
    }

    /**
     * 加白用户对话框
     */
    addWhiteConfirm() {
        confirm({
            title: '加白用户',
            content: '确认要加白该用户吗?',
            okText: '确认',
            cancelText: '取消',
            onOk() {
                console.log('OK');
            },
            onCancel() {
                console.log('Cancel');
            },
        });
    }


    render() {
        const menu = (
            <Menu>
                <Menu.Item>
                    <a target="_blank" onClick={this.pullBlackConfirm}>拉黑</a>
                </Menu.Item>
                <Menu.Item>
                    <a target="_blank" onClick={this.addWhiteConfirm}>加白</a>
                </Menu.Item>
            </Menu>
        );
        return (
            <Dropdown overlay={menu}>
                <a className="ant-dropdown-link" href="#">
                    更多 <Icon type="down"/>
                </a>
            </Dropdown>
        );
    }

}

/**
 * 编辑用户信息的form表单，出现在对话框中
 */
class UserInfoModalForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            department: props.department,
            emails: props.emails,
            mobilePhone: props.mobilePhone,
            role: props.role,
        };
        Object.assign(this.state, this.props);
    }

    async onLoadData(values) {
        const result = await request("/admin/users/?fullname=" + values.data.fullname + "&role=" + values.data.role);
        console.log(result);
        console.log(result.data);
        this.props.callback(result.data);
        console.log('Received values of form: ', values);
        this.setState({
            userList: result.data
        });

    };

    handleSubmit = (e) => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            if (!err) {
                //发送查询用户API
                //const result = request("/admin/users/?fullname="+values.data.fullname+"&department=" + values.data.department +"&role=" + values.data.role);
                //const result = await request("/admin/users/?fullname=" + values.data.fullname + "&role=" + values.data.role);
                this.onLoadData(values)
            }
        });
    };
    handleReset = () => {
        this.props.form.resetFields();
    };

    render() {
        const state = this.state;
        var role = "普通用户";
        if (state.role == "0") {
            role = "普通用户";
        } else if (state.role == "4") {
            role = "管理员";
        }
        const {getFieldDecorator} = this.props.form;
        return (
            <Form onSubmit={this.handleSubmit} className="login-form" layout="inline"
                  style={{marginBottom: 25, marginTop: 25}}>
                <Row>
                    <Col span={1}/>
                    <Col span={18}>
                        <FormItem>
                            {getFieldDecorator('data', {
                                initialValue: {
                                    department: state.department,
                                    emails: state.emails,
                                    mobilephone: state.mobilePhone,
                                    role: role
                                },
                            })(<UserInfoModalFormDataInput />)}
                        </FormItem>
                    </Col>
                    <Col span={1}/>
                </Row>
            </Form>
        );
    }
}
/**
 * 编辑用户表单的输入
 */
class UserInfoModalFormDataInput extends React.Component {

    static getDerivedStateFromProps(nextProps) {
        // Should be a controlled component.
        if ('value' in nextProps) {
            return {
                ...(nextProps.value || {}),
            };
        }
        return null;
    }

    constructor(props) {
        super(props);
        const value = props.value || {};
        //console.log(props);
        this.state = {
            department: value.department || "0",
            emails: value.emails || "",
            mobilephone: value.mobilephone || "",
            role: value.role,
        };
    };

    handleMobilePhoneChange = (e) => {
        const mobilephone = e.target.value;
        if (!('value' in this.props)) {
            this.setState({mobilephone});
        }
        this.triggerChange({mobilephone});
    };
    handleEmailsChange = (e) => {
        const emails = e.target.value;
        if (!('value' in this.props)) {
            this.setState({emails});
        }
        this.triggerChange({emails});
    };

    handleDepartMentChange = (department) => {
        if (!('value' in this.props)) {
            this.setState({department});
        }
        this.triggerChange({department});
    };

    handleRoleChange = (role) => {
        if (!('value' in this.props)) {
            this.setState({role});
        }
        this.triggerChange({role});
    };


    triggerChange = (changedValue) => {
        // Should provide an event to pass value to Form.
        const onChange = this.props.onChange;
        if (onChange) {
            onChange(Object.assign({}, this.state, changedValue));
        }
    };

    render() {
        const {size} = this.props;
        const state = this.state;
        return (
            <Row>
                <Row>
                    <div className="ant-col-7 ant-form-item-label"><label htmlFor="title"
                                                                          className="ant-form-item-required"
                                                                          title="用户手机">用户手机</label></div>
                    <div className="ant-col-16 ant-form-item-control-wrapper">
                        <Input
                            prefix={<Icon type="mobile" style={{color: 'rgba(0,0,0,.25)'}}/>}
                            size={size}
                            value={state.mobilephone}
                            onChange={this.handleMobilePhoneChange}
                        />
                    </div>
                </Row>
                <Row>
                    <div className="ant-col-7 ant-form-item-label"><label htmlFor="title"
                                                                          className="ant-form-item-required"
                                                                          title="用户邮箱">用户邮箱</label></div>
                    <div className="ant-col-16 ant-form-item-control-wrapper">
                        <Input
                            prefix={<Icon type="mail" style={{color: 'rgba(0,0,0,.25)'}}/>}
                            value={state.emails}
                            onChange={this.handleEmailsChange}
                        />
                    </div>
                </Row>
                <Row>
                    <div className="ant-col-7 ant-form-item-label"><label htmlFor="title"
                                                                          className="ant-form-item-required"
                                                                          title="用户手机">所在部门</label></div>
                    <div className="ant-col-16 ant-form-item-control-wrapper">
                        <Select
                            value={state.department}
                            size={size}
                            onChange={this.handleDepartMentChange}
                        >
                            <Option value="0">信息安全部</Option>
                            <Option value="1">应用平台部</Option>
                        </Select>
                    </div>
                </Row>
                <Row>
                    <div className="ant-col-7 ant-form-item-label"><label htmlFor="title"
                                                                          className="ant-form-item-required"
                                                                          title="用户权限">用户权限</label></div>
                    <div className="ant-col-16 ant-form-item-control-wrapper">
                        <Select
                            value={state.role}
                            size={size}
                            onChange={this.handleRoleChange}
                        >
                            <Option value="0">普通用户</Option>
                            <Option value="4">管理员</Option>
                        </Select>
                    </div>
                </Row>
            </Row>
        );
    }
}
