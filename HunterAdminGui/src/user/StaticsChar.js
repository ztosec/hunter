/**
 * Created by b5mali4 on 2018/12/6.
 */
import React, {Component} from 'react';
import {request} from '../utils/request';
import {Col, Row, Collapse, Icon, Card, Tooltip, message} from 'antd';
import * as echarts from 'echarts';
import {ChartCard, Field, MiniArea, MiniBar, MiniProgress} from 'ant-design-pro/lib/Charts';
import moment from 'moment';

/**
 * 波浪形个数统计图
 */
class NumChartCard extends Component {
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
                    x: key.split(" ")[0],
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

/**
 * 统计报表
 */
export default class StaticsChar extends Component {

    constructor(props) {
        super(props);
        this.state = {
            taskUrlVulnNum: {},
            level: {},
            type: {},
            dateList: [],
        };
    }

    /**
     * 初始化日期
     * 将2018-12-05 00:00:00处理成2018-12-05
     */
    getDates(dateList){
        let resultList = new Array()
        dateList.forEach(function (item, index) {
            resultList.push(item.split(" ")[0])
            //this.state.dateList.append(item.split(" ")[0])
        });
        return resultList;
    }

    componentWillMount() {
        this.onLoadData();
    }

    async onLoadData() {
        const {match: {params}} = this.props;
        await this.loadVulnstatisticsData();
        await this.loadTasksurlsvulnsData();
        await this.loadTasktimeData();
    };

    async loadVulnstatisticsData() {
        let result = await request("/user/vulnstatistics/count/");
        this.showLevelPie(result.data.level);
        this.showTypePie(result.data.type);
    }

    async loadTasksurlsvulnsData() {
        const result = await request("/user/tasksurlsvulns/count/filter/?day_range=100");
        this.showTaskUrlVulnLine(result.data);
        //console.log(taskUrlVulnNumResult);
        this.setState({
            taskUrlVulnNum: result.data
        });
    }
    async loadTasktimeData() {
        const result = await request("/user/tasktime/filter/?count=10");
        this.showTaskTime(result.data);
    }


    showTaskUrlVulnLine(taskUrlVulnNum) {
        let dom = this.refs["task-url-vlue-line"];
        console.log(taskUrlVulnNum.task);
        let taskUrlVlueChart = echarts.init(dom);
        let app = {};
        let option = null;
        option = {
            title: {
                text: '趋势图'
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
                data :this.getDates(Object.keys(taskUrlVulnNum.task)),
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

    //根据实际数据展示类型
    getTypeData(type) {
        var typeDateList = new Array();
        if (type.sql_inject > 0) {
            typeDateList.push("sql注入")
        }
        if (type.xss > 0) {
            typeDateList.push("xss")
        }
        if (type.xxe > 0) {
            typeDateList.push("xxe")
        }
        if (type.weak_pwd > 0) {
            typeDateList.push("弱密码")
        }
        if (type.cmdect > 0) {
            typeDateList.push("命令执行")
        }
        if (type.file_read > 0) {
            typeDateList.push("任意读取")
        }
        if (type.file_upload > 0) {
            typeDateList.push("任意上传")
        }
        if (type.file_include > 0) {
            typeDateList.push("任意包含")
        }
        if (type.ddos > 0) {
            typeDateList.push("拒绝服务")
        }
        if (type.csrf > 0) {
            typeDateList.push("csrf")
        }
        if (type.cors > 0) {
            typeDateList.push("cors")
        }
        if (type.jsonp > 0) {
            typeDateList.push("jsonp")
        }
        if (type.info_leak > 0) {
            typeDateList.push("信息泄漏")
        }
        if (type.crlf > 0) {
            typeDateList.push("crlf")
        }
        if (type.other > 0) {
            typeDateList.push("其他")
        }
        if (type.hidden_danger > 0) {
            typeDateList.push("隐藏风险")
        }
        return typeDateList;
    }

    showTypePie(type) {

        let dom = this.refs["type-pie"];
        let TypePieChart = echarts.init(dom, 'light');
        let app = {};
        let option = null;

        option = {
            title: {
                text: '漏洞类型',
                x: 'left'
            },
            tooltip: {
                trigger: 'item',
                formatter: "{a} <br/>{b}: {c} ({d}%)"
            },
            legend: {
                orient: 'vertical',
                x: 'right',
                data: this.getTypeData(type)
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

        option = {
            title: {
                text: '漏洞类型',
                x: 'left'
            },
            tooltip: {
                trigger: 'item',
                formatter: "{a} <br/>{b}: {c} ({d}%)"
            },
            legend: {
                orient: 'vertical',
                x: 'right',
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

        option = {
            title: {
                text: '任务执行时间统计',
                x: 'left'
            },
            color: ['#3398DB'],
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
                    barWidth: '10%',
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
        return (
            <Row>
                <Row>
                    <Col span={8}>
                        <div>
                            <NumChartCard title="任务个数" total={state.taskUrlVulnNum.task_total_num} color="#75d9b0"
                                          borderColor="#1dc98e" data={state.taskUrlVulnNum.task}/>
                        </div>
                    </Col>
                    <Col span={8}>
                        <div>
                            <NumChartCard title="请求数量" total={state.taskUrlVulnNum.url_total_num} color="#F0818B"
                                          borderColor="#e64658" data={state.taskUrlVulnNum.url}/>
                        </div>
                    </Col>
                    <Col span={8}>
                        <div>
                            <NumChartCard title="漏洞数量" total={state.taskUrlVulnNum.vuln_total_num} color="#BCAAFF"
                                          borderColor="#975fe4" data={state.taskUrlVulnNum.vuln}/>
                        </div>
                    </Col>
                </Row>
                <br/>
                <Row>
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
                <Row>
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
