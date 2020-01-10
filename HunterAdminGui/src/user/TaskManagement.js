/**
 * Created by b5mali4 on 2018/12/5.
 */
import React, {Component} from 'react';
import {
    Table, Select, Row, Col, Collapse, Card, Input, Button, Icon, Form, Modal, Dropdown, Menu, Progress, message
} from 'antd';
import {Redirect} from "react-router-dom";
import {WaterWave} from 'ant-design-pro/lib/Charts';
import {request, STATUS_CODES} from '../utils/request';
import {BrowserRouter as Router, Route, Link, Switch, NavLink} from "react-router-dom";
import task1png from '../assets/task1.png';
import task2png from '../assets/task2.png';
import task3png from '../assets/task3.png';
const Option = Select.Option;
const FormItem = Form.Item;
const confirm = Modal.confirm;

//任务列表
export default class UserTaskManagement extends Component {
    constructor(props) {
        super(props);
        this.state = {
            currentTaskInfo: {
                'create_time': '',
                'percent': 100,
                'scaned_url_num': 0,
                'unscaned_url_num': 0,
                'task_name': '',
                'total_url_num': 0,
                'username': '',
                'receiver_emails': '',
            },
            currentTaskInfos: [],
            unscanedTaskNum: 0,
            scanedTaskNum: 0,
        };
    }

    componentWillMount() {
        this.onLoadData();
    };

    /**
     * 加载当前任务 currenttasks
     * @returns {Promise.<void>}
     */
    async onLoadData() {
        const result = await request("/user/current_tasks/", false);
        this.setState({
            currentTaskInfos: result.data.working_task_info_list,
            unscanedTaskNum: result.data.working_task_num,
            scanedTaskNum: result.data.completed_task_num,
        });

    };

    render() {
        const currentTaskInfos = this.state.currentTaskInfos;
        var currentTaskInfo = this.state.currentTaskInfo;
        const scanedTaskNum = this.state.scanedTaskNum;
        const unscanedTaskNum = this.state.unscanedTaskNum;
        if (currentTaskInfos.length > 0) {
            currentTaskInfo = currentTaskInfos[0];
        }
        return (
            <Row>
                <Row style={{background: '#fff'}}>
                    <TopArea currentTaskInfo={currentTaskInfo} unscanedTaskNum={unscanedTaskNum}
                             scanedTaskNum={scanedTaskNum}> </TopArea>
                </Row>
                <Row style={{background: '#fff', marginTop: 25}}>
                    <TaskManagementTable currentTaskInfos={currentTaskInfos}></TaskManagementTable>
                </Row>

            </Row>
        )
    }

}
/**
 *展示当前任务详情
 */
class TopArea extends Component {

    constructor(props) {
        super(props);
        this.props = props;
    }

    render() {
        const currentTaskInfo = this.props.currentTaskInfo;
        const unscanedTaskNum = this.props.unscanedTaskNum;
        const scanedTaskNum = this.props.scanedTaskNum;
        return (
            <Row>
                <Col span={8}>
                    <Row>
                        <Col span={12} style={{textAlign: 'right'}}>
                            <img src={task1png} style={{marginTop: '20px', marginBottom: '20px'}}/>
                        </Col>
                        <Col span={12}>
                            <div style={{
                                position: 'relative',
                                textAlign: 'center',
                                marginTop: 20,
                                marginBottom: 20,
                                borderRight: '1px solid rgb(232, 232, 232)'
                            }}>
                                <span>待检测</span>
                                <p style={{
                                    color: 'rgba(0,0,0,.85)',
                                    fontSize: 24,
                                    lineHeight: 2,
                                    margin: 0
                                }}>{unscanedTaskNum}个任务</p>
                            </div>
                        </Col>
                    </Row>
                </Col>
                <Col span={8}>
                    <Row>
                        <Col span={12} style={{textAlign: 'right'}}>
                            <img src={task2png} style={{marginTop: '20px', marginBottom: '20px'}}/>
                        </Col>
                        <Col>
                            <div style={{
                                position: 'relative',
                                textAlign: 'center',
                                marginTop: 20,
                                marginBottom: 20,
                                borderRight: '1px solid rgb(232, 232, 232)'
                            }}>
                                <span>已检测</span>
                                <p style={{
                                    color: 'rgba(0,0,0,.85)',
                                    fontSize: 24,
                                    lineHeight: 2,
                                    margin: 0
                                }}>{scanedTaskNum}个任务</p>
                            </div>
                        </Col>
                    </Row>
                </Col>
                <Col span={8}>
                    <Row>
                        <Col span={12} style={{textAlign: 'right'}}>
                            <img src={task3png} style={{marginTop: '20px', marginBottom: '20px'}}/>
                        </Col>
                        <Col>
                            <div style={{position: 'relative', textAlign: 'center', marginTop: 20, marginBottom: 20}}>
                                <span>当前任务</span>
                                <p style={{
                                    color: 'rgba(0,0,0,.85)',
                                    fontSize: 24,
                                    lineHeight: 2,
                                    margin: 0
                                }}>{currentTaskInfo.total_url_num}个接口</p>
                            </div>
                        </Col>
                    </Row>
                </Col>
            </Row>
        )
    }
}
/**
 * 任务列表
 */
class TaskManagementTable extends Component {
    constructor(props) {
        super(props);
        this.props = props;
    }

    render() {
        //const currentTaskInfos = this.props.currentTaskInfos;
        const currentTaskInfoList = this.props.currentTaskInfos;

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
                dataIndex: 'username',
                key: 'username',
            }, {
                title: '开始时间',
                dataIndex: 'create_time',
                key: 'create_time',
            }, {
                title: '扫描状态',
                render: (value, row, index) => (
                    <TaskStatusModal index={index} taskStatusId={value.task_status}></TaskStatusModal>
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
                        <Col span={12}><TaskInfoModal hook_rule={record.hook_rule} receiver_emails={record.receiver_emails} task_name={record.task_name} task_id={record.task_id}/></Col>
                        <Col span={12}><MoreDropdown task_id={record.task_id}/></Col>
                    </Row>)
            },];
        return (
            <Row>
                <div style={{background: '#fff'}}>
                    <Row style={{paddingLeft: 20, paddingRight: 20, marginTop: 20, textAlign: 'center'}}>
                        <AddTaskModal />
                        <Table style={{marginTop: 10}} rowKey='task_id' columns={columns}
                               dataSource={currentTaskInfoList}/>
                    </Row>
                </div>

            </Row>
        )
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
        const taskStatusId = this.props.taskStatusId;
        const index = this.props.index;
        //默认第一个前端才显示运行中，后面都显示待运行
        if (index === 0) {
            return <div style={{color: "#f81d22"}}>运行中</div>
        } else {
            if (taskStatusId === 0 || taskStatusId === 1) {
                return <div>等待中</div>;
            } else if (taskStatusId === 2) {
                return <div>任务关闭</div>
            } else if (taskStatusId === 3) {
                return <div>扫描结束</div>
            }
        }
    }

}

/**
 * 新建任务按钮触发
 */
class AddTaskModal extends Component {
    state = {visible: false};

    showModal = () => {
        this.setState({
            visible: true,
        });
    }

    handleOk = (e) => {
        this.setState({
            visible: false,
        });
        //这里调用提交表单的回调函数，UserInfoModalForm组件中
        //console.log("新建任务提交了表单哦")
        let form = this.refs.getFormVlaue;//通过refs属性可以获得对话框内form对象
        form.validateFields((err, values) => {
            if (!err) {
                if (values.data.hookRule === undefined || values.data.hookRule.length <= 0 || values.data.taskName === undefined || values.data.taskName.length <= 0) {
                    message.error("创建失败，必填项不能为空");
                    return;
                }
                /*if (values.data.receiverEmails != undefined && values.data.receiverEmails.length > 0) {
                    var reg = new RegExp(/^([a-zA-Z0-9._-])+@([a-zA-Z0-9_-])+(\.[a-zA-Z0-9_-])+/);
                    if (!reg.test(values.data.receiverEmails)) {//正确的邮箱格式
                        message.error("创建失败，邮箱格式错误");
                        return;
                    }
                }*/
                console.log(values);//这里可以拿到数据
                this.createTask(values.data.hookRule, values.data.taskName, values.data.receiverEmails);
            }
        });
    };

    /**
     * 创建新任务
     * @param hookRule
     * @param taskName
     * @param receiverEmails
     * @returns {Promise.<void>}
     */
    async createTask(hookRule, taskName, receiverEmails) {
        await request('/user/tasks/', true, {
            method: "POST",
            body: JSON.stringify({
                "read_agreement": "true",
                "hook_rule": hookRule,
                "task_name": taskName,
                "receiver_email": receiverEmails
            })
        });
    }

    handleCancel = (e) => {
        //console.log(e);
        this.setState({
            visible: false,
        });
    }

    render() {
        const state = this.state;
        const WrappedUserInfoModalForm = Form.create()(TaskInfoModalForm);
        return (
            <div>
                <Button type="dashed" icon="plus" style={{width: '100%'}} onClick={this.showModal}>新建任务</Button>
                <Modal
                    title="编辑任务信息"
                    visible={this.state.visible}
                    onOk={this.handleOk}
                    onCancel={this.handleCancel}
                    width="40%"
                >
                    <WrappedUserInfoModalForm disabled={false} ref="getFormVlaue"/>
                </Modal>
            </div>
        );
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
        await request('/user/tasks/', true, {
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
 * 操作更多
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
        }
        ;
        var sentStopTask = async function (taskId) {
            const result = await request("/user/tasks/", true, {method: "DELETE", body: JSON.stringify({"task_id": taskId})});
            if (result != undefined && result.status == STATUS_CODES.HTTP_OK) {
                message.info('结束任务成功');
                window.setTimeout(window.location.href = result.site, 500);
            }
        };

    }


    render() {
        const taskId = this.props.task_id;
        const menu = (
            <Menu>
                <Menu.Item>
                    <a target="_blank" onClick={() => this.stopTaskConfirm(this.props.task_id)}>结束</a>
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