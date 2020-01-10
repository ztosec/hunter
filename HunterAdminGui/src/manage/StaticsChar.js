/**
 * Created by b5mali4 on 2018/8/2.
 */
import React, {Component} from 'react';
import {request} from '../utils/request';
import userpic from '../assets/user.png';
import {Col, Row, Collapse, Card, Tooltip, Icon} from 'antd';
import * as echarts from 'echarts';
import {ChartCard, Field, MiniArea, yuan, MiniBar, MiniProgress} from 'ant-design-pro/lib/Charts';


class UserCard extends Component {
    constructor(props) {
        super(props)
        this.props = props;
    }

    render() {
        const props = this.props;
        return (
            <ChartCard
                title="用户数"
                style={{borderRadius: 5, textAlign: 'center'}}
                avatar={
                    <img
                        style={{width: 66, height: 66}}
                        src={userpic}
                        alt="indicator"
                    />
                }
                total={<font style={{fontSize: 35}}>{props.total}</font>}
                footer={<div></div>}
            />
        )
    }
}
class NumAreaCard extends Component {
    constructor(props) {
        super(props);
        this.props = props;
    }

    render() {
        const props = this.props;
        const visitData = [];
        const beginDay = new Date().getTime();
        if (props.data) {
            for (let key in props.data) {
                visitData.push({
                    x: key,
                    y: props.data[key],
                })
            }
        }
        return (<ChartCard
            style={{borderRadius: 5}}
            title={<span>{props.title}</span>}
            total={<font style={{fontSize: 35}}>{props.total}</font>}
            contentHeight={67}
        >
            <MiniArea
                color={props.color}
                borderColor={props.borderColor}
                line
                height={45}
                data={visitData}
            />
        </ChartCard>)
    }
}

class TaskStateDivs extends Component {
    constructor(props) {
        super(props);
        this.props = props;
    }

    render() {
        const props = this.props;
        if (props.tasks == undefined) {
            return (<div style={{ position: 'relative', padding: '10px', border: '1px solid rgb(238, 238, 238)', borderRadius: 4, color: '#666666'}}> </div>);
        }
        //console.log(props.tasks)
        var boxs = [];

        props.tasks.map(function (task) {
            //console.log(task);
            var action;
            if (task.killed_time !== "" && task.killed_time !== "None") {
                action = <div key={task.id}>在<span style={{color: "rgb(10, 188, 60)", padding: "0px 4px"}}>{task.killed_time}</span>结束了任务 </div>;
            }
            else {
                action = <div key={task.id}>在<span style={{color: "rgb(10, 188, 60)", padding: "0px 4px"}}>{task.created_time}</span>创建了任务</div>;
            }
            //console.log(action);
            boxs.push(
                <Col key={task.id} span={6} style={{padding: '5px'}}>
                    <div style={{
                        position: 'relative',
                        padding: '10px',
                        border: '1px solid rgb(238, 238, 238)',
                        borderRadius: 4,
                        color: '#666666'
                    }}>
                        <div style={{
                            marginBottom: 8,
                            color: 'rgb(51, 51, 51)',
                            fontSize: 15,
                            height: 14,
                            textOverflow: 'ellipsis',
                            whiteSpace: 'nowrap',
                            fontWeight: 'bold'
                        }}>
                            @{task.full_name}
                        </div>
                        {action}
                    </div>
                </Col>
            )

        });
        return (<Row>{boxs}</Row>);
    }
}

export default class AdminStaticsChar extends Component {
    constructor(props) {
        super(props);
        this._isMounted = true;
        this.state = {
            taskUrlVulnNum: {},
            userList: {},
            taskList: {}
        };
    }

    componentDidMount() {
        this.onLoadData()
    };

    componentWillUnmount() {
        this._isMounted = false;
    };


    async onLoadData() {
        const {match: {params}} = this.props;
        this.loadVulnstatisticsData();
        this.loadTasksurlsvulnsData();
        this.loadUserListData();
        this.loadTaskListData();
        this.loadTaskTimeData();
    };

    /**
     * 统计数据
     * @returns {Promise.<void>}
     */
    async loadVulnstatisticsData() {
        const result = await request("/admin/vulnstatistics/count/");
        this.showLevelPie(result.data.level);
        this.showTypePie(result.data.type);
    }

    async loadTasksurlsvulnsData() {
        const result = await request("/admin/tasksurlsvulns/count/filter/?days=100");
        this.showTaskUrlVlueLine(result.data);
        if (this._isMounted) {
            this.setState({
                taskUrlVulnNum: result.data
            });
        }
    }

    /**
     * 获取用户列表
     * @returns {Promise.<void>}
     */
    async loadUserListData() {
        const result = await request("/admin/user/");
        if (this._isMounted) {
            this.setState({
                userList: result.data
            });
        }
    }

    /**
     * 获取任务列表
     * @returns {Promise.<void>}
     */
    async loadTaskListData() {
        const result = await request("/admin/tasks/?num=4");
        if (this._isMounted) {
            this.setState({
                taskList: result.data
            });
        }
    }

    /**
     * 任务时间
     * @returns {Promise.<void>}
     */
    async loadTaskTimeData(){
        const result = await request("/admin/tasktime/filter/?count=100")
        this.showTaskTime(result.data);
    }


    showTaskUrlVlueLine(taskUrlVulnNum) {
        let dom = this.refs["task-url-vlue-line"];
        //console.log(dom);
        let taskUrlVlueChart = echarts.init(dom);
        let app = {};
        let option = null;
        app.title = '环形图';
        option = {
            title: {
                text: '折线图堆叠'
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: ['任务', 'url', '漏洞',]
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            toolbox: {
                feature: {
                    saveAsImage: {}
                }
            },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                //data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
                data: Object.keys(taskUrlVulnNum.task),
            },
            yAxis: {
                type: 'value'
            },
            series: [
                {
                    name: '任务',
                    type: 'line',
                    stack: '总量',
                    data: Object.values(taskUrlVulnNum.task),
                },
                {
                    name: 'url',
                    type: 'line',
                    stack: '总量',
                    data: Object.values(taskUrlVulnNum.url),
                },
                {
                    name: '漏洞',
                    type: 'line',
                    stack: '总量',
                    data: Object.values(taskUrlVulnNum.vuln),
                }
            ]
        };
        if (option && typeof option === "object") {
            taskUrlVlueChart.setOption(option, true);
        }


    }

    showTypePie(type) {

        let dom = this.refs["type-pie"];
        let TypePieChart = echarts.init(dom, 'light');
        let app = {};
        let option = null;
        app.title = '环形图';

        option = {
            tooltip: {
                trigger: 'item',
                formatter: "{a} <br/>{b}: {c} ({d}%)"
            },
            legend: {
                orient: 'vertical',
                x: 'left',
                data: ['sql注入', 'xss', 'xxe', '弱密码', '命令执行', '任意读取', '任意上传', '任意包含', '拒绝服务', 'csrf', 'cors', 'jsonp', '信息泄漏', 'crlf', '其他', '隐藏风险']
            },
            series: [
                {
                    name: '访问来源',
                    type: 'pie',
                    radius: ['54%', '70%'],
                    avoidLabelOverlap: false,
                    label: {
                        normal: {
                            show: false,
                            position: 'center'
                        },
                        emphasis: {
                            show: true,
                            textStyle: {
                                fontSize: '30',
                                fontWeight: 'bold'
                            }
                        }
                    },
                    labelLine: {
                        normal: {
                            show: false
                        }
                    },


                    data: [
                        {value: type.sql_inject, name: 'sql注入'},
                        {value: type.xss, name: 'xss'},
                        {value: type.xxe, name: 'xxe'},
                        {value: type.weak_pwd, name: '弱密码'},
                        {value: type.cmdect, name: '命令执行'},
                        {value: type.file_read, name: '任意读取'},
                        {value: type.file_upload, name: '任意上传'},
                        {value: type.file_include, name: '任意包含'},
                        {value: type.ddos, name: '拒绝服务'},
                        {value: type.csrf, name: 'csrf'},
                        {value: type.cors, name: 'cors'},
                        {value: type.jsonp, name: 'jsonp'},
                        {value: type.info_leak, name: '信息泄漏'},
                        {value: type.crlf, name: 'crlf'},
                        {value: type.other, name: '其他'},
                        {value: type.hidden_danger, name: '隐藏风险'}
                    ]
                },
            ],
        };
        if (option && typeof option === "object") {
            TypePieChart.setOption(option, true);
        }
    }

    showLevelPie(level) {
        let dom = this.refs["level-pie"];
        let LevelPieChart = echarts.init(dom);
        let app = {};
        let option = null;
        app.title = '环形图';

        option = {
            tooltip: {
                trigger: 'item',
                formatter: "{a} <br/>{b}: {c} ({d}%)"
            },
            legend: {
                orient: 'vertical',
                x: 'left',
                data: ['高危', '中危', '低危',]
            },
            series: [
                {
                    name: '访问来源',
                    type: 'pie',
                    radius: ['54%', '70%'],
                    avoidLabelOverlap: false,
                    label: {
                        normal: {
                            show: false,
                            position: 'center'
                        },
                        emphasis: {
                            show: true,
                            textStyle: {
                                fontSize: '30',
                                fontWeight: 'bold'
                            }
                        }
                    },
                    labelLine: {
                        normal: {
                            show: false
                        }
                    },
                    data: [
                        {value: level.high, name: '高危'},
                        {value: level.middle, name: '中危'},
                        {value: level.low, name: '低危'},
                    ]
                }
            ],
            color: ['#008fff', '#57cbe9', '#00c7ed']

        };
        if (option && typeof option === "object") {
            LevelPieChart.setOption(option, true);
        }
    }

    /**
     * 显示每次任务消耗的时间，最多显示最近10次
     */
    showTaskTime(taskTime) {
        let dom = this.refs["tasktime-bar"];
        let taskTimeBarChart = echarts.init(dom);
        let app = {};
        let option = null;

        app.title = {
            text: '任务耗时间统计',
        };
        option = {
            color: ['#3398DB'],
            title: {
                text: '任务耗时间统计'
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                    type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                }
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: [
                {
                    type: 'category',
                    data: taskTime.map(function (v) {
                        return v.id;
                    }),
                    axisTick: {
                        alignWithLabel: true
                    }
                }
            ],
            yAxis: [
                {
                    type: 'value'
                }
            ],
            series: [
                {
                    name: '直接访问',
                    type: 'bar',
                    barWidth: '100%',
                    data: taskTime.map(function (v) {
                        return v.spend_time;
                    }),
                    //data: {taskTime.} [10, 52, 200, 334, 390, 330, 220]
                }
            ],
            color: ['#47a3f4']
        };
        if (option && typeof option === "object") {
            taskTimeBarChart.setOption(option, true);
        }
    }

    //任务次数和漏洞数量表url数量，横坐标为时间 task-url-vlue-line
    //横坐标是任务名称，纵坐标是漏洞数量,top10 task-vlue-line
    render() {
        const state = this.state;
        //console.log(state.taskList.tasks);
        return (
            <Row>
                <Row style={{marginBottom: 20}}>
                    <Col span={6}>
                        <div>
                            <UserCard total={state.userList.num}/>
                        </div>
                    </Col>
                    <Col span={6}>
                        <div>
                            <NumAreaCard title="任务数" total={state.taskUrlVulnNum.task_total_num} color="#75d9b0"
                                         borderColor="#1dc98e" data={state.taskUrlVulnNum.task}/>
                        </div>
                    </Col>
                    <Col span={6}>
                        <div>
                            <NumAreaCard title="漏洞数" total={state.taskUrlVulnNum.vuln_total_num} color="#BCAAFF"
                                         borderColor="#975fe4" data={state.taskUrlVulnNum.vuln}/>
                        </div>
                    </Col>
                    <Col span={6}>
                        <div>
                            <NumAreaCard title="请求数" total={state.taskUrlVulnNum.url_total_num} color="#F0818B"
                                         borderColor="#e64658" data={state.taskUrlVulnNum.url}/>
                        </div>
                    </Col>
                </Row>
                <Row style={{marginBottom: 20}}>
                    <Col span={24}>
                        <Card
                            title={<font style={{fontSize: 18, fontWeight: 'bold'}}>用户使用动态</font>}
                        >
                            <TaskStateDivs tasks={state.taskList.tasks}/>
                        </Card>
                    </Col>
                </Row>

                <Row style={{marginBottom: 20}}>
                    <Col span={12} style={{paddingRight: 5}}>
                        <div ref="level-pie"
                             style={{height: 300, background: '#fff', borderRadius: 5, padding: 10}}>
                        </div>
                    </Col>
                    <Col span={12} style={{paddingLeft: 5}}>
                        <div ref="type-pie" style={{height: 300, background: '#fff', borderRadius: 5, padding: 10}}>
                        </div>
                    </Col>
                </Row>
                <Row style={{marginBottom: 20}}>
                    <Col span={12} style={{paddingRight: 5, paddingTop: 5}}>
                        <div ref="task-url-vlue-line"
                             style={{height: 300, background: '#fff', borderRadius: 5, padding: 10}}></div>
                    </Col>
                    <Col span={12} style={{paddingLeft: 5, paddingTop: 5}}>
                        <div ref="tasktime-bar"
                             style={{height: 300, background: '#fff', borderRadius: 5, padding: 10}}></div>
                    </Col>
                </Row>

            </Row>
        )
    }
}
