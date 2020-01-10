/**
 * Created by b5mali4 on 2018/8/2.
 */
import React, {Component} from 'react';
import {request, STATUS_CODES} from '../utils/request';
import {Table, Select, Row, Col, Input, Button, Icon, Form, Modal, Dropdown, Menu, message, Progress} from 'antd';
import {BrowserRouter as Router, Route, Link, Switch, NavLink} from "react-router-dom";
import '../index.css';
const Option = Select.Option;
const Search = Input.Search;
const FormItem = Form.Item;
const confirm = Modal.confirm;
//子控件改变父控件参考 https://blog.csdn.net/hypocrite_toukaj1/article/details/81096555
/**
 * 管理员任务管理，用于结束某些任务
 */
export default class AdminTaskManagement extends Component {

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
        //this.setUserList = this.setUserList.bind(this);
        this.setTaskInfoList = this.setTaskInfoList.bind(this);
    }

    componentWillMount() {
        this.onLoadData();

    };

    //卸载时
    componentWillUnMount() {
        this._isMounted = false;
    };

    async onLoadData() {
        const result = await request("/admin/tasks/", false);
        if (this._isMounted) {
            this.setState({
                taskInfoList: result.data,
                //userList: result.data,
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

    setTaskInfoList(data) {
        if (this._isMounted) {
            this.setState({
                taskInfoList: data
            });
        }
    }


    render() {
        const WrappedTaskSearchForm = Form.create()(TaskSearchForm);
        const columns = [
            {
                title: 'ID',
                dataIndex: 'task_id',
                key: 'task_id',
            }, {
                title: '任务名',
                dataIndex: 'task_name',
                key: 'task_name',
            }, {
                title: 'Owner',
                dataIndex: 'create_user_name',
                key: 'create_user_name',
            }, {
                title: '开始时间',
                dataIndex: 'create_time',
                key: 'create_time',
            }, {
                title: '扫描状态',
                render: (value, row, index) => (
                    <TaskStatusModal index={index} taskStatus={value.task_status}></TaskStatusModal>
                ),
                key: 'task_status',
            }, {
                title: '扫描进度',
                render: (text, recode) => (
                    <div style={{width: 170}}><Progress percent={recode.percent} size="small" status="active"/></div>
                ),
                key: 'percent',
            }, {
                title: '管理操作',
                render: (text, record) => (
                    <Row>
                        <Col span={12}><TaskInfoModal hook_rule={record.hook_rule}
                                                      receiver_emails={record.receiver_emails}
                                                      task_name={record.task_name} task_id={record.task_id}/></Col>
                        <Col span={12}><MoreDropdown task_id={record.task_id}/></Col>
                    </Row>)
            },];
        return (
            <Row>
                <div style={{background: '#fff'}}>
                    <Row style={{paddingTop: 20, textAlign: 'center'}}>
                        <WrappedTaskSearchForm callback={this.setTaskInfoList}/>
                    </Row>
                    <Row style={{paddingLeft: 20, paddingRight: 20, marginTop: 20, textAlign: 'center'}}>
                        <Table rowKey={record => record.task_id} columns={columns}
                               dataSource={this.state.taskInfoList}/>
                    </Row>
                </div>

            </Row>
        );
    }
}

/**
 * 任务状态
 */
class TaskStatusModal extends Component {
    constructor(props) {
        super(props)
        this.props = props;
    }

    render() {
        const taskStatus = this.props.taskStatus;
        const index = this.props.index;
        //默认第一个前端才显示运行中，后面都显示待运行
        if (taskStatus === 0) {
            return <div>等待中</div>;
        } else if(taskStatus === 1){
            return <div>扫描中</div>;
        } else if (taskStatus === 3) {
            return <div>任务被关闭</div>
        } else if (taskStatus === 2) {
            return <div>扫描结束</div>
        }
    }
}

/**
 * 编辑任务
 * hook_rule={record.hook_rule}
 * receiver_emails={record.receiver_emails}
 * task_name={record.task_name}
 * task_id={record.task_id}
 */
class TaskInfoModal extends Component {
    constructor(props) {
        super(props);
        this.state = {
            visible: false,
            hookRule: props.hook_rule,
            receiverEmails: props.receiver_emails,
            taskName: props.task_name,
            taskId: props.task_id,
        };

    };

    showModal = () => {
        this.setState({
            visible: true,
        });
    };

    handleOk = (e) => {
        //console.log(e);
        this.setState({
            visible: false,
        });
        //这里调用提交表单的回调函数，UserInfoModalForm组件中
        console.log("更新hookurl提交了表单哦");
        let demo = this.refs.getFormVlaue;//通过refs属性可以获得对话框内form对象
        demo.validateFields((err, values) => {
            if (!err) {
                //console.log(values);//这里可以拿到数据
                this.changeTaskHookRule(values.data.taskId, values.data.hookRule)
            }
        });
    };

    async changeTaskHookRule(taskId, hookRule) {
        await request('/admin/tasks/', true, {
            method: "PUT",
            body: JSON.stringify({"task_id": taskId, "hook_rule": hookRule})
        });
    };

    handleCancel = (e) => {
        this.setState({
            visible: false,
        });
    };

    render() {
        const state = this.state;
        const WrappedTaskInfoModalForm = Form.create()(TaskInfoModalForm);
        return (
            <div>
                <a onClick={this.showModal}>编辑</a>
                <Modal
                    title="编辑任务信息"
                    visible={this.state.visible}
                    onOk={this.handleOk}
                    onCancel={this.handleCancel}
                    width="40%"
                >
                    <WrappedTaskInfoModalForm hookRule={state.hookRule} receiverEmails={state.receiverEmails}
                                              taskName={state.taskName} taskId={state.taskId} disabled={true}
                                              ref="getFormVlaue"/>
                </Modal>
            </div>
        );
    }

}
/**
 * 编辑任务信息的form表单，出现在对话框中
 */
class TaskInfoModalForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            hookRule: props.hookRule,
            receiverEmails: props.receiverEmails,
            taskName: props.taskName,
            taskId: props.taskId,
            disabled: props.disabled,
        };
        Object.assign(this.state, this.props);
    }

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
        const state = this.state;
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
                                    hookRule: state.hookRule,
                                    receiverEmails: state.receiverEmails,
                                    taskName: state.taskName,
                                    taskId: state.taskId,
                                    disabled: state.disabled,
                                },
                            })(<TaskInfoModalFormDataInput />)}
                        </FormItem>
                    </Col>
                    <Col span={1}/>
                </Row>
            </Form>
        );
    }
}

/**
 * 编辑任务表单的输入
 */
class TaskInfoModalFormDataInput extends React.Component {

    static getDerivedStateFromProps(nextProps) {
        // Should be a controlled component.
        if ('value' in nextProps) {
            return {
                ...(nextProps.value || {}),
            };
        }
        return null;
    }

    /**
     *  hookrule: state.hook_rule
     *  receiveremails: state.receiver_emails
     *  taskname: state.task_name
     *  taskid: state.task_id,
     * @param props
     */
    constructor(props) {
        super(props);
        const value = props.value || {};
        this.state = {
            hookRule: value.hookRule || "0",
            receiverEmails: value.receiverEmails || "",
            taskName: value.taskName || "",
            taskId: value.taskId,
            disabled: value.disabled,
        };
    };

    handleHookRuleChange = (e) => {
        const hookRule = e.target.value;
        if (!('value' in this.props)) {
            this.setState({hookRule});
        }
        this.triggerChange({hookRule});
    };
    handleReceiverEmailsChange = (e) => {
        const receiverEmails = e.target.value;
        if (!('value' in this.props)) {
            this.setState({receiverEmails});
        }
        this.triggerChange({receiverEmails});
    };

    handleTaskNameChange = (e) => {
        const taskName = e.target.value;
        if (!('value' in this.props)) {
            this.setState({taskName});
        }
        this.triggerChange({taskName});
    };
    handleTaskIdChange = (e) => {
        const taskId = e.target.value;
        if (!('value' in this.props)) {
            this.setState({taskId});
        }
        this.triggerChange({taskId});
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
                    <div className="ant-col-7 ant-form-item-label">
                        <label htmlFor="title" className="ant-form-item-required" title="网址正则">网址正则</label></div>
                    <div className="ant-col-16 ant-form-item-control-wrapper">
                        <Input
                            prefix={<Icon type="code" style={{color: 'rgba(0,0,0,.25)'}}/>}
                            size={size}
                            value={state.hookRule}
                            onChange={this.handleHookRuleChange}
                        />
                    </div>
                </Row>
                <Row>
                    <div className="ant-col-7 ant-form-item-label">
                        <label htmlFor="title" title="发送邮箱">发送邮箱</label></div>
                    <div className="ant-col-16 ant-form-item-control-wrapper">
                        <Input
                            disabled={state.disabled}
                            prefix={<Icon type="mail" style={{color: 'rgba(0,0,0,.25)'}}/>}
                            value={state.receiverEmails}
                            onChange={this.handleReceiverEmailsChange}
                        />
                    </div>
                </Row>
                <Row>
                    <div className="ant-col-7 ant-form-item-label"><label htmlFor="title"
                                                                          className="ant-form-item-required"
                                                                          title="任务名称">任务名称</label></div>
                    <div className="ant-col-16 ant-form-item-control-wrapper">
                        <Input
                            disabled={state.disabled}
                            prefix={<Icon type="flag" style={{color: 'rgba(0,0,0,.25)'}}/>}
                            value={state.taskName}
                            onChange={this.handleTaskNameChange}
                        />
                    </div>
                </Row>
            </Row>
        );
    }
}

/**
 * 任务管理下拉列表
 */
class MoreDropdown extends Component {
    state = {visible: false};

    showModal = () => {
        this.setState({
            visible: true,
        });
    };

    constructor(props) {
        super(props)
        this.props = props;
    }

    /**
     * 结束任务对话框
     */
    stopTaskConfirm(taskId) {
        if (taskId != undefined) {
            confirm({
                title: '结束任务',
                content: '确认要结束该任务吗?',
                okText: '确认',
                okType: 'danger',
                cancelText: '取消',
                onOk() {
                    sentStopTask(taskId);
                    //console.log('启动结束任务');
                },
                onCancel() {
                    //console.log('取消结束任务');
                },
            })
        };
        var sentStopTask = async function (taskId) {
            await request("/admin/tasks/", true, {method: "DELETE", body: JSON.stringify({"task_id": taskId})});
        };

    }


    render() {
        const taskId = this.props.task_id;
        const menu = (
            <Menu>
                <Menu.Item>
                    <a target="_blank" onClick={() => this.stopTaskConfirm(this.props.task_id)}>结束</a>
                </Menu.Item>
                <Menu.Item>
                    <Link to={"/scanrecord/" + taskId}>查看</Link>
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
 * 搜索任务form表单
 */
class TaskSearchForm extends React.Component {
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
        const result = await request("/admin/tasks/?task_id=" + values.data.task_id + "&status=" + values.data.status);
        this.props.callback(result.data);
        if (this._isMounted) {
            this.setState({
                taskInfoList: result.data
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
                                initialValue: {task_id: "", status: ""},
                            })(<TaskSearchFormDataInput />)}
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
 * 任务搜索表单
 */
class TaskSearchFormDataInput extends React.Component {

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
            task_id: value.task_id || "",
            status: value.status || "",
        };
    };

    handleTaskIDChange = (e) => {
        const task_id = e.target.value;
        if (!('value' in this.props)) {
            this.setState({task_id});
        }
        this.triggerChange({task_id});
    };

    handleStatusChange = (status) => {
        if (!('value' in this.props)) {
            this.setState({status});
        }
        this.triggerChange({status});
    };

    triggerChange = (changedValue) => {
        // Should provide an event to pass value to Form.
        const onChange = this.props.onChange;
        if (onChange) {
            onChange(Object.assign({}, this.state, changedValue));
        }
    };

    getStatus(status) {
        const roleDict = {"0": "等待中", "1": "扫描中", "2": "扫描结束", "3": "任务被关闭"};
        return roleDict[status];
    }

    render() {
        const {size} = this.props;
        const state = this.state;
        //const status = this.getStatus(state.status);
        return (
            <Row>
                <Col span={12}>
                    <Input
                        prefix={<Icon type="user" style={{color: 'rgba(0,0,0,.25)'}}/>}
                        size={size}
                        value={state.task_id}
                        onChange={this.handleTaskIDChange}
                    />
                </Col>
                <Col span={12}>
                    <Select
                        value={state.status}
                        size={size}
                        style={{width: 200}}
                        onChange={this.handleStatusChange}
                    >
                        <Option value="">默认</Option>
                        <Option value="0">等待中</Option>
                        <Option value="1">扫描中</Option>
                        <Option value="2">扫描结束</Option>
                        <Option value="3">任务被关闭</Option>
                    </Select>
                </Col>
            </Row>
        );
    }
}