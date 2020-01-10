/**
 * Created by b5mali4 on 2018/8/2.
 */
import React, {Component} from 'react';
import {request, STATUS_CODES} from '../utils/request';
import {Table, Select, Row, Col, Input, Button, Icon, Form, Modal, Dropdown, Menu, message} from 'antd';
import {BrowserRouter as Router, Route, Link, Switch, NavLink} from "react-router-dom";
import '../index.css';
const Option = Select.Option;
const Search = Input.Search;
const FormItem = Form.Item;
const confirm = Modal.confirm;
//子控件改变父控件参考 https://blog.csdn.net/hypocrite_toukaj1/article/details/81096555
/**
 * 用户管理
 */
export default class UsersTable extends Component {

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
        this.setUserList = this.setUserList.bind(this);
    }

    componentWillMount() {
        this.onLoadData();

    };

    //卸载时
    componentWillUnMount() {
        this._isMounted = false;
    };

    async onLoadData() {
        const result = await request("/admin/users/", false);
        if (this._isMounted) {
            this.setState({
                userList: result.data,
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

    setUserList(data) {
        if (this._isMounted) {
            this.setState({
                userList: data
            });
        }
    }


    render() {
        //console.log("UserTable==>render");
        const WrappedUserSearchForm = Form.create()(UserSearchForm);
        const columns = [{
            title: '账户名称',
            dataIndex: 'user_name',
            key: 'user_name',
        }, {
            title: '用户名',
            dataIndex: 'full_name',
            key: 'full_name',
        }, {
            title: '扫描次数',
            dataIndex: 'scan_count',
            key: 'scan_count',
        }, {
            title: '最近操作时间',
            dataIndex: 'recent_operation_time',
            key: 'recent_operation_time',
        }, {
            title: '记录',
            dataIndex: 'task_ids',
            key: 'task_ids',
            render: (text, record) => <Link to={"/manage/scanrecord/userid/" + record.id}>历史列表</Link>
        }, {
            title: '管理操作',
            render: (text, record) => (
                <Row><Col span={12}><UserInfoModal depart_ment={record.depart_ment} email={record.email}
                                                   mobile_phone={record.mobile_phone} role={record.role}
                                                   id={record.id}/></Col><Col
                    span={12}><MoreDropdown/></Col></Row>)
        },];
        return (
            <Row>
                <div style={{background: '#fff'}}>
                    <Row style={{paddingTop: 20, textAlign: 'center'}}>
                        <WrappedUserSearchForm callback={this.setUserList}/>
                    </Row>
                    <Row style={{paddingLeft: 20, paddingRight: 20, marginTop: 20, textAlign: 'center'}}>
                        <Table rowKey={record => record.id} columns={columns} dataSource={this.state.userList}/>
                    </Row>
                </div>

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
            depart_ment: props.depart_ment,
            email: props.email,
            mobile_phone: props.mobile_phone,
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
        await request("/admin/users/" + userId + "/", true, {
            method: 'PUT',
            body: JSON.stringify(values.data)
        });
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
                    okText="确认"
                    cancelText="取消"
                >
                    <WrappedUserInfoModalForm depart_ment={state.depart_ment} email={state.email}
                                              mobile_phone={state.mobile_phone} role={state.role} ref="getFormVlaue"/>
                </Modal>
            </div>
        );
    }
}

/**
 * 编辑更新用户表单
 */
class UserInfoModalForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            depart_ment: props.depart_ment,
            email: props.email,
            mobile_phone: props.mobile_phone,
            role: props.role,
        };
        Object.assign(this.state, this.props);
    }

    render() {
        const {getFieldDecorator} = this.props.form;
        const state = this.state;
        return (
            <Form onSubmit={this.handleSubmit} className="login-form" layout="inline"
                  style={{marginBottom: 25, marginTop: 25}}>
                <Row>
                    <Col span={1}/>
                    <Col span={18}>
                        <FormItem>
                            {getFieldDecorator('data', {
                                initialValue: {
                                    depart_ment: state.depart_ment,
                                    email: state.email,
                                    mobile_phone: state.mobile_phone,
                                    role: state.role
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
            depart_ment: value.depart_ment || "0",
            email: value.email || "",
            mobile_phone: value.mobile_phone || "",
            role: value.role,
        };
    };

    handleMobilePhoneChange = (e) => {
        const mobile_phone = e.target.value;
        if (!('value' in this.props)) {
            this.setState({mobile_phone});
        }
        this.triggerChange({mobile_phone});
    };
    handleEmailChange = (e) => {
        const email = e.target.value;
        if (!('value' in this.props)) {
            this.setState({email});
        }
        this.triggerChange({email});
    };

    handleDepartMentChange = (e) => {
        const depart_ment = e.target.value;
        if (!('value' in this.props)) {
            this.setState({depart_ment});
        }
        this.triggerChange({depart_ment});
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

    /**
     * 根据角色权限展示角色
     */
    getRole(roleId) {
        const roleDict = {"0": "普通用户", "4": "管理员"};
        return roleDict[roleId];
    }

    render() {
        const {size} = this.props;
        const state = this.state;
        const role = this.getRole(state.role);
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
                            value={state.mobile_phone}
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
                            value={state.email}
                            onChange={this.handleEmailChange}
                        />
                    </div>
                </Row>
                <Row>
                    <div className="ant-col-7 ant-form-item-label"><label htmlFor="title"
                                                                          className="ant-form-item-required"
                                                                          title="用户手机">所在部门</label></div>
                    <div className="ant-col-16 ant-form-item-control-wrapper">
                        <Input
                            value={state.depart_ment}
                            size={size}
                            onChange={this.handleDepartMentChange}
                        >
                        </Input>
                    </div>
                </Row>
                <Row>
                    <div className="ant-col-7 ant-form-item-label"><label htmlFor="title"
                                                                          className="ant-form-item-required"
                                                                          title="用户权限">用户权限</label></div>
                    <div className="ant-col-16 ant-form-item-control-wrapper">
                        <Select
                            value={role}
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
 * 搜索用户form表单
 */
class UserSearchForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
        this._isMounted = true;
        Object.assign(this.state, this.props);
    }

    /**
     * 加载数据
     * @param values
     * @returns {Promise.<void>}
     */
    async onLoadData(values) {
        const result = await request("/admin/users/?full_name=" + values.data.fullname + "&role=" + values.data.role);
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

/**
 * 用户搜索表单
 */
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
                <Col span={12}>
                    <Input
                        prefix={<Icon type="user" style={{color: 'rgba(0,0,0,.25)'}}/>}
                        size={size}
                        value={state.fullname}
                        onChange={this.handleFullNameChange}
                    />
                </Col>
                <Col span={12}>
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