/**
 * Created by b5mali4 on 2018/12/6.
 */

import React, {Component} from 'react';
import {request} from '../utils/request';
import {Col, Row, Collapse, Card,} from 'antd';
import * as echarts from 'echarts';
/**
 * 单条扫描记录的漏洞详情
 */
export default class VulnDetails extends Component {
    constructor(props) {
        super(props);
        this.state = {
            details: [],
            level: {},
            type: {},
        };
    };

    componentDidMount() {
        this.onLoadData();
    };

    async onLoadData() {
        let {match: {params}} = this.props;
        let result = await request("/user/vulnerability/details/filter/?task_id=" + params.id);
        this.setState({
            details: result.vlun.details,
            level: result.vlun.level,
            type: result.vlun.type,
        });
        this.showLevelPie(result.vlun.level);
        this.showTypePie(result.vlun.type);

    };

    getLevelData(level) {
        let levelDateList = new Array();
        if (level.high > 0) {
            levelDateList.push("高危");
        }
        if (level.middle > 0) {
            levelDateList.push("中危");
        }
        if (level.low > 0) {
            levelDateList.push("低危");
        }
        return levelDateList;
    }

    showLevelPie(level) {
        let dom = this.refs["level-pie"];
        let LevelPieChart = echarts.init(dom);
        let app = {};
        let option = null;

        option = {
            title: {
                text: '等级统计',
                x: 'left'
            },
            tooltip: {
                trigger: 'item',
                formatter: "{a} <br/>{b}: {c} ({d}%)"
            },
            legend: {
                orient: 'vertical',
                x: 'right',
                data: this.getLevelData(level),
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
            color: ['#008fff', '#57cbe9', '#00c5c4']

        };
        if (option && typeof option === "object") {
            LevelPieChart.setOption(option, true);
        }
    }

    //根据实际数据展示类型
    getTypeData(type) {
        let typeDateList = new Array();
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
        app.title = '环形图';

        option = {
            title: {
                text: '类型统计',
                x: 'left'
            },
            tooltip: {
                trigger: 'item',
                formatter: "{a} <br/>{b}: {c} ({d}%)"
            },
            legend: {
                orient: 'vertical',
                x: 'right',
                data: this.getTypeData(type),
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

    render() {

        return (
            <div>
                <Row>
                    <Col span={12} style={{paddingRight: 5}}>
                        <div ref="level-pie" style={{height: 300, background: '#fff', borderRadius: 5, padding: 10}}>
                        </div>
                    </Col>
                    <Col span={12} style={{paddingLeft: 5}}>
                        <div ref="type-pie" style={{height: 300, background: '#fff', borderRadius: 5, padding: 10}}>
                        </div>
                    </Col>
                </Row>
                <br/>
                <VulnDetailCard details={this.state.details} ></VulnDetailCard>
            </div>
        )
    }
}

/**
 * 漏洞详情卡片，包含类型、等级、描述等等，可展开
 */
class VulnDetailCard extends Component {

    constructor(props) {
        super(props);
        this.props = props;
    }
    render() {
        return (
            <Row>
                <Col span={24}>
                    <Collapse bordered={false}>
                        {
                            this.props.details.map((item, index) => {
                                //console.log(item);
                                const data = item;
                                //const data = JSON.parse(item);
                                return (
                                    <Collapse.Panel key={index} header={data.info}>

                                        <Card
                                            type="inner"
                                            title="漏洞类型"
                                        >
                                            {data.chinese_type}
                                        </Card>
                                        <Card
                                            type="inner"
                                            title="漏洞等级"
                                        >
                                            {data.level}
                                        </Card>
                                        <Card
                                            type="inner"
                                            title="poc"
                                        >
                                            {data.payload}
                                        </Card>
                                        <Card
                                            type="inner"
                                            title="漏洞描述"
                                        >
                                            {data.description}

                                        </Card>
                                        <Card
                                            type="inner"
                                            title="影响版本"
                                        >
                                            {data.imp_version}

                                        </Card>
                                        <Card
                                            type="inner"
                                            title="修复建议"
                                        >
                                            {data.repair}
                                        </Card>
                                    </Collapse.Panel>
                                )
                            })
                        }
                    </Collapse>
                </Col>
            </Row>
        )
    }
}