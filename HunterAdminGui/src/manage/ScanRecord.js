/**
 * Created by b5mali4 on 2018/8/2.
 */
import React, {Component} from 'react';
import {request} from '../utils/request';
import {Table} from 'antd';
import {BrowserRouter as Router, Route, Link, Switch, NavLink} from "react-router-dom";

export default class AdminScanRecordTable extends Component {
    constructor(props){
        super(props);
    }
    state = {
        filterDropdownVisible: false,
        data: [],
        searchText: '',
        filtered: false,
    };

    componentWillMount() {
        console.log("AdminScanRecordTable");
        this.onLoadData();
    };

    async onLoadData() {
        const {match: {params}} = this.props;
        const result = await request("/admin/scan_record/filter/?user_id=" + params.userid);
        this.setState({
            data: result.data
        });

    };

    render() {
        const columns = [{
            title: 'ID',
            dataIndex: 'task_id',
            key: 'taskId',
        }, {
            title: '创建时间',
            dataIndex: 'created_time',
            key: 'createTime',
        }, {
            title: '任务名',
            dataIndex: 'task_name',
            key: 'taskName',
            render: (text, record) => <Link to={"/scanrecord/" + record.task_id}>{text}</Link>
        }, {
            title: 'url数量',
            dataIndex: 'urls_num',
            key: 'urlNum',
        }, {
            title: '漏洞数量',
            dataIndex: 'vulns_num',
        }, {
            title: '风险等级',
            dataIndex: 'risk_level',
        }];
        return <Table style={{background: '#fff'}}  rowKey={record => record.task_id} columns={columns} dataSource={this.state.data}/>;
    }
}