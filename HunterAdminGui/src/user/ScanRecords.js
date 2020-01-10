/**
 * Created by b5mali4 on 2018/12/5.
 */
import React, {Component} from 'react';
import {request} from '.././utils/request';
import {Table} from 'antd';
import {Link} from "react-router-dom";

/**
 * 用户扫描记录表单
 */
export default class UserScanRecordsTable extends Component {
    constructor(props) {
        super(props);
        this.state = {
            filterDropdownVisible: false,
            data: [],
            searchText: '',
            filtered: false,
        };
    }

    componentWillMount() {
        this.onLoadData();
    };

    /**
     * 记载扫描记录数据
     * @returns {Promise.<void>}
     */
    async onLoadData() {
        const result = await request("/user/scan_record/");
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